from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb+srv://port99:BBRnaAd7f3Hadhrq@cluster0.5l5eay2.mongodb.net/?retryWrites=true&w=majority')
db = client.milmmelier;

# 로그인 페이지 코딩 시작

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="아이디/비밀번호가 일치하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token =  jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 프로필 업데이트
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

# 맛집 페이지 코딩 시작

@app.route('/matjipmark')
def matjip():
    return render_template('index.html')


@app.route('/matjip', methods=["GET"])
def get_matjip():
# 맛집 목록을 반환하는 API
    return jsonify({'result': 'success', 'matjip_list': []})

@app.route('/like_matjip', methods=["POST"])
def like_matjip():
    title_receive = request.form["title_give"]
    address_receive = request.form["address_give"]
    action_receive = request.form["action_give"]
    print(title_receive, address_receive, action_receive)

    if action_receive == "like":
        db.matjips.update_one({"title": title_receive, "address": address_receive}, {"$set": {"liked": True}})
    else:
            db.matjips.update_one({"title": title_receive, "address": address_receive}, {"$unset": {"liked": False}})
    return jsonify({'result': 'success'})

# 크롤링 코드 시작

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://www.mangoplate.com/search/%EB%B0%80%ED%81%AC%ED%8B%B0', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
cafes = soup.select('body > main > article > div.column-wrapper > div > div > section > div.search-list-restaurants-inner-wrap > ul > li')
for cafe in cafes:
    a = cafe.select_one('figure > figcaption > div > a > h2')
    if a is not None:
        name = " ".join(a.text.split())
        star = cafe.select_one('div:nth-child(1) > figure > figcaption > div > strong').text
        address = cafe.select_one('div:nth-child(1) > figure > a > div > img')['alt'].split("-",maxsplit=1)[1]

        doc = {
            'star' : star,
            'name' : name,
            'address' : address
        }
        db.matjips.insert_one(doc)


# 리뷰 페이지 코딩 시작

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/review/edit')
def reviewEdit():
    return render_template('edit.html')

@app.route('/review/listing', methods=['GET'])
def show_review():

    reviews = list(db.review.find({}, {'_id' : False}))
  
    return jsonify({'reviews': reviews})

@app.route("/review/posting", methods=["POST"])
def review_post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    # file = request.files["file_give"]
    
    doc = {
        'title' : title_receive,
        'content' : content_receive,
        # 'file' : file
    }

    db.review.insert_one(doc)

    return jsonify({'msg':'작성 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)