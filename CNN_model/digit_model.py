import pandas as pd
import numpy as np
import keras
from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras import regularizers
from sklearn.utils import shuffle
from keras.models import save_model
from sklearn.model_selection import train_test_split

df1 = pd.read_csv("data/train_digit.csv")
ones = pd.read_csv("data/1.csv")
fours = pd.read_csv("data/4.csv")
sixes = pd.read_csv("data/6.csv")
eights = pd.read_csv("data/8.csv")

nulls = pd.read_csv("data/null.csv")
ones_s = pd.read_csv("data/1s.csv")
nines_s = pd.read_csv("data/9s.csv")
fours_s = pd.read_csv("data/4s.csv")

df1 = df1.drop(df1[df1["label"] == 1].index)
df1 = df1.drop(df1[df1["label"] == 4].index)
df = pd.concat([df1, ones, fours], axis=0)

i_zero = 0
i_four = 0
i_six = 0
i_eight = 0
i_one = 0
i_nine = 0
for row in range(len(df.index)):
    if df.iloc[row]["label"] == 0:
        df.iloc[row] = nulls.iloc[i_zero].copy()
        i_zero += 1
    if df.iloc[row]["label"] == 4 and i_four < 1500:
        df.iloc[row] = fours_s.iloc[i_four].copy()
        i_four += 1
    if df.iloc[row]["label"] == 6 and i_six < 1500:
        df.iloc[row] = sixes.iloc[i_six].copy()
        i_six += 1
    if df.iloc[row]["label"] == 8 and i_eight < 1500:
        df.iloc[row] = eights.iloc[i_eight].copy()
        i_eight += 1
    if df.iloc[row]["label"] == 1 and i_one < 1500:
        df.iloc[row] = ones_s.iloc[i_one].copy()
        i_one += 1
    if df.iloc[row]["label"] == 9 and i_nine < 1500:
        df.iloc[row] = nines_s.iloc[i_nine].copy()
        i_nine += 1




df = shuffle(df)
y = np.array(df["label"])
X = np.array(df.drop((["label"]), axis=1))

X = X.reshape(-1, 28, 28, 1)

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
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    metrics=[
        keras.metrics.SparseCategoricalAccuracy(name="acc"),
    ],
)

model.fit(X, y, epochs=10, validation_split=0.1, batch_size=64,
          callbacks=[keras.callbacks.EarlyStopping(monitor="val_acc", patience=7, restore_best_weights=True)])

model.save("models/digitModel.keras")