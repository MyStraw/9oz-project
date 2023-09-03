# 군집화 정보를 해시테이블에 추가하는 함수
def update_hash_table_with_cluster_info(hash_table, cluster_labels, cluster_centers, latent_vectors):
    for i, label in enumerate(cluster_labels):
        hash_table[i].update({
            'cluster_label': label,
            'cluster_center': cluster_centers[label],
            'latent_vector': latent_vectors[i]
        })

# 예시 사용법
# 이미 해시테이블에 기본 정보가 들어가 있다고 가정
image_info_hash_table = {
    0: {'image_name': 'image_0.jpg', 'sale_url': 'url_0'},
    1: {'image_name': 'image_1.jpg', 'sale_url': 'url_1'},
    # ...
}

# 군집화 정보
cluster_labels = [0, 1, 0, 2, 1]  # 각 이미지의 군집 레이블
cluster_centers = [[0, 0], [1, 1], [2, 2]]  # 각 군집의 중심점
latent_vectors = [[0.1, 0.2], [1.1, 1.2], [0.2, 0.1], [2.1, 2.2], [1.2, 1.1]]  # 각 이미지의 잠재 벡터

# 해시테이블 업데이트
update_hash_table_with_cluster_info(image_info_hash_table, cluster_labels, cluster_centers, latent_vectors)