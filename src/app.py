import os
import random, string, time
from flask import Flask, request, Response, jsonify
import sqlalchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from model.models import *

app = Flask(__name__)
app.debug = True
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'Secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

Base.metadata.create_all(engine)

#db = SQLAlchemy(app)
# from model.models import *
# db.create_all()
# db.session.commit()

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        req = request.get_json(force=True)
        em = req['email']
        psw = req['password']
        user = session.query(User).filter_by(email=em).first()
        if user:
            if check_password_hash(user.password, psw):
                x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
                token = generate_password_hash(x, method='sha256')
                new_token = session.query(Token).filter_by(email=em).first()
                if new_token!=None:
                    new_token.token = token
                    new_token.timestamp = int(time.time())
                else:
                    new_token = Token(token=token, email=em, timestamp=int(time.time()))
                    session.add(new_token)
                session.commit()
                res = {'user': user.as_dict(), 'token': new_token.as_dict()}
                return jsonify(res)
        res = Response('Invalid username/password')
        res.status = 404
        return res
    return Response(status=404)

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        req = request.get_json(force=True)
        data = req['data']
        un = data['username']
        em = data['email']
        pwd = data['password']
        asrt = session.query(User).filter_by(username=un).first()
        if asrt:
            res = Response("Username already in use!")
            res.status = 400
            return res
        asrt = session.query(User).filter_by(email=em).first()
        if asrt:
            res = Response("Email already in use!")
            res.status = 400
            return res
        usr = User(username=un, email=em, password=generate_password_hash(pwd, method='sha256'))
        session.add(usr)
        session.commit()
        res = Response('User created sucessfuly!')
        res.status = 201
        return res
    return Response(status=404)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    tk = request.headers['token']
    token = session.query(Token).filter_by(token=tk).first()
    if token.email == request.headers['email']:
        session.delete(token)
        session.commit()
        res = Response('Logged out!')
        return res

@app.route('/auth', methods=['GET'])
def auth():
    if request.method == 'GET':
        tk = request.headers['token']
        token = session.query(Token).filter_by(token=tk).first()
        if token:
            if request.headers['email'] == token.email:
                if int(time.time())-int(token.timestamp) > 1800:
                    res = Response('Session expired!')
                    res.status_code = 401
                    return res
                token.timestamp = int(time.time())
                session.add(token)
                session.commit()
                res = Response("authenticated")
                res.status_code = 200
                return res
            res = Response()
            res.status_code=401
            return res
        res = Response()
        res.status_code=401
        return res

@app.route('/user/<username>', methods=['GET'])
def user():
    user = session.query(User).filter_by(email=request.args['username']).first()
    if user:
        return jsonify(user.as_dict())
    res = Response('User not found.')
    res.status_code = 404
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)