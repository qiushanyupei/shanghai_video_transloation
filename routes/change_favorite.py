from flask import Blueprint,request,jsonify
from db.db_init import get_db
import os
from db.db_table import Video,User,Collect

change_favorite = Blueprint('change_favorite', __name__)

@change_favorite.route('/change_favorite',methods=['POST'])
def change_favorite_():
    #json接受形式
    data = request.json

    # 提取JSON中的各个字段
    filename = data.get('filename')
    username = data.get('username')
    with get_db() as db:
        old_collect = db.query(Collect).filter(Collect.username == username,Collect.filename == filename).first()
        print(old_collect)
        if old_collect:
            return jsonify({"flag": "Failure"})
        else:
            new_collect = Collect(username=username, filename=filename)
            # 添加到会话
            db.add(new_collect)
            # 提交会话，将数据保存到数据库
            db.commit()
    return jsonify({"flag": "Success"})