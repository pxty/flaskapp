# flaskapp
Для работы в каталоге с приложение необходимо создать .env вида, см. ниже. Не хранится в репозитории из соображений безопасности.


FLASK_APP=webapp

SECRET_KEY=yourSecretKey

ALLOWED_KEYS=username|password

UPLOAD_FOLDER=/files

ALLOWED_EXTENSIONS = txt|pdf|png|jpg|jpeg|gif|csv


PS: Если сразу не взлетит, то возможно, в Dockerfile надо править пути тут COPY ./requirements.txt /requirements.txt 
