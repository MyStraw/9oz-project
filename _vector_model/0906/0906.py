import os
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
from tensorflow.keras.layers import UpSampling2D, Conv2D, Dense, Flatten, Reshape
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.applications import VGG16
import json


# 원본 폴더와 대상 폴더 경로 설정
source_folder = 'c:/queenit/'

# 대상 폴더의 이미지 리스트 생성
image_files = os.listdir(source_folder)

# 이미지 파일을 랜덤하게 train과 test로 분할
train_files, test_files = train_test_split(image_files, test_size=0.2, random_state=42)

image_size = (32, 32)

# 이미지 데이터를 불러와서 NumPy 배열로 변환
train_images = np.array([np.array(Image.open(os.path.join(source_folder, file)).resize(image_size)) for file in train_files])
test_images = np.array([np.array(Image.open(os.path.join(source_folder, file)).resize(image_size)) for file in test_files])

# 데이터 정규화
train_images = train_images / 255.0
test_images = test_images / 255.0

# TensorFlow 변수에 할당 (여기서는 MNIST 예제와 유사하게 변수명을 사용)
train_X, train_Y = train_images, None  # train_Y는 필요에 따라 레이블을 할당
test_X, test_Y = test_images, None  # test_Y는 필요에 따라 레이블을 할당

print(train_X.shape)
print(test_X.shape)

#test1


# VGG16 모델
vgg16 = VGG16(weights='imagenet', include_top=False, input_shape=(32, 32, 3))
vgg16.trainable = False  # Freeze the VGG16 layers

# 오토인코더 모델
autoencoder = Sequential()

# 인코더 부분 (VGG16)
autoencoder.add(vgg16)

# Flatten과 Dense
autoencoder.add(Flatten())
autoencoder.add(Dense(64, activation='relu'))

# 디코더 부분
autoencoder.add(Dense(8 * 8 * 128, activation='relu'))
autoencoder.add(Reshape((8, 8, 128)))
autoencoder.add(UpSampling2D((2, 2)))
autoencoder.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
autoencoder.add(UpSampling2D((2, 2)))
autoencoder.add(Conv2D(3, (3, 3), activation='sigmoid', padding='same'))

# 모델 컴파일
input_img = autoencoder.input  # input_img 변수 추가
decoded = autoencoder.layers[-1].output  # decoded 변수 추가
autoencoder = Model(input_img, decoded)
autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy', metrics=['mse'])

# 모델 요약
autoencoder.summary()

# Train the model (모델학습, vgg16 기반 모델 학습하기.)
history = autoencoder.fit(
    train_X, train_X,  # 입력과 출력이 같습니다.
    epochs=50,
    batch_size=128,
    shuffle=True,
    validation_data=(test_X, test_X)
)

# 학습 이력에서 손실과 MSE를 가져옵니다.
train_loss = history.history['loss']
val_loss = history.history['val_loss']
train_mse = history.history['mse']
val_mse = history.history['val_mse']

# 학습 과정을 출력
print("Train Loss: ", train_loss)
print("Validation Loss: ", val_loss)
print("Train MSE: ", train_mse)
print("Validation MSE: ", val_mse)

# 인코딩 및 디코딩까지 하는 모델. 난 안쓸거.
autoencoder.save("autoencoder_vgg16.h5")



# 잠재 벡터 추출 모델 저장 (인코더 부분만)
encoder_model = Model(inputs=autoencoder.input, outputs=autoencoder.layers[-6].output)
encoder_model.save("encoder_vgg16.h5")  # 인코더 모델만 저장

# 잠재 벡터 추출
latent_vectors = encoder_model.predict(train_X)

# 테이블에 저장할 데이터 준비
data = {
    'id': range(len(train_files)),
    'image_path': train_files,
    'latent_vector': list(latent_vectors),
    # 'cluster_label': ...,  # 군집화 라벨, 필요하면 추가
    # 'cluster_center_distance': ... # 군집화 중심 거리, 필요하면 추가
}

# DataFrame 생성
df = pd.DataFrame(data)
df['latent_vector'] = df['latent_vector'].apply(lambda x: ','.join(map(str, x)))

# CSV 파일로 저장
df.to_csv('latent_vectors.csv', index=False)

print("CSV 파일 만들어짐.")

#위의 3개 합친거



