from flask import Flask, request, jsonify, send_from_directory
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import os

app = Flask(__name__)

# 모델 로딩
encoder = load_model('path_to_encoder_model')  # Encoder 모델의 경로
kmeans_A = KMeans(n_clusters=15)  # A 폴더의 최적 k 값
kmeans_B = KMeans(n_clusters=12)  # B 폴더의 최적 k 값

# 이미지를 잠재 벡터로 변환하는 함수
def image_to_latent_vector(image):
    image = image.resize((128, 128))
    image_array = np.array([img_to_array(image)])
    image_array = image_array.astype('float32') / 255.
    latent_vector = encoder.predict(image_array)
    return latent_vector.reshape((latent_vector.shape[0], -1))

@app.route('/find_similar', methods=['POST'])
def find_similar():
    # 이미지 업로드
    image_file = request.files['image']
    image = Image.open(image_file)

    # 이미지를 잠재 벡터로 변환
    latent_vector = image_to_latent_vector(image)

    # 가장 가까운 군집 찾기
    distances_to_B_clusters = np.linalg.norm(kmeans_B.cluster_centers_ - latent_vector, axis=1)
    closest_B_cluster = np.argmin(distances_to_B_clusters)

    # 가장 가까운 군집에 속한 이미지의 파일명 찾기
    similar_B_indices = np.where(B_cluster_labels == closest_B_cluster)[0]
    similar_B_filenames = [B_image_files[idx] for idx in similar_B_indices]

    return jsonify({'similar_products': similar_B_filenames})

if __name__ == '__main__':
    app.run(port=5000)
