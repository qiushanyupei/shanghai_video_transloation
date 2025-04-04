from flask import Blueprint,request,jsonify
from db.db_init import get_db
import os
from db.db_table import Video,User,Collect

cancel_favorite = Blueprint('cancel_favorite', __name__)

@cancel_favorite.route('/cancel_favorite',methods=['POST'])
def cancel_favorite_():
    #json接受形式
    data = request.json

    # 提取JSON中的各个字段
    filename = data.get('filename')
    username = data.get('username')
    if username is None:
        print("username is None")
    if filename is None:
        print("filename is None")
    with get_db() as db:
        old_collect = db.query(Collect).filter(Collect.username == username,Collect.filename == filename).first()
        if old_collect:
            db.delete(old_collect)
            db.commit()
            print("Success")
            return jsonify({"flag": "Success"})
        else:
            pass
            # new_collect = Collect(username=username, filename=filename)
            # # 添加到会话
            # db.add(new_collect)
            # # 提交会话，将数据保存到数据库
            # db.commit()
    return jsonify({"flag": "Failure"})