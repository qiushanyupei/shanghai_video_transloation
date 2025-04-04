from flask import Blueprint,request,jsonify
from db.db_init import get_db
import os
from db.db_table import Video,User

fetch_community = Blueprint('fetch_community', __name__)

@fetch_community.route('/fetch_community',methods=['GET'])
def fetch_community_():
    result = []
    with get_db() as db:
        video_info = db.query(Video).filter(Video.is_public == True)
        for video in video_info:
            result.append({
                "name": video.filename,
                "file_path": video.newfilepath
            })
    return jsonify(result)
