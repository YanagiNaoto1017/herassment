import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer

# CSVファイルを読み込む
df = pd.read_csv('app/harassment_model.csv')

# データフレームを表示する
print(df)

# データフレームのカラムを確認
print("Columns:", df.columns)

# 特徴量とラベルを分ける
x = df['text']  # テキストデータ
y = df['labels']  # ラベルデータ

# テキストデータを数値ベクトルに変換
vectorizer = CountVectorizer()
x_vectorized = vectorizer.fit_transform(x)

X_train, X_test, y_train, y_test = train_test_split(x_vectorized, y, test_size=0.2, random_state=42)

# 訓練データでモデルを学習
model = RandomForestClassifier()
model.fit(X_train, y_train)

# モデルを保存
joblib.dump(model, 'harassment_model.pkl')