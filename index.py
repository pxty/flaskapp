from flask import Flask
# импорт для индекса файлов
from flask_autoindex import AutoIndex
# импорт для загрузчика файлов
from flask import flash, request, redirect, render_template, session
from werkzeug.utils import secure_filename
# импорт для работы с путями
import os
# Для .env
from dotenv import load_dotenv
# авторизация
from flask_httpauth import HTTPBasicAuth
from datetime import timedelta


app = Flask(__name__)


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
UPLOAD_FOLDER = str(os.getcwd()) + str(os.environ.get('UPLOAD_FOLDER'))
ALLOWED_KEYS = os.environ.get("ALLOWED_KEYS").split("|")
ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS").split("|")
app.permanent_session_lifetime = timedelta(seconds=12)


files_index = AutoIndex(app, browse_root=UPLOAD_FOLDER, add_url_rules=False)


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    """Пара логин пароль из POST-запроса сравнивается с тем, что в ALLOWED_KEYS.
    """
    if username == ALLOWED_KEYS[0]:
        if password == ALLOWED_KEYS[1]:
            return username


@app.route("/", methods=["POST", "GET"])
def login():
    """ Логин в приложение и сохранение в сесии"""
    if request.method == "POST":
        user = request.form["k1"]
        passw = request.form["k2"]
        if verify_password(user, passw):
            session["user"] = user
            session["passw"] = passw
            return redirect("user")  # уходим к списку файлов
        else:
            return redirect("/")  # Неверные логин и пароль
    else:
        if "user" in session and "passw" in session:
            return redirect("user")  #
        return render_template("index.html")  # возврат к форме авторизации


@app.route('/user', methods=('POST', 'GET'))
@app.route('/user/<path:path>')
def autoindex(path='.'):
    if "user" in session:
        return files_index.render_autoindex(path, template='fileList.html')
    else:
        return redirect("/")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Загрузка файла в директорию UPLOAD_FOLDER
    Проверка метода, авторизации, что файл был выбран
    что расширение файла разрешено.
    """
    if "user" in session:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':  # непустой
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):  #
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                return redirect(request.url)
        return redirect("user")


@app.route("/logout")
def logout():
    """Сбрасывает сессию, происходит разлогинивание."""
    session.pop("user", None)
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
