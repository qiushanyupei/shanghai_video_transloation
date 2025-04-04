from flask import Flask
# from flask_cors import CORS
from routes.home_page import home
from routes.register import register
from routes.login import login
from routes.edit import edit
from routes.upload_record import upload_record
from routes.new_video import new_video
from routes.fetch_community import fetch_community
from routes.change_public_status import change_public_status
from routes.change_favorite import change_favorite
from routes.fetch_favorite import fetch_favorite
from routes.cancel_favorite import cancel_favorite

#初始化
app = Flask(__name__)
# CORS(app)

#需要的端口蓝图
app.register_blueprint(home)
app.register_blueprint(register)
app.register_blueprint(login)
app.register_blueprint(edit)
app.register_blueprint(upload_record)
app.register_blueprint(new_video)
app.register_blueprint(fetch_community)
app.register_blueprint(change_public_status)
app.register_blueprint(change_favorite)
app.register_blueprint(fetch_favorite)
app.register_blueprint(cancel_favorite)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
