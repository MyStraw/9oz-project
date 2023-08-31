from flask import Flask, request, jsonify
import pickle  # 모델을 로드하기 위해 사용

app = Flask(__name__)



@app.route('/predict', methods=['POST'])
def predict():
    #data = request.json  # JSON 데이터를 파싱
    image_file = request.files['image']
  
    
    # # 모델 실행
    # output = model.predict(input_data)
    
    return jsonify({'similar_images': similar_image_list})
   
if __name__ == '__main__':
    app.run(port=5000)
