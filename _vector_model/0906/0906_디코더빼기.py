import os
import shutil
from PIL import Image
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min, pairwise_distances
from sklearn.manifold import TSNE
import csv
from tensorflow.keras import Model 
from tensorflow.keras.layers import UpSampling2D, Conv2D, Dense, Flatten, Reshape, Input, MaxPooling2D
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.applications import VGG16
import json
import io


# Blob to PNG 함수
def convert_blob_to_png(blob_path, png_path):
    with open(blob_path, 'rb') as f:
        blob_data = f.read()
    image = Image.open(io.BytesIO(blob_data))
    image.save(png_path)



# 상대 경로
relative_path = "../../../crawling_project/result/onpice_clothes"

# 경로가 존재하는지 확인
if os.path.exists(relative_path):
    print("경로존재")
else:
    print("경로없음")


categories = ['onpice_clothes', 'outer_clothes', 'under_skirt_clothes', 'upper_clothes']
model_info_dict = {}
all_data = []

image_size = (32, 32)

def load_and_preprocess_image(image_path, image_size):
    try:
        image = Image.open(image_path).resize(image_size)
        image_array = np.array(image)
        if len(image_array.shape) == 2:  # 흑백 이미지일 경우
            image_array = np.stack([image_array] * 3, axis=2)
        return image_array
    except Exception as e:
        print(f"Error occurred when processing {image_path}: {e}")
        return None

for category in categories:
    source_folder = f"../../../crawling_project/result/{category}"
    
    # Blob 파일을 PNG로 변환
    for filename in os.listdir(source_folder):
        if filename.endswith('.blob'):
            blob_path = os.path.join(source_folder, filename)
            png_path = os.path.join(source_folder, filename.replace('.blob', '.png'))
            convert_blob_to_png(blob_path, png_path)
 
    image_files = [f for f in os.listdir(source_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]  
    train_files, test_files = train_test_split(image_files, test_size=0.2, random_state=42)

    train_images_list = []
    for file in train_files:
        img = load_and_preprocess_image(os.path.join(source_folder, file), image_size)
        if img is not None:
            train_images_list.append(img)
    train_images_list = [img[:, :, :3] if img.shape[2] == 4 else img for img in train_images_list]    
    train_images = np.array(train_images_list)
    
    test_images_list = [load_and_preprocess_image(os.path.join(source_folder, file), image_size) for file in test_files]
    test_images_list = [img for img in test_images_list if img is not None]
    test_images_list = [img[:, :, :3] if img.shape[2] == 4 else img for img in test_images_list]
    test_images = np.array(test_images_list)

    

    # # 이미지 데이터를 불러와서 NumPy 배열로 변환
    # train_images = np.array([np.array(Image.open(os.path.join(source_folder, file)).resize(image_size)) for file in train_files])
    # test_images = np.array([np.array(Image.open(os.path.join(source_folder, file)).resize(image_size)) for file in test_files])

    # 데이터 정규화
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    # TensorFlow 변수에 할당 (여기서는 MNIST 예제와 유사하게 변수명을 사용)
    train_X, train_Y = train_images, None  # train_Y는 필요에 따라 레이블을 할당
    test_X, test_Y = test_images, None  # test_Y는 필요에 따라 레이블을 할당

    print(train_X.shape)
    print(test_X.shape)

    ## 인코더만 학습하기 위해선, 데이터 자체의 차원을 인코더 아웃풋과 똑같이 맞춰서 입력으로 넣어줘야한다. 여기서 정보손실이 발생할 우려가 있다.
    
    # 인코더 부분 정의
    input_img = Input(shape=(32, 32, 3))
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)

    # 인코더 모델 정의
    encoder = Model(input_img, encoded)
    encoder.compile(optimizer='adam', loss='binary_crossentropy', metrics=['mse'])

    # 학습 (예: 50 에포크, 배치 크기 128)
    encoder.fit(train_X, train_X, epochs=50, batch_size=128)

    h5save_path = "../../9oz-project/h5model/"
    
    # 카테고리별로 인코더 모델 저장
    encoder_model_path = os.path.join(h5save_path, f"encoder_only_{category}.h5")
    encoder.save(encoder_model_path)

    # 잠재 벡터 추출
    latent_vectors = encoder.predict(train_X)
       

    # K-means 군집화
    n_clusters = 10  # 군집의 수
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(latent_vectors)

    # 각 데이터 포인트의 군집 중심까지의 거리 계산
    individual_distances = np.linalg.norm(latent_vectors - kmeans.cluster_centers_[kmeans.labels_], axis=1)

    # DataFrame 생성 전에 길이 확인
    assert len(train_files) == latent_vectors.shape[0] == len(kmeans.labels_) == len(individual_distances)

    # 정보 저장
    model_info = {
        'latent_vectors': latent_vectors,
        'kmeans_labels': kmeans.labels_,
        'individual_distances': individual_distances,
        'train_files': train_files  # 각 카테고리별 train_files 정보도 저장
    }
    model_info_dict[category] = model_info



