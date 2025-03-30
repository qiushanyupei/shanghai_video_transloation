from flask import Blueprint,render_template

edit = Blueprint('edit', __name__)

@edit.route('/edit',methods=['GET','POST'])
def edit_():
    return render_template("编辑界面.html")