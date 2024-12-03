from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Создаем приложение Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Установите свой секретный ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Путь к базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем отслеживание изменений

# Инициализация базы данных
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Главная страница
@app.route('/')
def home():
    return render_template('index.html')

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        # Проверка, существует ли уже пользователь с таким именем
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно! Войдите в систему.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Сохраняем ID пользователя в сессии
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

if __name__ == '__main__':
    # Создаем таблицы в базе данных перед запуском приложения
    with app.app_context():
        db.create_all()  # Создание таблиц, если их еще нет
    app.run(debug=True)
