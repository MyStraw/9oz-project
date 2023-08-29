from flask import Flask, request, jsonify
import pickle  # 모델을 로드하기 위해 사용

app = Flask(__name__)

# 모델 로딩
with open('your_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # JSON 데이터를 파싱
    input_data = data['input']
    
    # 모델 실행
    output = model.predict(input_data)
    
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(port=5000)
