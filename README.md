# flaskapp
Для работы в каталоге с приложением необходимо создать .env вида, см. ниже. Не хранится в репозитории из соображений безопасности.


FLASK_APP=webapp

SECRET_KEY=yourSecretKey

ALLOWED_KEYS=username|password

UPLOAD_FOLDER=/files

ALLOWED_EXTENSIONS = txt|pdf|png|jpg|jpeg|gif|csv


PS: Если сразу не взлетит, то возможно, в Dockerfile надо править пути тут:

COPY ./requirements.txt /requirements.txt 

===================================

git clone https://github.com/pxty/flaskapp.git

sudo docker build -t flaskapp:latest .

sudo docker tag flaskapp pxty/flaskapp

sudo docker login -u "DockerID" -p "password" docker.io  # от докерхаба

sudo docker push pxty/flaskapp  # репозиторий на докерхабе создан заранее!!!

sudo sudo docker run --name flaskapp -d -p 5000:5000 --mount type=bind,source=/home/username/files,target=/files flaskapp
