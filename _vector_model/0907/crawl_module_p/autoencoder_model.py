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

    # def train_model(self, train_images, test_images):
    #     self.autoencoder_model.fit(
    #         train_images, train_images,
    #         epochs=50,
    #         batch_size=128,
    #         shuffle=True,
    #         validation_data=(test_images, test_images)
    #     )

    def save_model(self, path='autoencoder_model.h5'):
        self.autoencoder_model.save(path)

    def extract_latent_vectors(self):
        # 잠재 벡터 추출 모델 저장 (인코더 부분만)
        self.encoder_model = Model(inputs=self.autoencoder_model.input, outputs=self.autoencoder_model.layers[-7].output)
        self.encoder_model.save("encoder_model.h5")
        
        # 이미지 데이터 로딩 및 전처리
        # 여기서는 self.image_dir 폴더에서 이미지를 로드하고 전처리한다고 가정합니다.
        image_files = os.listdir(self.image_dir)
        images = [load_and_process_single_image(os.path.join(self.image_dir, f)) for f in image_files]  
        images = [img for img in images if img is not None]  # None 제거
        if len(images) == 0:
            return None
        images = np.array(images)
        
        # 잠재 벡터 추출
        latent_vectors = self.encoder_model.predict(images)
        if np.isnan(latent_vectors).any():
            return None
        return latent_vectors
    
    def load_model(self, path='autoencoder_model.h5'):
        self.autoencoder_model = load_model(path)
