from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Dense, Flatten, Reshape, UpSampling2D, Conv2D
from tensorflow.keras.applications import VGG16
import numpy as np
import os
from load_and_process_images import load_and_process_single_image
from cv2 import dnn  # YOLO를 위한 OpenCV DNN 모듈
import cv2
import torch
import io
from PIL import Image
from rembg import remove
from datetime import datetime
from tensorflow.keras.applications import ResNet50

def convert_blob_to_png(blob_path, png_path):
    with open(blob_path, 'rb') as f:
        blob_data = f.read()
    image = Image.open(io.BytesIO(blob_data))
    image.save(png_path)
    
    
def convert_gif_to_png(gif_path, png_path):
    image = Image.open(gif_path)
    image = image.convert('RGBA')  # 애니메이션 GIF의 첫 프레임만 가져옵니다.
    image.save(png_path)    

class Autoencoder:
    def __init__(self, image_dir='C:/queenit/'):
        self.image_dir = image_dir
        self.autoencoder_model = None
        self.encoder_model = None  # 잠재 벡터를 추출하기 위한 인코더 모델

    def build_model(self):
        # # VGG16 모델 불러오기
        # vgg16 = VGG16(weights='imagenet', include_top=False, input_shape=(416, 416, 3))
        # vgg16.trainable = False  # Freeze the VGG16 layers
        
        # ResNet50 모델 불러오기
        resnet50 = ResNet50(weights='imagenet', include_top=False, input_shape=(416, 416, 3))
        resnet50.trainable = False  # Freeze the ResNet50 layers
        
        
        

        # 오토인코더 모델 초기화
        self.autoencoder_model = Sequential()

        # # 인코더 부분 (VGG16)
        # self.autoencoder_model.add(vgg16)
        # 인코더 부분 (ResNet50)
        self.autoencoder_model.add(resnet50)

        # Flatten과 Dense (잠재벡터)
        self.autoencoder_model.add(Flatten())
        self.autoencoder_model.add(Dense(64, activation='relu')) #얘가 잠재벡터

        # 디코더 부분 (옵션)
        self.autoencoder_model.add(Dense(8 * 8 * 128, activation='relu'))
        self.autoencoder_model.add(Reshape((8, 8, 128)))
        self.autoencoder_model.add(UpSampling2D((2, 2)))
        self.autoencoder_model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
        self.autoencoder_model.add(UpSampling2D((2, 2)))
        self.autoencoder_model.add(Conv2D(3, (3, 3), activation='sigmoid', padding='same'))

        # 모델 컴파일
        self.autoencoder_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['mse'])

    def train_model(self, train_images, test_images):
        history = self.autoencoder_model.fit(
            train_images, train_images,
            epochs=50,
            batch_size=128,
            shuffle=True,
            validation_data=(test_images, test_images)
        )
        #손실이랑 mse()
        train_loss = history.history['loss']
        val_loss = history.history['val_loss']
        train_mse = history.history['mse']
        val_mse = history.history['val_mse']

        # 학습 과정도 보자
        print("Train Loss: ", train_loss)
        print("Validation Loss: ", val_loss)
        print("Train MSE: ", train_mse)
        print("Validation MSE: ", val_mse)
        
        self.save_model()

        # 인코딩 및 디코딩까지 하는 모델. 난 안쓸거.(잠재벡터 뽑기만 하면 돼)
        

    def save_model(self, path='autoencoder_model.h5'):
        self.autoencoder_model.save(path) 




    def extract_latent_vectors(self, subfolder):
        if self.autoencoder_model is None:
            print("Error: Autoencoder model is not built.")
            return None
        # 잠재 벡터 추출 모델 저장 (인코더 부분만)
        self.encoder_model = Model(inputs=self.autoencoder_model.input, outputs=self.autoencoder_model.layers[-7].output)
        self.encoder_model.save("encoder_model.h5")
        
        image_files = [f for f in os.listdir(os.path.join(self.image_dir, subfolder)) if not f.endswith('.csv')]
        
        # 이미지 데이터 로딩 및 전처리
        # 여기서는 self.image_dir 폴더에서 이미지를 로드하고 전처리한다고 가정합니다.            
        
        # 디버깅 코드: image_files 길이 출력
        print(f"Number of image files: {len(image_files)}")

        # 현재 날짜와 시간을 문자열로 가져오기
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")

        # 폴더 이름에 날짜와 시간 추가하여 처음부터 만들기
        new_folder = os.path.join('C:/queenit_removed/', f'background_removed_{current_time}')

        # 폴더 생성
        try:
            os.makedirs(new_folder, exist_ok=True)
        except PermissionError:
            print("Permission denied: Cannot create directory.")
                
        images = []
        total_files = len(image_files)
        for idx, f in enumerate(image_files):
            full_image_path = os.path.join(self.image_dir, subfolder, f) 
            print(f"Processing file {idx + 1} of {total_files}") 
            
            if f.endswith('.blob'):
                png_path = f"{f[:-5]}.png"  # .blob 확장자 제거 후 .png 추가
                convert_blob_to_png(full_image_path, os.path.join(self.image_dir,subfolder, png_path))
                f = png_path  # 이제 f는 .png 파일을 가리킵니다.
            if f.endswith('.gif'):
                png_path = f"{f[:-4]}.png"  # .gif 확장자 제거 후 .png 추가
                convert_gif_to_png(full_image_path, os.path.join(self.image_dir, subfolder, png_path))
                f = png_path     
            
            img = load_and_process_single_image(full_image_path)
            # if img is not None:
            #     images.append(img)
            if img is None:
                print(f"Image {f} could not be processed.")
            
            # 배경 제거 부분 추가
            input_image = Image.open(full_image_path) 
            output_image = remove(input_image)
            
            # RGBA to RGB
            if output_image.mode == 'RGBA':
                output_image = output_image.convert('RGB')
                
            # 하위 폴더에 이미지 저장
            output_image_path = os.path.join(new_folder, f)
            output_image.save(output_image_path)  # 원래 이미지 덮어쓰기
            
            # 하위 폴더에서 이미지 로딩 및 잠재 벡터 추출
            img = load_and_process_single_image(output_image_path)
            if img is not None:
                images.append(img)
            print(f"Finished processing and saving file {idx + 1} of {total_files}")  # 완료된 진행 상황 출력
             
       
        # 디버깅 코드: images 리스트 길이 출력
        print(f"Number of images loaded: {len(images)}")
        if len(images) == 0:
            return None
        images = np.array(images)
            
        
        
        # 잠재 벡터 추출
        latent_vectors = self.encoder_model.predict(images)
        
        # 디버깅 코드: latent_vectors 배열 형상 출력
        print(f"Shape of latent_vectors array: {latent_vectors.shape}")

        # 디버깅 코드: latent_vectors와 image_files 길이 비교
        print(f"Number of latent vectors: {len(latent_vectors)}")
        print(f"Number of image files: {len(image_files)}")
        
        if np.isnan(latent_vectors).any():
            return None
        return latent_vectors
    
    def load_model(self, path='encoder_model.h5'):
        try:
            self.encoder_model = load_model(path)
        except:
            print("Model not found, creating a new one.")
            self.build_model()
            self.encoder_model = Model(inputs=self.autoencoder_model.input, outputs=self.autoencoder_model.layers[-7].output)
            self.encoder_model.save("encoder_model.h5")