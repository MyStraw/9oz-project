from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import os
from process_and_cluster_images import process_and_cluster_images
from flask_cors import CORS

app = Flask(__name__)

# 해시테이블로 이미지 정보 저장
image_info_hash_table = {}

CORS(app)
@app.route('/crawl_images', methods=['POST'])
def crawl_images():
    # 크롤링 로직
    url = "https://web.queenit.kr/"  # '퀸잇' 웹사이트 주소
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
      
    
    # 이미지 URL과 판매 URL을 파싱
    image_elements = soup.select("image_selector")  # 실제 HTML 구조에 맞게 수정 필요
    
    
    # 이미지 저장 경로
    save_path = "C:/queenin-img/"
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    
    for idx, element in enumerate(image_elements):
        img_url = element.get('src')
        sale_url = element.get('href')
        
        img_data = requests.get(img_url).content
        img_filename = f"image_{idx}.jpg"
        
        with open(os.path.join(save_path, img_filename), 'wb') as handler:
            handler.write(img_data)
        
        # 해시테이블에 이미지 정보 저장
        image_info_hash_table[idx] = {'image_name': img_filename, 'sale_url': sale_url}
    
    # 여기서 이미지 처리 및 군집화 함수 호출 (아래에 구현)
    process_and_cluster_images(save_path, image_info_hash_table)
    
    return "Crawling and processing completed."
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')