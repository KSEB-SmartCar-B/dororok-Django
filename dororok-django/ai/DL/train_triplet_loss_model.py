import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from ai.DL.data_preprocessing import preprocess_data
import numpy as np

# 데이터 로드 및 전처리
directory = '../genre_audio_feature'
data, scaled_features, labels, scaler = preprocess_data(directory)

# Triplet 배치 생성기 함수
def triplet_batch_generator(data, labels, batch_size=128):
    max_index = len(data) - 1  # 최대 인덱스는 7031
    while True:
        triplets = []
        triplet_set = set()

        while len(triplets) < batch_size:
            i = np.random.randint(0, max_index + 1)  # 인덱스 범위를 0 ~ 7031로 제한
            anchor = data[i]
            anchor_label = labels[i]

            positive_indices = np.where(labels == anchor_label)[0]
            positive_indices = positive_indices[positive_indices != i]

            negative_indices = np.where(labels != anchor_label)[0]

            if len(positive_indices) > 0 and len(negative_indices) > 0:
                pos_idx = np.random.choice(positive_indices)
                neg_idx = np.random.choice(negative_indices)

                # 범위 내 인덱스인지 다시 확인
                if pos_idx <= max_index and neg_idx <= max_index:
                    positive = data[pos_idx]
                    negative = data[neg_idx]

                    triplet = (tuple(anchor), tuple(positive), tuple(negative))

                    if triplet not in triplet_set:
                        triplet_set.add(triplet)
                        triplets.append([anchor, positive, negative])

        triplets = np.array(triplets)
        yield [triplets[:, 0], triplets[:, 1], triplets[:, 2]], np.zeros((len(triplets), 1))

# Triplet Neural Network 설계
def create_base_network(input_shape):
    input = layers.Input(shape=input_shape)
    x = layers.Dense(1024, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))(input)
    x = layers.Dense(512, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))(x)
    x = layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))(x)
    x = layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))(x)
    x = layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))(x)
    x = layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))(x)
    model = models.Model(input, x)
    return model

def triplet_loss(y_true, y_pred, alpha=0.2):
    anchor, positive, negative = y_pred[:, 0], y_pred[:, 1], y_pred[:, 2]
    pos_dist = tf.reduce_sum(tf.square(anchor - positive), axis=1)
    neg_dist = tf.reduce_sum(tf.square(anchor - negative), axis=1)
    loss = tf.maximum(pos_dist - neg_dist + alpha, 0.0)
    return tf.reduce_mean(loss)

# 네트워크 구성
input_shape = (scaled_features.shape[1],)
base_network = create_base_network(input_shape)

input_anchor = layers.Input(shape=input_shape, name="anchor_input")
input_positive = layers.Input(shape=input_shape, name="positive_input")
input_negative = layers.Input(shape=input_shape, name="negative_input")

processed_anchor = base_network(input_anchor)
processed_positive = base_network(input_positive)
processed_negative = base_network(input_negative)

merged_vector = tf.stack([processed_anchor, processed_positive, processed_negative], axis=1)

model = models.Model([input_anchor, input_positive, input_negative], merged_vector)

# 모델 컴파일
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.000001), loss=triplet_loss)

# 데이터셋을 배치 생성기로 학습
batch_size = 128
steps_per_epoch = len(scaled_features) // batch_size

# 검증 배치 생성기
validation_steps = len(scaled_features) // batch_size // 5  # 검증 데이터의 비율을 줄여 메모리 사용 감소
val_batch_generator = triplet_batch_generator(scaled_features, labels, batch_size=batch_size)

# Early Stopping 콜백 정의
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# 모델 학습
model.fit(
    triplet_batch_generator(scaled_features, labels, batch_size=batch_size),
    steps_per_epoch=steps_per_epoch,
    epochs=500,
    validation_data=val_batch_generator,
    validation_steps=validation_steps,
    callbacks=[early_stopping]
)

# 모델과 스케일러 저장
def save_model(model, scaler, model_path, scaler_path):
    model.save(model_path)
    base_network.save('base_network_full.keras')
    np.savez(scaler_path, mean_=scaler.mean_, scale_=scaler.scale_)

save_model(model, scaler, 'triplet_model_full.keras', 'scaler_params_full.npz')
