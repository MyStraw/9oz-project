from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Dense, Flatten, Reshape, UpSampling2D, Conv2D
from tensorflow.keras.applications import VGG16
import numpy as np
import os
from load_and_process_images import load_and_process_single_image

class Autoencoder:
    def __init__(self, image_dir='C:/queenit'):
        self.image_dir = image_dir
        self.autoencoder_model = None
        self.encoder_model = None  # 잠재 벡터를 추출하기 위한 인코더 모델

    def build_model(self):
        # VGG16 모델 불러오기
        vgg16 = VGG16(weights='imagenet', include_top=False, input_shape=(32, 32, 3))
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
        
        self.save_model

        # 인코딩 및 디코딩까지 하는 모델. 난 안쓸거.(잠재벡터 뽑기만 하면 돼)
        

    def save_model(self, path='autoencoder_model.h5'):
        self.autoencoder_model.save(path)

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
        images = [load_and_process_single_image(os.path.join(self.image_dir, f)) for f in image_files]  
        
        # 이미지의 shape을 확인합니다.
        for i, img in enumerate(images):
            if img is not None:
                if img.shape != (32, 32, 3):  # 이 부분은 원하는 shape에 맞게 수정합니다.
                    print(f"이미지 {i}의 shape이 비정상입니다: {img.shape}")

        # None 값을 제거합니다.
        images = [img for img in images if img is not None]

        # NumPy 배열로 변환합니다.
        if len(images) == 0:
            return None

        images = np.array(images)  # 이 부분에서 에러가 발생했을 것입니다.
        
        
        
        
        
        
        
        
        
        images = [img for img in images if img is not None]  # None 제거
        if len(images) == 0:
            return None
        images = np.array(images)
        
        # 잠재 벡터 추출
        latent_vectors = self.encoder_model.predict(images)
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