
from tensorflow.keras.models import load_model

from PIL import Image
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
import base64
import io
from rembg import remove
import os

# 미리 훈련된 인코더 모델 불러오기
encoder_model = load_model("encoder_model.h5")

# CSV 파일 불러오기
df = pd.read_csv("latent_vectors_with_all_info.csv",  encoding='cp949')
df['latent_vector'] = df['latent_vector'].apply(lambda x: list(map(float, x.split(','))))



def predict_similar_items(base64_image, mainclass_value):
    # base64 이미지 디코딩 및 전처리
    image = Image.open(io.BytesIO(base64.b64decode(base64_image))).resize((416, 416))
    
    # 배경 제거 (rembg 사용)
    image_array = np.array(image)
    if image_array.shape[2] == 4:  # RGBA일 경우 RGB로 변환
        image_array = image_array[:, :, :3]
    image_array = (image_array * 255).astype(np.uint8)
    image = Image.fromarray(image_array)
    output_image = remove(image)  # 배경 제거
    
    # RGBA to RGB (배경 제거 후 채널이 4개일 수 있음)
    if output_image.mode == 'RGBA':
        output_image = output_image.convert('RGB')
        
    # 재변환 및 정규화
    output_image = np.array(output_image) / 255.0
    output_image = np.expand_dims(output_image, axis=0)
    
    # 배경 제거된 이미지 저장
    save_path = "background_removed_images"  # 저장할 디렉토리 설정
    if not os.path.exists(save_path):
        os.makedirs(save_path)  # 디렉토리 없으면 생성
    save_image_path = os.path.join(save_path, "background_removed.png")  # 이미지 저장 경로
    
    output_image_pil = Image.fromarray((output_image[0] * 255).astype(np.uint8))  # Numpy array to PIL Image
    output_image_pil.save(save_image_path)  # 이미지 저장
    
    # 잠재 벡터 추출
    latent_vector = encoder_model.predict(output_image)
    
    
    # image = np.array(image) / 255.0
    # image = np.expand_dims(image, axis=0)
    
    # # 잠재 벡터 추출
    # latent_vector = encoder_model.predict(image)
    
    # 가장 가까운 군집 찾기
    distances = pairwise_distances(latent_vector, np.stack(df['latent_vector'].to_numpy()))
    closest_cluster_label = df.loc[np.argmin(distances), 'cluster_label']
    
    # 군집 내 랭킹 생성
    same_cluster_items = df[df['cluster_label'] == closest_cluster_label]
    ranked_items = same_cluster_items.sort_values(by='cluster_center_distance')
    
   

    
    # # 유사도 기반 랭킹
    # all_distances = pairwise_distances(latent_vector, np.stack(df['latent_vector'].to_numpy()))
    # ranked_items_by_distance = df.loc[np.argsort(all_distances.flatten())]
    
    # cluster_center_distance 값이 1 미만인 이미지만 선택
    filtered_items = ranked_items[ranked_items['cluster_center_distance'] < 1]
    
    # 결과 반환 (이미지 경로 목록, 10개 이내)
    return filtered_items['image_path'].tolist()[:5]
    
    
    
    # 결과 반환 (이미지 경로 목록)
    return ranked_items_by_distance['image_path'].tolist()[:10]
    
     # 결과 반환 (이미지 경로 목록)
    return ranked_items['image_path'].tolist()[:10]

    
    
    
    # 결과 반환 (이미지 경로 목록)
    return ranked_items_by_distance['image_path'].tolist()[:10]
    
     # 결과 반환 (이미지 경로 목록)
    return ranked_items['image_path'].tolist()[:10]
