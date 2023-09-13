from flask import Flask, request, jsonify, send_from_directory
from clustering import perform_clustering
from autoencoder_model import Autoencoder
from flask_cors import CORS
from save_model_and_cluster_info import save_to_csv_and_hash
from autoencoder_model import Autoencoder
import os
from crawl import QueenitCrawling
from flask import Flask, request, jsonify
from service_logic import predict_similar_items  # 위에서 작성한 서비스 로직을 import



app = Flask(__name__)
CORS(app)
@app.route('/crawl', methods=['POST'])
def crawl():
    # # # Step 1: 크롤링 작업   
    # url = 'https://web.queenit.kr/'
    # path_input = 'c:/queenit/'
    
    # repeat = 50    
    # subfolders = ['top','onepiece','bottom','outer', 'skirt']
    
    # for i in subfolders:
    #      QueenitCrawling.queenit_crawling(url, path_input, i , repeat)
    
    # # 크롤링 코드 실행
    # QueenitCrawling.queenit_crawling(url, path_input, repeat, 'top')
    # QueenitCrawling.queenit_crawling(url, path_input, repeat, 'onepiece')
    # QueenitCrawling.queenit_crawling(url, path_input, repeat, 'bottom')
    # QueenitCrawling.queenit_crawling(url, path_input, repeat, 'outer')
    # QueenitCrawling.queenit_crawling(url, path_input, repeat, 'skirt')    
   

    # Step 2: 각 폴더별로 반복문 돌면서 각자 처리후 csv에 저장
    subfolders = ['outer', 'onepiece', 'skirt', 'bottom', 'top']
    for subfolder in subfolders:
        image_folder = f'C:/queenit/{subfolder}'    
        image_files = [f for f in os.listdir(image_folder) if not f.endswith('.csv')]
        #image_files = os.listdir(image_folder)


        # Step 3: 잠재 벡터 추출 및 모델 저장
        
        # 모델 빌드 (인코더 모델)
        autoencoder = Autoencoder()    
        autoencoder.build_model()
        latent_vectors = autoencoder.extract_latent_vectors(subfolder)
        
        if latent_vectors is None or len(latent_vectors) == 0:
            print("Error: Latent vectors are not properly generated.")
            return jsonify({'status': 'failure'})
        
        # Step 4: 군집화와 군집 중심 거리 계산    
        df = perform_clustering(latent_vectors, image_files, subfolder)
        
        # Step 5: CSV 파일 저장    
        save_to_csv_and_hash(df)    
    return jsonify({'status': 'success'})


@app.route('/predict', methods=['POST'])
def predict():
    # 클라이언트로부터 base64 이미지 받기
    data = request.get_json()   
    
    # "mainclass" 값 출력
    mainclass_value = data.get('mainclass')  # 'mainclass' 키가 없을 경우 None을 반환
    semiclass_value = data.get('semiclass')
    print(f"mainclass: {mainclass_value}")
    print(f"semiclass : {semiclass_value}")
    base64_image = data['image_data']
    
    # 비슷한 아이템 찾기
    print(f"mainclass_value: {mainclass_value}, semiclass_value: {semiclass_value}")
    similar_item_paths = predict_similar_items(base64_image, mainclass_value, semiclass_value)
    
    # 이미지 파일 경로를 URL로 변환
    server_ip = "10.125.121.185"    
    if mainclass_value == 'bottom' and semiclass_value == 'skirt':
        mainclass_value = 'skirt'        
        
    similar_item_urls = [f"http://{server_ip}:5000/predicted/{mainclass_value}/{path}" for path in similar_item_paths]
    
    return jsonify({'similar_item_urls': similar_item_urls})

# 이미지 url 만들어서 뿌리기
@app.route('/predicted/<mainclass>/<filename>', methods=['GET'])
def serve_image(mainclass, filename):
    return send_from_directory(f'c:/queenit/{mainclass}', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

