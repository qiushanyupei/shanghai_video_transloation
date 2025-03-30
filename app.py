from flask import Flask
# from flask_cors import CORS
from routes.home_page import home
from routes.register import register
from routes.login import login
from routes.edit import edit

#初始化
app = Flask(__name__)
# CORS(app)

#需要的端口蓝图
app.register_blueprint(home)
app.register_blueprint(register)
app.register_blueprint(login)
app.register_blueprint(edit)

if __name__ == '__main__':
    app.run()
