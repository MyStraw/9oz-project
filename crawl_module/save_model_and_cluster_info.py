import json
import numpy as np  # numpy 추가
from tensorflow.keras.models import load_model

def save_model(autoencoder):
    autoencoder.save('final_autoencoder_model.h5')


def save_cluster_info_to_hash_table(cluster_labels, cluster_centers, latent_vectors, image_info_hash_table):
    for i, label in enumerate(cluster_labels):
        image_info_hash_table[i].update({
            'latent_vector': latent_vectors[i].tolist(),
            'cluster_label': int(label),
            'cluster_center': cluster_centers[label].tolist()
        })

def save_hash_table_to_disk(image_info_hash_table, filename='image_info.json'):
    with open(filename, 'w') as f:
        json.dump(image_info_hash_table, f)

# JSON 파일에서 데이터 로드
with open('cluster_labels.json', 'r') as f:
    cluster_labels = np.array(json.load(f))
with open('cluster_centers.json', 'r') as f:
    cluster_centers = np.array(json.load(f))
with open('latent_vectors.json', 'r') as f:
    latent_vectors = np.array(json.load(f))

if __name__ == "__main__":
    # 이미 해시테이블과 모델이 있다고 가정
    image_info_hash_table = {}  # 실제 해시테이블을 사용하세요.
    autoencoder = load_model('final_autoencoder_model.h5')  # 실제 모델을 로드하세요.

    save_model(autoencoder)
    save_cluster_info_to_hash_table(cluster_labels, cluster_centers, latent_vectors, image_info_hash_table)
    save_hash_table_to_disk(image_info_hash_table)
















# import pickle

# def save_cluster_info(cluster_labels, cluster_centers):
#     with open('cluster_info.pkl', 'wb') as f:
#         pickle.dump({'labels': cluster_labels, 'centers': cluster_centers}, f)

# # 해시테이블을 사용해 정보 저장
# def save_to_hash_table(cluster_labels, cluster_centers):
#     hash_table = {}
#     for i, label in enumerate(cluster_labels):
#         hash_table[label] = cluster_centers[i]
    
#     # 해시테이블을 파일 또는 DB에 저장
#     # ...
