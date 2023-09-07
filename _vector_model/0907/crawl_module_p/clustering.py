from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import numpy as np
import pandas as pd

def perform_clustering(latent_vectors, image_files):
    # K-means 군집화
    n_clusters = 10  # 군집의 수
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(latent_vectors)
    
    # 각 데이터 포인트의 군집 중심까지의 거리 계산
    individual_distances = np.linalg.norm(latent_vectors - kmeans.cluster_centers_[kmeans.labels_], axis=1)
    
    # t-SNE 시각화
    tsne = TSNE(n_components=2, learning_rate=100, perplexity=30, random_state=0)
    latent_tsne = tsne.fit_transform(latent_vectors)
    
    # 테이블에 저장할 데이터 준비
    data = {
        'id': range(len(image_files)),
        'image_path': image_files,
        'latent_vector': list(latent_vectors),
        'cluster_label': kmeans.labels_,
        'cluster_center_distance': individual_distances,
        'tsne-2d-one': latent_tsne[:, 0],
        'tsne-2d-two': latent_tsne[:, 1]
    }
    
    # DataFrame 생성
    df = pd.DataFrame(data)
    
    # 잠재 벡터를 문자열로 변환 (CSV 저장을 위해)
    df['latent_vector'] = df['latent_vector'].apply(lambda x: ','.join(map(str, x)))
    
    return df
