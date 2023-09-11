from flask import Flask, request, jsonify, send_file
import base64
from PIL import Image
from io import BytesIO
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    image_data_base64 = request.json.get('image_name')
    image_data = base64.b64decode(image_data_base64)

    # 이미지 데이터를 PIL Image 객체로 변환
    image = Image.open(BytesIO(image_data))

    # AI 모델로 결과를 계산하는 코드 (예시)
    # 예를 들어, 이미지를 회전하는 것으로 대체
    image = image.rotate(45)

    # 이미지를 BytesIO 객체로 저장
    byte_io = BytesIO()
    image.save(byte_io, 'JPEG')

    # BytesIO 객체를 웹 브라우저로 전송
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
