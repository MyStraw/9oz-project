from flask import Flask, request, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)
#CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
@app.route('/predict', methods=['POST'])
def predict():
    image_data_base64 = request.json.get('image_data')
    image_data = base64.b64decode(image_data_base64)

    # AI 모델로 결과를 계산하는 코드 (예시)
    result = "통신보안"

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
