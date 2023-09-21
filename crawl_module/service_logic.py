
from tensorflow.keras.models import load_model

from PIL import Image
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
import base64
import io
from rembg import remove
import os

# # 미리 훈련된 인코더 모델 불러오기
# encoder_model = load_model("encoder_model.h5")

# # CSV 파일 불러오기
# df = pd.read_csv("latent_vectors_with_all_info.csv",  encoding='cp949')
# df['latent_vector'] = df['latent_vector'].apply(lambda x: list(map(float, x.split(','))))



def predict_similar_items(base64_image, mainclass_value, semiclass_value):
    
    # 미리 훈련된 인코더 모델 불러오기
    encoder_model = load_model("encoder_model.h5")

    # CSV 파일 불러오기
    df = pd.read_csv("latent_vectors_with_all_info.csv",  encoding='cp949')
    df['latent_vector'] = df['latent_vector'].apply(lambda x: list(map(float, x.split(','))))
    
    
    
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
    
    if mainclass_value == 'bottom' and semiclass_value == 'skirt':
        filtered_df = df[df['mainclass'] == 'skirt']
    else:
        filtered_df = df[df['mainclass'] == mainclass_value]
        
     # DataFrame 비어있는지 확인
    if filtered_df.empty:
        print("Filtered DataFrame is empty")
        return []    
    # 인덱스 재설정
    filtered_df.reset_index(drop=True, inplace=True)
 
 
    # # 모든 잠재 벡터와의 거리 계산
    # all_distances = pairwise_distances(
    #     latent_vector, np.stack(filtered_df['latent_vector'].to_numpy())
    # ).flatten()

    # # 거리를 기반으로 랭킹 적용
    # ranked_items = filtered_df.loc[np.argsort(all_distances)]

    # # 결과 반환 (이미지 경로 목록, 5개 이내)
    # return ranked_items['image_path'].tolist()[:5]
 
 
    
    # 가장 가까운 군집 찾기
    distances = pairwise_distances(latent_vector, np.stack(filtered_df['latent_vector'].to_numpy()))
    closest_cluster_label = filtered_df.loc[np.argmin(distances), 'cluster_label']
    
    # 군집 내 랭킹 생성
    same_cluster_items = filtered_df[filtered_df['cluster_label'] == closest_cluster_label]
    #ranked_items = same_cluster_items.sort_values(by='cluster_center_distance')  

    
    # # 유사도 기반 랭킹
    # all_distances = pairwise_distances(latent_vector, np.stack(filtered_df['latent_vector'].to_numpy()))
    # ranked_items_by_distance = filtered_df.loc[np.argsort(all_distances.flatten())]
    
    # 수정된 부분: 군집 내에서의 상대적 가까움을 기준으로 랭킹 매기기
    same_cluster_items['relative_distance'] = pairwise_distances(
        latent_vector, np.stack(same_cluster_items['latent_vector'].to_numpy())
    ).flatten()
    ranked_items = same_cluster_items.sort_values(by='relative_distance')  
    
    
    # cluster_center_distance 값이 1 미만인 이미지만 선택
    # filtered_items = ranked_items[ranked_items['cluster_center_distance'] < 1]
    
    # # 상대거리 1미만 선택
    # filtered_items = ranked_items[ranked_items['relative_distance'] < 1]
    
    # 결과 반환 (이미지 경로 목록, 5개 이내)
    #return ranked_items['image_path'].tolist()[4:9]
    return ranked_items['image_path'].tolist()[4:9]
    
    # # cluster_center_distance 값이 1 미만인 이미지만 선택
    # filtered_items = ranked_items[ranked_items['cluster_center_distance'] < 1.5]
    
    # # 결과 반환 (이미지 경로 목록, 5개 이내)
    # return filtered_items['image_path'].tolist()[:5]    
