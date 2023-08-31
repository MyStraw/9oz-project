import base64

# 이미지 파일을 읽습니다.
with open("abc.jpg", "rb") as image_file:
    # 이미지를 Base64로 인코딩합니다.
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

# 이제 base64_image 변수를 Postman의 JSON Body에 넣을 수 있습니다.
