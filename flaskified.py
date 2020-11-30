from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from crud_ops.myConfigs import Configs
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

# import models

##App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'iamsecret'
app.config.from_object(Configs)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# jwt = JWTManager(app)
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentname = db.Column(db.String(), nullable=True)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id


# JWT area
def token_generation(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user_session = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return 'Token is invalid !!'

        return func(current_user_session, *args, **kwargs)

    return decorated


@app.route('/', methods=['POST', 'GET'])
@token_generation
def index(current_user_session):
    if request.method == 'POST':
        task_data = request.form
        sid = task_data['id']
        name = task_data['name']
        push_task = Students(id=sid, studentname=name)

        try:
            db.session.add(push_task)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There could be an issue with your Code, Please check ;<'

    else:
        tasks = Students.query.order_by(Students.dateCreated).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:ids>')
def delete(ids):
    drop_student = Students.query.get(ids)
    try:
        db.session.delete(drop_student)
        db.session.commit()
        return redirect('/')
    except:
        return "Delete Code has some issue, Learn well before doing this stuff ;)"


@app.route('/update/<int:ids>', methods=['POST', 'GET'])
def update(ids):
    taskUpdate = Students.query.get_or_404(ids)
    if request.method == 'POST':
        taskUpdate.id = request.form['id']
        taskUpdate.studentname = request.form['name']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue in deletion procedure'

    else:
        return render_template('/update.html', task=taskUpdate)


@app.route('/dict')
def dictionary():
    dict = {'Eng': 100, 'Math': 101, 'Urdu': 50}
    return render_template('/dict.html', dict=dict)


# signup routing
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST' and 'email' in request.form:
        # get data from html form into python dictionary
        signupData = request.form
        # get variables
        name, email = signupData.get('name'), signupData.get('email'),
        password = signupData.get('password')
        # Checking  if user is already in database
        checkUser = Users.query.filter_by(email=email).first()

        if not checkUser:
            insertUser = Users(public_id=str(uuid.uuid4()),
                               name=name,
                               email=email,
                               password=generate_password_hash(password))
            try:
                db.session.add(insertUser)
                db.session.commit()
                return render_template('login.html')
            except:
                return 'Server is not responding', 202

        else:
            # returns 202 if user already exists
            return make_response('User already exists. Please Log in.', 202)
    else:
        return render_template('/signup.html')


# signup routing
@app.route('/login', methods=['POST', 'GET'])
def login():
    loginForm = request.form
    if request.method == 'POST':
        if not loginForm and loginForm.get('email') and loginForm.get('password'):
            return make_response('Could not verify',
                                 404,
                                 {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
                                 )
        # Check user in database
        userExists = Users.query.filter_by(email=loginForm.get('email')).first()
        if not userExists:
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
            )

        if check_password_hash(userExists.password, loginForm.get('password')):
            token = jwt.encode({'public_id': userExists.public_id,
                                'exp': datetime.utcnow() + timedelta(minutes=30)},
                               app.config['SECRET_KEY'])

            headers = {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                'x-access-token': token
            }
            # response = redirect(url_for('index'))
            # response.headers['x-access-token'] = token.decode('UTF-8') # make_response(jsonify({'x-access-token': token.decode('UTF-8')}), 201)
            return redirect(url_for('index'))

        else:
            return 'PASSWORD is fake'
    else:
        return redirect('/login.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=2333, debug=True)
