from flask import Flask, request, session, jsonify, Response
import user_info
import static_text

app = Flask(__name__)   # 创建一个实例flask对象
app.secret_key = static_text.STATIC_KEY   # session需要密码
app.config["JSON_AS_ASCII"] = False     # json返回中文而不是utf8


@app.route("/")     # 装饰器处理路由 必须有路径
def hello():
    return jsonify(msg="hello world")


@app.route("/login", methods=["POST"])
def login():
    get_data = request.get_json()
    return user_info.login_check(get_data)


@app.route("/register", methods=["POST"])
def register():
    get_data = request.get_json()
    return user_info.register_check(get_data)


app.run(host="0.0.0.0", port=5000)