# 모든 카테고리에 대한 정보를 하나의 CSV 파일로 저장

for category, model_info in model_info_dict.items():
    latent_vectors = model_info['latent_vectors']
    kmeans_labels = model_info['kmeans_labels']
    individual_distances = model_info['individual_distances']
    train_files = model_info['train_files']

    for i in range(len(latent_vectors)):
        data_row = {
            'id': i,
            'image_path': train_files[i],  # 이 부분은 실제 train_files 경로에 맞게 수정해야 함
            'latent_vector': latent_vectors[i],
            'cluster_label': kmeans_labels[i],
            'cluster_center_distance': individual_distances[i],
            'model_category': category  # 모델 카테고리 정보 추가
        }
        all_data.append(data_row)
print(len(train_files))  # 이미지 파일의 개수
print(latent_vectors.shape[0])  # 잠재 벡터의 개수
print(len(kmeans.labels_))  # k-means 라벨의 개수
print(len(individual_distances))  # 군집 중심까지의 거리의 개수       
print(len(category)) 

df = pd.DataFrame(data_row)
df['latent_vector'] = df['latent_vector'].apply(lambda x: ','.join(map(str, x)))
csvsave_path = "../../9oz-project/csv/"
csv_file_path = os.path.join(csvsave_path, 'latent_vectors_with_all_info.csv')
df.to_csv(csv_file_path, index=False)
df.to_csv('latent_vectors_with_all_info.csv', index=False)



# 해시 테이블로 데이터 로딩
# 해시 테이블 로딩 함수 예시
csv_path = 'latent_vectors_with_all_info.csv'
def load_hash_table_from_csv(csv_path):
    hash_table = {}
    with open(csv_path, mode='r', encoding='utf-8') as file:
        csvFile = csv.DictReader(file)
        for lines in csvFile:
            unique_key = f"{lines['id']}_{lines['model_category']}"
            hash_table[unique_key] = {
                'image_path': lines['image_path'],
                'latent_vector': lines['latent_vector'],
                'cluster_label': lines['cluster_label'],
                'cluster_center_distance': lines['cluster_center_distance'],
                'model_category' : lines['model_category']
            }
    return hash_table



# # 1. 저장된 인코더 모델 불러오기
# encoder_model = load_model("encoder_vgg16.h5")

# # 2. 임의의 이미지에서 잠재 벡터 추출 (임의의 이미지가 img 변수에 있다고 가정)
# # 2. 이미지 경로에서 실제 이미지 로드
# img_path = "/content/drive/MyDrive/K-fashion/vector model/B_folder/AFA1CA801.jpg"
# img = Image.open(img_path).resize((32, 32))  # 이미지 로드 및 크기 조절
# img = np.array(img)  # 이미지를 NumPy 배열로 변환
# img = img / 255.0  # 정규화
# img = np.expand_dims(img, axis=0)  # 배치 차원 추가

# latent_vector = encoder_model.predict(img)

# # 3. CSV 파일 또는 해시 테이블에서 모든 잠재 벡터와 군집 라벨 불러오기
# df = pd.read_csv("latent_vectors_with_all_info.csv")

# # 잠재 벡터를 리스트로 변환
# df['latent_vector'] = df['latent_vector'].apply(lambda x: list(map(float, x.split(','))))

# # 4. 추출된 잠재 벡터와 가장 유사한 군집 찾기
# distances = pairwise_distances(latent_vector, np.stack(df['latent_vector'].to_numpy()))
# closest_cluster_label = df.loc[np.argmin(distances), 'cluster_label']

# # 5. 해당 군집 내에서 아이템들을 랭킹에 따라 정렬
# def rank_within_cluster(cluster_label, df):
#     same_cluster_items = df[df['cluster_label'] == cluster_label]
#     ranked_items = same_cluster_items.sort_values(by='cluster_center_distance')
#     return ranked_items

# ranked_items = rank_within_cluster(closest_cluster_label, df)

# # 6. 랭킹 결과를 JSON 파일로 저장
# def save_ranking_to_json(ranked_items, json_path):
#     ranked_image_paths = ranked_items['image_path'].tolist()
#     with open(json_path, 'w') as f:
#         json.dump(ranked_image_paths, f)

# save_ranking_to_json(ranked_items, json_path='ranked_items.json')