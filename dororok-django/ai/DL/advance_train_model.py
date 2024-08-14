import os

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from ai.DL.data_preprocessing import preprocess_data
from ai.DL.train_triplet_loss_model import base_network


def triplet_loss(y_true, y_pred, alpha=0.2):
    anchor, positive, negative = y_pred[:, 0], y_pred[:, 1], y_pred[:, 2]
    pos_dist = tf.reduce_sum(tf.square(anchor - positive), axis=1)
    neg_dist = tf.reduce_sum(tf.square(anchor - negative), axis=1)
    loss = tf.maximum(pos_dist - neg_dist + alpha, 0.0)
    return tf.reduce_mean(loss)

model = load_model('Model/basic/triplet_model_advance.keras', custom_objects={'triplet_loss': triplet_loss})
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
directory = os.path.join(BASE_DIR, 'genre_audio_feature')
new_data, new_scaled_features, new_labels, _ = preprocess_data(directory)




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


model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.000001), loss=triplet_loss)

new_batch_size = 128
new_steps_per_epoch = len(new_scaled_features) // new_batch_size
new_val_batch_generator = triplet_batch_generator(new_scaled_features, new_labels, batch_size=new_batch_size)

early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

history = model.fit(
    triplet_batch_generator(new_scaled_features, new_labels, batch_size=new_batch_size),
    steps_per_epoch=new_steps_per_epoch,
    epochs=100,
    validation_data=new_val_batch_generator,
    validation_steps=new_steps_per_epoch // 5,
    callbacks=[early_stopping]
)

plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss During Additional Training')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()


def save_model(model, scaler, model_path, scaler_path):
    model.save(model_path)
    base_network.save('base_network_advance.keras')
    np.savez(scaler_path, mean_=scaler.mean_, scale_=scaler.scale_)
    save_model(model, None, 'Model/advance/triplet_model_advance.keras', 'Model/advance/scaler_params.npz')
