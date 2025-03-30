from flask import Blueprint,render_template,request
from db.db_init import get_db
from db.db_table import User

register = Blueprint('register', __name__)

@register.route('/register',methods=['GET','POST'])
def register_():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('name')
        password = request.form.get('password')
        # confirm_password = request.form.get('check password')
        with get_db() as db:
            # 检查用户名是否已存在
            existing_user = db.query(User).filter(User.username == username).first()
            if existing_user:#存在重复用户名，不允许注册
                return "Failure"

            # 创建新用户对象
            new_user = User(username=username, password=password)
            # 添加到会话
            db.add(new_user)
            # 提交会话，将数据保存到数据库
            db.commit()

        return "Success"

    return render_template("注册.html")