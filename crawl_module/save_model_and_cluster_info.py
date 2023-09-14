import pandas as pd
import csv

def save_to_csv_and_hash(df, csv_path='latent_vectors_with_all_info.csv'):
    try:
        # 기존 CSV 파일을 불러옴
        existing_df = pd.read_csv(csv_path, encoding='cp949')
    except FileNotFoundError:
        # 파일이 없으면 새로 저장
        df.to_csv(csv_path, index=False, encoding='cp949')
        return

    # 기존 DataFrame과 새로운 DataFrame을 결합
    combined_df = pd.concat([existing_df, df], ignore_index=True)
    
     # 중복된 행 제거
    unique_df = combined_df.drop_duplicates(subset=['image_path', 'latent_vector', 'cluster_label', 'cluster_center_distance', 'mainclass'])
    
    # 다시 CSV 파일로 저장
    # combined_df.to_csv(csv_path, index=False, encoding='cp949')
    unique_df.to_csv(csv_path, index=False, encoding='cp949')
    
    
    # 해시 테이블로 데이터 로딩
    hash_table = {}
    with open(csv_path, mode='r', encoding='cp949') as file:
        csvFile = csv.DictReader(file)
        for lines in csvFile:
            hash_table[lines['id']] = {
                'image_path': lines['image_path'],
                'latent_vector': lines['latent_vector'],
                'cluster_label': lines['cluster_label'],
                'cluster_center_distance': lines['cluster_center_distance'],
                'mainclass': lines['mainclass']  # mainclass 추가
            }
    return hash_table
