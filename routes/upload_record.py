from flask import Blueprint,request,jsonify
from db.db_init import get_db
import os
from db.db_table import Video,User

upload_record = Blueprint('upload_record', __name__)

@upload_record.route('/upload_record',methods=['GET'])
def upload_record_():
    #formdata数据接受方式
    username = request.args.get("username", "")
    #第一个参数是键名，第二个参数是键不存在时返回的默认值
    result = []
    with get_db() as db:
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            # 处理用户不存在的情况，例如返回错误信息或抛出异常
            raise ValueError(f"用户 {username} 不存在")
        else:
            video_info = db.query(Video).filter(Video.user_id == user.id)
            for video in video_info:
                result.append({
                    "name": video.filename,
                    "file_path": video.filepath,
                    "subtitle_path": video.srtpath,
                    "font_size": video.fontsize,
                    "color": video.color,
                    "is_public_flag": video.is_public
                })
    return jsonify(result)