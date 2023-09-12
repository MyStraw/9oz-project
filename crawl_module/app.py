from flask import Flask, request, jsonify, send_from_directory
from clustering import perform_clustering
from some_crawling_library import QueenitCrawler
from autoencoder_model import Autoencoder
from flask_cors import CORS
from save_model_and_cluster_info import save_to_csv_and_hash
from autoencoder_model import Autoencoder
import os

from flask import Flask, request, jsonify
from service_logic import predict_similar_items  # 위에서 작성한 서비스 로직을 import

app = Flask(__name__)
CORS(app)
@app.route('/crawl', methods=['POST'])
def crawl():
    # # Step 1: 크롤링 작업   
    
    # crawler = QueenitCrawler(save_path='C:/queenit')
    # crawler.crawl_images()

    # Step 2: 이미지 저장 (크롤링 함수 내부에서 처리될 수도 있음)
    # 이미지가 C:/queenit에 저장되도록 코드 작성
    image_folder = 'C:/queenit'  # 크롤링된 이미지가 저장된 폴더
    image_files = os.listdir(image_folder)

    # Step 3: 잠재 벡터 추출 및 모델 저장
    
    # 모델 빌드 (인코더 모델)
    autoencoder = Autoencoder()    
    autoencoder.build_model()
    latent_vectors = autoencoder.extract_latent_vectors()
    
    if latent_vectors is None or len(latent_vectors) == 0:
        print("Error: Latent vectors are not properly generated.")
        return jsonify({'status': 'failure'})
    
    # Step 4: 군집화와 군집 중심 거리 계산    
    df = perform_clustering(latent_vectors, image_files)
    
    # Step 5: CSV 파일 저장    
    save_to_csv_and_hash(df)    
    return jsonify({'status': 'success'})


@app.route('/predict', methods=['POST'])
def predict():
    # 클라이언트로부터 base64 이미지 받기
    data = request.get_json()   
    
    # "mainclass" 값 출력
    mainclass_value = data.get('mainclass', None)  # 'mainclass' 키가 없을 경우 None을 반환
    semiclass_value = data.get('semiclass', None)
    print(f"mainclass: {mainclass_value}")
    print(f"semiclass : {semiclass_value}")
    base64_image = data['image_data']
    # 비슷한 아이템 찾기
    similar_item_paths = predict_similar_items(base64_image, mainclass_value)
    
    # 이미지 파일 경로를 URL로 변환
    server_ip = "10.125.121.185"
    similar_item_urls = [f"http://{server_ip}:5000/predicted/{path}" for path in similar_item_paths]
    
    return jsonify({'similar_item_urls': similar_item_urls})

# 이미지 url 만들어서 뿌리기
@app.route('/predicted/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory('c:/queenit/', filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

