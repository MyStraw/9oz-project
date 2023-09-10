import tensorflow as tf
import json
from PIL import Image

# 이미지를 불러와서 리사이징하는 함수
def load_and_resize_image(image_path, target_size=(800, 800)):
    image = Image.open(image_path)
    image = image.resize(target_size)
    return image

# JSON 파일을 불러와서 라벨링 정보를 추출하는 함수
def load_labeling_info(json_path):
    with open(json_path, 'r') as f:
        labeling_info = json.load(f)
    return labeling_info

# 예시
image = load_and_resize_image('/path/to/image.jpg')
labeling_info = load_labeling_info('/path/to/label.json')



# 모델 설정
model_config = {
    'backbone': 'resnet50',
    'num_classes': NUM_CLASSES,  # 분류할 클래스 수
    'optimizer': tf.keras.optimizers.SGD(learning_rate=0.002, momentum=0.9, weight_decay=0.0001),
    'start_epoch': 34,  # 미세조정을 시작할 에폭 번호
    'end_epoch': 50,  # 학습을 종료할 에폭 번호
    'image_size': (800, 800),  # 입력 이미지 크기
    'batch_size': BATCH_SIZE,  # 배치 크기
}

# tf.data.Dataset을 사용하여 데이터 파이프라인 구축
train_dataset = tf.data.Dataset.from_tensor_slices((train_image_paths, train_json_paths))
train_dataset = train_dataset.map(load_and_preprocess_data)  # 전처리 함수 적용
train_dataset = train_dataset.batch(BATCH_SIZE).shuffle(buffer_size=1000).repeat()

# 모델 학습
model.fit(train_dataset, epochs=model_config['end_epoch'], initial_epoch=model_config['start_epoch'])

# tf.data.Dataset을 사용하여 데이터 파이프라인 구축
train_dataset = tf.data.Dataset.from_tensor_slices((train_image_paths, train_json_paths))
train_dataset = train_dataset.map(load_and_preprocess_data)  # 전처리 함수 적용
train_dataset = train_dataset.batch(BATCH_SIZE).shuffle(buffer_size=1000).repeat()

# 모델 학습
model.fit(train_dataset, epochs=model_config['end_epoch'], initial_epoch=model_config['start_epoch'])

# 검증 데이터셋으로 모델 평가
val_dataset = tf.data.Dataset.from_tensor_slices((val_image_paths, val_json_paths))
val_dataset = val_dataset.map(load_and_preprocess_data).batch(BATCH_SIZE)
model.evaluate(val_dataset)
