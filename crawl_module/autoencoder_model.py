from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import Adam

def build_advanced_autoencoder(input_shape=(28, 28, 1)):
    input_img = Input(shape=input_shape)
    
    # 인코더
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    encoded = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    
    # 디코더 (디코더가 필요한가? 잠재벡터만 추출할건데. 일단 놔두고)
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)
    
    autoencoder = Model(input_img, decoded)
    encoder_model = Model(inputs=input_img, outputs=encoded)
    #autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
    autoencoder.compile(optimizer=Adam(lr=0.001), loss='binary_crossentropy')
    return autoencoder, encoder_model

# 모델 생성 및 학습
def train_advanced_autoencoder(autoencoder, train_data, epochs=50, batch_size=256):
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10),
        ModelCheckpoint(filepath='best_autoencoder_model.h5', monitor='val_loss', save_best_only=True)
    ]
    
    autoencoder.fit(train_data, train_data,
                    epochs=epochs,
                    batch_size=batch_size,
                    shuffle=True,
                    validation_split=0.2, 
                    callbacks=callbacks)
    
    # 최종 모델 저장
    autoencoder.save("final_autoencoder_model.h5")









# # 모델 생성 및 학습
# advanced_autoencoder = build_advanced_autoencoder()

# # Early Stopping and Model Checkpoint
# callbacks = [
#     EarlyStopping(monitor='val_loss', patience=10),
#     ModelCheckpoint(filepath='best_autoencoder_model.h5', monitor='val_loss', save_best_only=True)
# ]

# # 모델 학습
# # advanced_autoencoder.fit(x_train, x_train, epochs=50, batch_size=256, shuffle=True, validation_data=(x_test, x_test), callbacks=callbacks)
