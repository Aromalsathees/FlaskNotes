from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash,check_password_hash  
from models import db, User
# create flaskapp and database configurations
app = Flask(__name__)
app.config['SECRET_KEY'] ='authenticationkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db.init_app(app)


# register urls and views starts from here
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)
        user = User(username=username,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect((url_for('login')))
    return render_template('register.html')


# Login urls and views starts from here
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password,password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')


# dashboard urls and views starts from here
@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')
    


# logout urls and views starts from here
@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)