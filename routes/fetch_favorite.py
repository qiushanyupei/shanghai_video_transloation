from flask import Blueprint,request,jsonify
from db.db_init import get_db
import os
from db.db_table import Video,User,Collect

fetch_favorite = Blueprint('fetch_favorite', __name__)

@fetch_favorite.route('/fetch_favorite',methods=['GET'])
def fetch_favorite_():
    # formdata数据接受方式
    username = request.args.get("username", "")
    result = []
    with get_db() as db:
        collect_info = db.query(Collect).filter(Collect.username == username)
        for collect in collect_info:
            video = db.query(Video).filter(Video.filename == collect.filename).first()
            result.append({
                "name": video.filename,
                "file_path": video.newfilepath
            })
    return jsonify(result)
