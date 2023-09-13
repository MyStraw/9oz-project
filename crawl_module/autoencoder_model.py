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


# # YOLO3 모델 로드
# net = dnn.readNet("yolov3.weights", "yolov3.cfg")
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# # YOLOv5 모델 로드
# model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # 'yolov5s'는 작은 모델, 'yolov5l'은 큰 모델
# Blob to PNG 함수

def convert_blob_to_png(blob_path, png_path):
    with open(blob_path, 'rb') as f:
        blob_data = f.read()
    image = Image.open(io.BytesIO(blob_data))
    image.save(png_path)




class Autoencoder:
    def __init__(self, image_dir='C:/queenit/'):
        self.image_dir = image_dir
        self.autoencoder_model = None
        self.encoder_model = None  # 잠재 벡터를 추출하기 위한 인코더 모델

    def build_model(self):
        # VGG16 모델 불러오기
        vgg16 = VGG16(weights='imagenet', include_top=False, input_shape=(416, 416, 3))
        vgg16.trainable = False  # Freeze the VGG16 layers

        # 오토인코더 모델 초기화
        self.autoencoder_model = Sequential()

        # 인코더 부분 (VGG16)
        self.autoencoder_model.add(vgg16)

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


    
    # # YOLO3를 이용한 객체 인식 함수
    # def detect_objects(self, image):
    #     net.setInput(cv2.dnn.blobFromImage(image, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False))
    #     layerOutputs = net.forward(output_layers)
        
    #     object_coordinates = []
        
    #     for output in layerOutputs:
    #         for detection in output:
    #             scores = detection[5:]
    #             classID = np.argmax(scores)
    #             confidence = scores[classID]
    #             if confidence > 0.5:  # Confidence level
    #                 box = detection[0:4] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])
    #                 (centerX, centerY, width, height) = box.astype("int")
                    
    #                 x1 = int(centerX - (width / 2))
    #                 y1 = int(centerY - (height / 2))
    #                 x2 = x1 + width
    #                 y2 = y1 + height
                    
    #                 object_coordinates.append((x1, y1, x2, y2))
                    
    #     return object_coordinates
    
    
    
    # # YOLOv5 이용
    # def detect_objects(self, image):
    #     print("Input image shape:", image.shape)  # 입력 이미지의 형태 출력
    #     results = model(image)  # 이미지를 YOLOv5 모델에 적용
    #     print("YOLOv5 Results:", results.xyxy[0])  # 디버깅용
    #     object_coordinates = []
        
    #     # YOLOv5 결과에서 좌표 추출
    #     for det in results.xyxy[0].cpu().detach().numpy():
    #         x1, y1, x2, y2, conf, class_ = det
    #         # if conf > 0.1:  # Confidence level
    #         object_coordinates.append((int(x1), int(y1), int(x2), int(y2)))

    #     return object_coordinates
    
    
 
    




    def extract_latent_vectors(self):
        if self.autoencoder_model is None:
            print("Error: Autoencoder model is not built.")
            return None
        # 잠재 벡터 추출 모델 저장 (인코더 부분만)
        self.encoder_model = Model(inputs=self.autoencoder_model.input, outputs=self.autoencoder_model.layers[-7].output)
        self.encoder_model.save("encoder_model.h5")
        
        # 이미지 데이터 로딩 및 전처리
        # 여기서는 self.image_dir 폴더에서 이미지를 로드하고 전처리한다고 가정합니다.
        image_files = os.listdir(self.image_dir)            
        
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
            print(f"Processing file {idx + 1} of {total_files}") 
            if f.endswith('.blob'):
                png_path = f"{f[:-5]}.png"  # .blob 확장자 제거 후 .png 추가
                convert_blob_to_png(os.path.join(self.image_dir, f), os.path.join(self.image_dir, png_path))
                f = png_path  # 이제 f는 .png 파일을 가리킵니다.
            
            img = load_and_process_single_image(os.path.join(self.image_dir, f))
            # if img is not None:
            #     images.append(img)
            if img is None:
                print(f"Image {f} could not be processed.")
            
            # 배경 제거 부분 추가
            input_image = Image.open(os.path.join(self.image_dir, f))
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
       
        #기존코드...for부분이 대체
        # images = [load_and_process_single_image(os.path.join(self.image_dir, f)) for f in image_files]         
        # images = [img for img in images if img is not None]  # None 제거
      
       
        # 디버깅 코드: images 리스트 길이 출력
        print(f"Number of images loaded: {len(images)}")
        if len(images) == 0:
            return None
        images = np.array(images)
        
        # # YOLO로 객체 좌표 추출 및 잠재 벡터 추출
        # latent_vectors = []
        # for img in images:
        #     object_coordinates = self.detect_objects(img)
        #     for coord in object_coordinates:
        #         x1, y1, x2, y2 = coord
        #         object_img = img[y1:y2, x1:x2]  # 객체 부분만 추출
        #         print("Object coordinates: ", object_coordinates)  # 디버깅용
                
        #         # 여기서 object_img를 VGG16에 맞게 전처리.
        #         object_img_resized = cv2.resize(object_img, (32, 32))  # 예: 크기를 (32, 32)로 조절
        #         object_img_ready = np.expand_dims(object_img_resized, axis=0)  # 차원 추가
                
        #         object_vector = self.encoder_model.predict(object_img_ready)  # 잠재 벡터 추출
        #         latent_vectors.append(object_vector)
        # latent_vectors = np.array(latent_vectors)
        # print("Shape of latent_vectors: ", np.array(latent_vectors).shape)
        
        # # 문제가 있을 경우 로그 출력
        # if latent_vectors.shape[0] == 0:
        #     print("Error: Latent vectors are not properly generated.")
        #     response = {"status": "failure"}
        # else:
        #     # ... (이하 코드)
        #     response = {"status": "success"}
        
        
        # return latent_vectors
        
        
        
        
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