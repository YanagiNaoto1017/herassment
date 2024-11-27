Package            Version
------------------ ---------
annotated-types    0.7.0
asgiref            3.8.1
blis               1.0.1
catalogue          2.0.10
certifi            2024.8.30
charset-normalizer 3.4.0
click              8.1.7
cloudpathlib       0.20.0
colorama           0.4.6
confection         0.1.5
cymem              2.0.10
Django             4.2
django-extensions  3.2.3
filelock           3.16.0
fsspec             2024.9.0
ginza              5.2.0
idna               3.10
ja_core_news_sm    3.8.0
ja-ginza           5.2.0
Jinja2             3.1.4
langcodes          3.5.0
language_data      1.3.0
marisa-trie        1.2.1
markdown-it-py     3.0.0
MarkupSafe         2.1.5
mdurl              0.1.2
mpmath             1.3.0
murmurhash         1.0.11
mysqlclient        2.2.6
networkx           3.3
numpy              2.0.2
opencv-python      4.10.0.84
packaging          24.2
pillow             10.4.0
pip                24.3.1
plac               1.4.3
preshed            3.0.9
pydantic           2.10.2
pydantic_core      2.27.1
Pygments           2.18.0
PyMySQL            1.1.1
requests           2.32.3
rich               13.9.4
sendmail           2.0
setuptools         74.1.2
shellingham        1.5.4
smart-open         7.0.5
spacy              3.8.2
spacy-legacy       3.0.12
spacy-loggers      1.0.5
sqlparse           0.5.1
srsly              2.4.8
SudachiDict-core   20241021
SudachiPy          0.6.9
sympy              1.13.2
thinc              8.3.2
torch              2.4.1
torchvision        0.19.1
tqdm               4.67.1
typer              0.13.1
typing_extensions  4.12.2
tzdata             2024.1
urllib3            2.2.3
wasabi             1.1.3
weasel             0.4.1
wrapt              1.17.0

# Django インストール
pip install Django==4.2

# Djangoサーバー起動
python manage.py runserver

# 自然言語処理に関するインスール
pip install spacy
python -m spacy download ja_core_news_sm
pip install ja-ginza