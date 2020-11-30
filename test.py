from flask import Flask,render_template,url_for,request,session,logging,redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker


database_user = 'root'
database_pwd = 'admin123'
database = 'target'

engine = create_engine(f'mysql://{database_user}:{database_pwd}@localhost/{database}')
db=scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'iamsecret'


@app.route('/', methods=['GET'])
def data():
    test = db.execute("SELECT * FROM user").fetchone()
    return str(test.id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=2000, debug=True)