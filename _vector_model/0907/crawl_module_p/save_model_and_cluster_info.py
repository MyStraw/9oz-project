import csv

def save_to_csv_and_hash(df, csv_path='latent_vectors_with_all_info.csv'):
    # DataFrame을 CSV 파일로 저장
    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    # 해시 테이블로 데이터 로딩
    hash_table = {}
    with open(csv_path, mode='r', encoding='utf-8') as file:
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
    return hash_table
