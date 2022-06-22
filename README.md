한 곳까지 올립니다.
-html-
    function logout() {
        $.removeCookie('mytoken');
            alert('로그아웃!')
            window.location.href='/sign_in'

-py-
#포스팅한 정보를 토대로 좋아요를 업데이트(테스트는 못해봤어요)
@app.route("/get_posts", methods=['GET'])
def get_posts():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return jsonify({"result":"success", "msg":"포스팅을 가져왔습니다."})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try :
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return jsonify({"result":"success", "msg":"updated"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

#로그아웃은 틀만 짰어요. html에 있는 것만으로도 실행된다면 필요없는 부분입니다.
@app.route('/logout')
def logout():
    return render_template('login.html')