# 잠재 벡터 추출 모델 저장 (인코더 부분만)
encoder_model = Model(inputs=autoencoder.input, outputs=autoencoder.layers[-6].output)
encoder_model.save("encoder_vgg16.h5")  # 인코더 모델만 저장

# 잠재 벡터 추출
latent_vectors = encoder_model.predict(train_X)

# K-means 군집화
n_clusters = 10  # 군집의 수
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(latent_vectors)

# 각 데이터 포인트의 군집 중심까지의 거리 계산
individual_distances = np.linalg.norm(latent_vectors - kmeans.cluster_centers_[kmeans.labels_], axis=1)

# DataFrame 생성 전에 길이 확인
assert len(train_files) == latent_vectors.shape[0] == len(kmeans.labels_) == len(individual_distances)



# 테이블에 저장할 데이터 준비
data = {
    'id': range(len(train_files)),
    'image_path': train_files,
    'latent_vector': list(latent_vectors),
    'cluster_label': kmeans.labels_,
    'cluster_center_distance': individual_distances,  # 수정된 부분
    'tsne-2d-one': latent_tsne[:, 0],
    'tsne-2d-two': latent_tsne[:, 1]
}
print(len(train_files))  # 이미지 파일의 개수
print(latent_vectors.shape[0])  # 잠재 벡터의 개수
print(len(kmeans.labels_))  # k-means 라벨의 개수
print(len(individual_distances))  # 군집 중심까지의 거리의 개수


# DataFrame 생성
df = pd.DataFrame(data)

# 잠재 벡터를 문자열로 변환 (CSV 저장을 위해)
df['latent_vector'] = df['latent_vector'].apply(lambda x: ','.join(map(str, x)))

# DataFrame을 CSV 파일로 저장
csv_path = 'latent_vectors_with_all_info.csv'
df.to_csv(csv_path, index=False)

# 해시 테이블로 데이터 로딩
hash_table = {}
with open(csv_path, mode ='r')as file:
    csvFile = csv.DictReader(file)
    for lines in csvFile:
        hash_table[lines['id']] = {
            'image_path': lines['image_path'],
            'latent_vector': lines['latent_vector'],
            'cluster_label': lines['cluster_label'],
            'cluster_center_distance': lines['cluster_center_distance'],
            'tsne-2d-one': lines['tsne-2d-one'],
            'tsne-2d-two': lines['tsne-2d-two'],
        }

# 1. 저장된 인코더 모델 불러오기
encoder_model = load_model("encoder_vgg16.h5")

# 2. 임의의 이미지에서 잠재 벡터 추출 (임의의 이미지가 img 변수에 있다고 가정)
# 2. 이미지 경로에서 실제 이미지 로드
img_path = "/content/drive/MyDrive/K-fashion/vector model/B_folder/AFA1CA801.jpg"
img = Image.open(img_path).resize((32, 32))  # 이미지 로드 및 크기 조절
img = np.array(img)  # 이미지를 NumPy 배열로 변환
img = img / 255.0  # 정규화
img = np.expand_dims(img, axis=0)  # 배치 차원 추가

latent_vector = encoder_model.predict(img)

# 3. CSV 파일 또는 해시 테이블에서 모든 잠재 벡터와 군집 라벨 불러오기
df = pd.read_csv("latent_vectors_with_all_info.csv")

# 잠재 벡터를 리스트로 변환
df['latent_vector'] = df['latent_vector'].apply(lambda x: list(map(float, x.split(','))))

# 4. 추출된 잠재 벡터와 가장 유사한 군집 찾기
distances = pairwise_distances(latent_vector, np.stack(df['latent_vector'].to_numpy()))
closest_cluster_label = df.loc[np.argmin(distances), 'cluster_label']

# 5. 해당 군집 내에서 아이템들을 랭킹에 따라 정렬
def rank_within_cluster(cluster_label, df):
    same_cluster_items = df[df['cluster_label'] == cluster_label]
    ranked_items = same_cluster_items.sort_values(by='cluster_center_distance')
    return ranked_items

ranked_items = rank_within_cluster(closest_cluster_label, df)

# 6. 랭킹 결과를 JSON 파일로 저장
def save_ranking_to_json(ranked_items, json_path):
    ranked_image_paths = ranked_items['image_path'].tolist()
    with open(json_path, 'w') as f:
        json.dump(ranked_image_paths, f)

save_ranking_to_json(ranked_items, json_path='ranked_items.json')