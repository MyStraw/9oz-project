import os
from PIL import Image

# A 폴더와 B 폴더 경로 설정
A_folder_path = "A_folder/"
B_folder_path = "B_folder/"

# 폴더에서 이미지 파일 목록 불러오기
A_image_files = [f for f in os.listdir(A_folder_path) if f.endswith('.jpg') or f.endswith('.png')]
B_image_files = [f for f in os.listdir(B_folder_path) if f.endswith('.jpg') or f.endswith('.png')]

# 이미지 불러오기 (예시로 A 폴더의 첫 번째 이미지)
example_A_image = Image.open(os.path.join(A_folder_path, A_image_files[0]))

# 이미지 확인 (옵션)
example_A_image.show()

# 리사이징할 이미지의 크기 설정
resize_shape = (128, 128)

# A 폴더의 모든 이미지 리사이징
A_images_resized = [Image.open(os.path.join(A_folder_path, f)).resize(resize_shape) for f in A_image_files]

# B 폴더의 모든 이미지 리사이징
B_images_resized = [Image.open(os.path.join(B_folder_path, f)).resize(resize_shape) for f in B_image_files]
