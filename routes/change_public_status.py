from flask import Blueprint,request,jsonify
from db.db_init import get_db
import os
from db.db_table import Video,User,Collect

change_public_status = Blueprint('change_public_status', __name__)

@change_public_status.route('/change_public_status',methods=['POST'])
def change_public_status_():
    #json接受形式
    data = request.json

    # 提取JSON中的各个字段
    filename = data.get('filename')
    with get_db() as db:
        video = db.query(Video).filter(Video.filename == filename).first()
        if video:
            video.is_public = not video.is_public
            if video.is_public == False:
                collects = db.query(Collect).filter(Collect.filename == filename)
                for collect in collects:
                    db.delete(collect)
            db.commit()
        else:
            print("搜不到这个文件")
    return jsonify({"flag": "Success"})