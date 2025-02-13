# システムを動かす手順↓
## インストール
・サイトから3.12以上のバージョンのPythonのインストール
バージョン確認のコマンド
python --version
Python 3.12.4

・以下のコマンドを入力し仮想環境に接続
python -m venv venv
.\venv\Scripts\activate

・Djangoのインストール
pip install Django==4.2

・PyMySQLのインストール
pip install PyMySQL

pip install django-extensions

・自然言語処理に関するインスール
pip install spacy
pip install ja-ginza
python -m spacy download ja_core_news_sm

・jwtのインストール
pip install djangorestframework-simplejwt

・サイトからXAMMPをインストール
　phpMyAdminにアクセスし、DBを新規作成する

## マイグレートを行う
python manage.py migrate

## Djangoサーバー起動
python manage.py runserver