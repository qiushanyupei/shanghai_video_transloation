from flask import Blueprint,render_template,request,jsonify
from db.db_init import get_db
from db.db_table import User

login = Blueprint('login', __name__)

@login.route('/login',methods=['GET','POST'])
def login_():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('name')
        password = request.form.get('password')
        # confirm_password = request.form.get('check password')
        with get_db() as db:
            # 查询数据库中是否存在该用户名
            user = db.query(User).filter(User.username == username).first()

            if user:
                # 如果用户存在，检查密码是否匹配
                if user.password == password:  # 假设密码是明文存储（不推荐）
                    return {"flag":"Success","username":username}  # 登录成功
                else:
                    return {"flag":"Failure1","username":username}  # 密码错误
            else:
                return {"flag":"Failure2","username":username}  # 用户名不存在

    return render_template("登录.html")