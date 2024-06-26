import pandas as pd
import numpy as np
import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.utils import shuffle

# read MNIST data
df1 = pd.read_csv("csv_data/train_digit.csv")

# read additional digit data
ones = pd.read_csv("csv_data/1.csv")
fours = pd.read_csv("csv_data/4.csv")
nulls = pd.read_csv("csv_data/null.csv")

new_data = [pd.read_csv("csv_data/1s.csv"),
            pd.read_csv("csv_data/2s.csv"),
            pd.read_csv("csv_data/3s.csv"),
            pd.read_csv("csv_data/4s.csv"),
            pd.read_csv("csv_data/5s.csv"),
            pd.read_csv("csv_data/6s.csv"),
            pd.read_csv("csv_data/7s.csv"),
            pd.read_csv("csv_data/8s.csv"),
            pd.read_csv("csv_data/9s.csv")]

nines_s = pd.read_csv("csv_data/9s.csv")

# replace MNIST '1' and '4' with mine + replace '0' with empty image
df1 = df1.drop(df1[df1["label"] == 1].index)
df1 = df1.drop(df1[df1["label"] == 4].index)
df1 = df1.drop(df1[df1["label"] == 0].index)
df = pd.concat([df1, ones, fours, nulls], axis=0)

# replace 1000 MNIST samples of each digit with new data
replaced_cnt = [0 for _ in range(10)]
for row in range(len(df.index)):
    for i in range(1, 10):
        if df.iloc[row]["label"] == i and replaced_cnt[i] < 1000:
            df.iloc[row] = new_data[i-1].iloc[replaced_cnt[i]].copy()
            replaced_cnt[i] += 1


# prepare training data
df = shuffle(df)
y = np.array(df["label"])
X = np.array(df.drop((["label"]), axis=1))
X = X.reshape(-1, 28, 28, 1)

# create convolutional model
model = keras.Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(10, activation='softmax')
])

model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(),
    optimizer=keras.optimizers.Adam(learning_rate=1e-4),
    metrics=[
        keras.metrics.SparseCategoricalAccuracy(name="acc"),
    ],
)


# train and save model
model.fit(X, y, epochs=25, validation_split=0.2, batch_size=128,
          callbacks=[keras.callbacks.EarlyStopping(monitor="val_acc", patience=3)])

model.save("../resources/models/model.keras")