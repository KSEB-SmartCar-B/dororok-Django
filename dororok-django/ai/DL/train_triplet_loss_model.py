import os
import tensorflow as tf
from tensorflow.keras import layers, models
from ai.DL.data_preprocessing import preprocess_data
import numpy as np

def train_and_save_model():
    # 데이터 로드 및 전처리 (정규화 포함)
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_file_dir)
    directory = os.path.join(base_dir, 'genre_audio_feature')

    print(f"'genre_audio_feature' 디렉토리의 절대 경로: {directory}")

    if os.path.exists(directory):
        print(f"디렉토리 {directory}가 존재합니다.")
        files = os.listdir(directory)
        print(f"디렉토리 내부의 파일들: {files}")
    else:
        print(f"디렉토리 {directory}가 존재하지 않습니다.")
        return

    # 데이터 전처리 수행
    data, scaled_features, labels, scaler = preprocess_data(directory)

    def triplet_batch_generator(data, labels, batch_size=128):
        max_index = len(data) - 1
        while True:
            triplets = []
            triplet_set = set()

            while len(triplets) < batch_size:
                i = np.random.randint(0, max_index + 1)
                anchor = data[i]
                anchor_label = labels[i]

                positive_indices = np.where(labels == anchor_label)[0]
                positive_indices = positive_indices[positive_indices != i]

                negative_indices = np.where(labels != anchor_label)[0]

                if len(positive_indices) > 0 and len(negative_indices) > 0:
                    pos_idx = np.random.choice(positive_indices)
                    neg_idx = np.random.choice(negative_indices)

                    if pos_idx <= max_index and neg_idx <= max_index:
                        positive = data[pos_idx]
                        negative = data[neg_idx]

                        triplet = (tuple(anchor), tuple(positive), tuple(negative))

                        if triplet not in triplet_set:
                            triplet_set.add(triplet)
                            triplets.append([anchor, positive, negative])

            triplets = np.array(triplets)
            yield [triplets[:, 0], triplets[:, 1], triplets[:, 2]], np.zeros((len(triplets), 1))

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

    def triplet_loss(y_true, y_pred, alpha=0.4):
        anchor, positive, negative = y_pred[:, 0], y_pred[:, 1], y_pred[:, 2]
        pos_dist = tf.reduce_sum(tf.square(anchor - positive), axis=1)
        neg_dist = tf.reduce_sum(tf.square(anchor - negative), axis=1)
        loss = tf.maximum(pos_dist - neg_dist + alpha, 0.0)
        return tf.reduce_mean(loss)

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
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.000001), loss=triplet_loss)

    batch_size = 128
    steps_per_epoch = len(scaled_features) // batch_size

    validation_steps = len(scaled_features) // batch_size // 5
    val_batch_generator = triplet_batch_generator(scaled_features, labels, batch_size=batch_size)

    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    model.fit(
        triplet_batch_generator(scaled_features, labels, batch_size=batch_size),
        steps_per_epoch=steps_per_epoch,
        epochs=1000,
        validation_data=val_batch_generator,
        validation_steps=validation_steps,
        callbacks=[early_stopping]
    )

    def save_model(model, scaler, model_path, scaler_path, base_network_path):
        # 모델을 저장할 경로가 존재하는지 확인하고, 없으면 디렉토리 생성
        model_dir = os.path.dirname(model_path)
        base_network_dir = os.path.dirname(base_network_path)

        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        if not os.path.exists(base_network_dir):
            os.makedirs(base_network_dir)

        # 전체 모델(triplet model) 저장
        model.save(model_path)

        # 베이스 네트워크 모델 저장
        base_network.save(base_network_path)

        # 스케일러 저장
        np.savez(scaler_path, mean_=scaler.mean_, scale_=scaler.scale_)

    # 경로 설정 예시
    model_path = '/usr/src/app/dororok-django/ai/DL/Model/advance/triplet_model_advance.keras'
    scaler_path = '/usr/src/app/dororok-django/ai/DL/Model/advance/scaler_params.npz'
    base_network_path = '/usr/src/app/dororok-django/ai/DL/Model/advance/base_network_advance.keras'

    # 모델 저장
    save_model(model, scaler, model_path, scaler_path, base_network_path)

if __name__ == '__main__':
    train_and_save_model()