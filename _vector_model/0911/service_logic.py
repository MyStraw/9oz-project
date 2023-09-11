
from tensorflow.keras.models import load_model

from PIL import Image
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
import base64
import io

# 미리 훈련된 인코더 모델 불러오기
encoder_model = load_model("encoder_model.h5")

# CSV 파일 불러오기
df = pd.read_csv("latent_vectors_with_all_info.csv")
df['latent_vector'] = df['latent_vector'].apply(lambda x: list(map(float, x.split(','))))

def predict_similar_items(base64_image, mainclass_value):
    # base64 이미지 디코딩 및 전처리
    image = Image.open(io.BytesIO(base64.b64decode(base64_image))).resize((32, 32))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    
    # 잠재 벡터 추출
    latent_vector = encoder_model.predict(image)
    
    # 가장 가까운 군집 찾기
    distances = pairwise_distances(latent_vector, np.stack(df['latent_vector'].to_numpy()))
    closest_cluster_label = df.loc[np.argmin(distances), 'cluster_label']
    
    # 군집 내 랭킹 생성
    same_cluster_items = df[df['cluster_label'] == closest_cluster_label]
    ranked_items = same_cluster_items.sort_values(by='cluster_center_distance')
    
    # 결과 반환 (이미지 경로 목록)
    return ranked_items['image_path'].tolist()[:10]

