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

nulls = pd.read_csv("data/null.csv")
one_s = pd.read_csv("data/1s.csv")
two_s = pd.read_csv("data/2s.csv")
three_s = pd.read_csv("data/3s.csv")
fours_s = pd.read_csv("data/4s.csv")
five_s = pd.read_csv("data/5s.csv")
six_s = pd.read_csv("data/6s.csv")
seven_s = pd.read_csv("data/7s.csv")
eight_s = pd.read_csv("data/8s.csv")
nines_s = pd.read_csv("data/9s.csv")



df1 = df1.drop(df1[df1["label"] == 1].index)
df1 = df1.drop(df1[df1["label"] == 4].index)
df = pd.concat([df1, ones, fours], axis=0)

i_zero, i_one, i_two, i_three, i_four, i_five, i_six, i_seven, i_eight, i_nine = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

for row in range(len(df.index)):
    if df.iloc[row]["label"] == 0:
        df.iloc[row] = nulls.iloc[i_zero].copy()
        i_zero += 1
    if df.iloc[row]["label"] == 1 and i_one < 1000:
        df.iloc[row] = one_s.iloc[i_one].copy()
        i_one += 1
    if df.iloc[row]["label"] == 2 and i_two < 1000:
        df.iloc[row] = two_s.iloc[i_two].copy()
        i_two += 1
    if df.iloc[row]["label"] == 3 and i_three < 1000:
        df.iloc[row] = three_s.iloc[i_three].copy()
        i_three += 1
    if df.iloc[row]["label"] == 4 and i_four < 1000:
        df.iloc[row] = fours_s.iloc[i_four].copy()
        i_four += 1
    if df.iloc[row]["label"] == 5 and i_five < 1000:
        df.iloc[row] = five_s.iloc[i_five].copy()
        i_five += 1
    if df.iloc[row]["label"] == 6 and i_six < 1000:
        df.iloc[row] = six_s.iloc[i_six].copy()
        i_six += 1
    if df.iloc[row]["label"] == 7 and i_seven < 1000:
        df.iloc[row] = seven_s.iloc[i_seven].copy()
        i_seven += 1
    if df.iloc[row]["label"] == 8 and i_eight < 1000:
        df.iloc[row] = eight_s.iloc[i_eight].copy()
        i_eight += 1
    if df.iloc[row]["label"] == 9 and i_nine < 1000:
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

model.save("models/TM.keras")