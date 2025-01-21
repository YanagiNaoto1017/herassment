import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score

# CSVファイルを読み込む
df = pd.read_csv('app/harassment_words_model.csv')
# データフレームを表示する
print(df)

# 特徴量とラベルを分ける
x = df['words']  # テキストデータ
y = df['labels']  # ラベルデータ

# テキストデータを数値ベクトルに変換
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(x)

X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# 訓練データでモデルを学習
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)
accuracy = accuracy_score(y_test, pred)
print(accuracy)

# モデルを保存
# joblib.dump(model, 'harassment_model.pkl')

# # # モデルをロード
# model = joblib.load('harassment_model.pkl')

# input_data = [""]

# X = vectorizer.transform(input_data)

# prediction = model.predict(X)

# print(prediction)