from PIL import Image
import numpy as np
import os


# def load_images_from_folder(folder_path):
#     image_files = os.listdir(folder_path)
#     images = [image.load_img(os.path.join(folder_path, img_file), target_size=(28, 28)) for img_file in image_files]
#     return np.array([image.img_to_array(img) for img in images])

def load_and_process_single_image(image_path):
    # 파일 확장자 확인
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    file_extension = os.path.splitext(image_path)[1]
    if file_extension.lower() not in valid_extensions:
        print(f"Unsupported file extension: {file_extension}")
        return None
    
    if os.path.isdir(image_path):
        return None  # 디렉토리면 None 반환
    
    img = Image.open(image_path)
    img = img.resize((32, 32))  # 모델의 입력 크기에 맞춰 이미지 크기를 조정합니다.
    img_array = np.array(img)
    
    if len(img_array.shape) == 2:
        img_array = np.expand_dims(img_array, axis=-1)
        
    if img_array.shape[2] == 4:  # RGBA일 경우 RGB로 변환
        img_array = img_array[:, :, :3]
    
    img_array = img_array.astype('float32') / 255.0  # Normalization
    
    return img_array