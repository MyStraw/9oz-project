from load_and_process_images import load_and_process_images
from autoencoder_model import build_advanced_autoencoder, load_autoencoder
from clustering import find_optimal_clusters, perform_clustering
from app import image_info_hash_table

def process_and_cluster_images(folder_path = "c:/queenit", image_info_hash_table={}):
    # Step 1: 이미지 로딩 및 전처리
    images = load_and_process_images(folder_path)
    
    # Step 2: 오토인코더 모델 로딩
    autoencoder, encoder_model = load_autoencoder('final_autoencoder_model.h5')
    
    # Step 3: 잠재 벡터 추출
    latent_vectors = encoder_model.predict(images)
    
    # Step 4: 클러스터링
    cluster_to_images, cluster_centers = perform_clustering(latent_vectors)
    
    # Step 5: 해시테이블에 군집화 정보와 잠재 벡터 저장
    for idx, info in image_info_hash_table.items():
        info['latent_vector'] = latent_vectors[idx].tolist()
        info['cluster_label'] = cluster_to_images[idx]
        info['cluster_center'] = cluster_centers[cluster_to_images[idx]].tolist()











# from autoencoder_model import build_advanced_autoencoder
# from clustering import perform_clustering
# from save_model_and_cluster_info import save_cluster_info
# from hash_table import save_image_info_to_hash_table
# from load_and_process_images import load_images_from_folder

# def process_and_cluster_images(image_folder_path = "c:/queenit-img", image_info_hash_table):
#     # 이미지 로드
#     images = load_images_from_folder(image_folder_path)
    
#     # 오토인코더 모델 생성 및 훈련
#     autoencoder = build_advanced_autoencoder()
#     # 모델 훈련 코드 (필요한 경우)
#     # autoencoder.fit( ... )
    
#     # 잠재 벡터 추출 및 군집화
#     cluster_labels, cluster_centers = perform_clustering(images)
    
#     # 군집 정보 저장
#     save_cluster_info(cluster_labels, cluster_centers)
    
#     # 이미지 정보 및 군집 레이블 해시테이블에 저장
#     for idx, label in enumerate(cluster_labels):
#         image_info_hash_table[idx]['cluster_label'] = label
    
#     # 해시테이블 저장
#     save_image_info_to_hash_table(image_info_hash_table)
