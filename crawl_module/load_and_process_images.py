# from tensorflow.keras.preprocessing import image
# import numpy as np
# import os


from PIL import Image
import numpy as np
import os


# def load_images_from_folder(folder_path):
#     image_files = os.listdir(folder_path)
#     images = [image.load_img(os.path.join(folder_path, img_file), target_size=(28, 28)) for img_file in image_files]
#     return np.array([image.img_to_array(img) for img in images])

def load_and_process_images(image_folder):
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    images = []
    
    for image_file in image_files:
        img = Image.open(os.path.join(image_folder, image_file))
        img = img.resize((28, 28))  # 모델의 입력 크기에 맞춰 이미지 크기를 조정
        img_array = np.array(img)
        images.append(img_array)
        
    images = np.array(images)
    images = images.astype('float32') / 255.0  # Normalization
    
    return images