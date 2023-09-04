from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
from autoencoder_model import build_advanced_autoencoder
import matplotlib.pyplot as plt 
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image  # image 추가
import os  # os 추가
import json  # json 라이브러리 추가
from load_and_process_images import load_images  # 이미지 로딩 함수 추가

def load_images(folder_path="c:/queenit"):
    image_files = os.listdir(folder_path)
    images = [image.load_img(os.path.join(folder_path, img_file), target_size=(28, 28)) for img_file in image_files]
    return np.array([image.img_to_array(img) for img in images])
    # 이 부분은 실제 이미지 로드 로직에 따라 다릅니다.
    # 예를 들어, load_images_from_folder 함수를 사용할 수 있습니다.
    pass
# 오토인코더 모델과 인코더 모델 빌드
autoencoder = load_model('final_autoencoder_model.h5')
encoder_model = Model(inputs=autoencoder.input, outputs=autoencoder.get_layer('encoder_output').output)

# 이미지 데이터 로드 (이미지 로드 로직이 있다고 가정)
input_images = load_images()  # 이 부분은 실제 이미지 로드 로직에 따라 다릅니다.

# 잠재 벡터 추출
latent_vectors = encoder_model.predict(input_images)

def find_optimal_clusters(data, max_k):
    iters = range(2, max_k+1, 2)
    
    sse = []
    for k in iters:
        sse.append(KMeans(n_clusters=k, random_state=20).fit(data).inertia_)
        
    f, ax = plt.subplots(1, 1)
    ax.plot(iters, sse, marker='o')
    ax.set_xlabel('Cluster Centers')
    ax.set_xticks(iters)
    ax.set_xticklabels(iters)
    ax.set_ylabel('SSE')
    ax.set_title('SSE by Cluster Center Plot')
    
def perform_clustering(encoded_imgs, n_clusters=10):
    kmeans = KMeans(n_clusters=n_clusters, random_state=20)
    cluster_labels = kmeans.fit_predict(encoded_imgs)
    
    cluster_to_images = {}
    for i, label in enumerate(cluster_labels):
        if label not in cluster_to_images:
            cluster_to_images[label] = []
        cluster_to_images[label].append(i)
        
    return cluster_to_images, kmeans.cluster_centers_

# 군집화 수행
cluster_to_images, cluster_centers = perform_clustering(latent_vectors)
# 군집화 결과를 JSON으로 저장
cluster_labels = [label for images in cluster_to_images.values() for label in [key] * len(images)]
with open('cluster_labels.json', 'w') as f:
    json.dump(cluster_labels, f)
with open('cluster_centers.json', 'w') as f:
    json.dump(cluster_centers.tolist(), f)
with open('latent_vectors.json', 'w') as f:
    json.dump(latent_vectors.tolist(), f)






# from sklearn.cluster import KMeans
# import tensorflow as tf
# import numpy as np

# # 이미지 로드 함수 (실제 구현 필요)
# def load_images_from_folder(folder_path):
#     return np.array([])

# # K-Means 클러스터링 및 잠재 벡터 추출
# def perform_clustering(folder_path):
#     images = load_images_from_folder(folder_path)
#     autoencoder = tf.keras.models.load_model('best_autoencoder_model.h5')
#     latent_vectors = autoencoder.predict(images)

#     kmeans = KMeans(n_clusters=3)
#     kmeans.fit(latent_vectors)
#     cluster_labels = kmeans.labels_
#     cluster_centers = kmeans.cluster_centers_

#     return cluster_labels, cluster_centers

