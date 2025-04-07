from flask import Blueprint,render_template,request,jsonify
from db.db_init import get_db
from db.db_table import User,Video
import os
import subprocess
import shutil
from datetime import datetime,timedelta

new_video = Blueprint('new_video', __name__)
#转换成ffmpeg可以接受的颜色参数
def hex_to_ass_color(hex_color):
    """Convert #RRGGBB to &HBBGGRR& (ASS/SSA format)"""
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]  # Remove #
    if len(hex_color) != 6:
        raise ValueError("Color must be in #RRGGBB format")
    rr = hex_color[0:2]  # Red
    gg = hex_color[2:4]  # Green
    bb = hex_color[4:6]  # Blue
    return f"&H{bb}{gg}{rr}&"  # Reorder to BBGGRR

def embed_subtitle(input_video, subtitle_file, output_video,color,font_size,font_name,bold,italic,underline):
    """
    使用FFmpeg硬嵌入SRT字幕到视频

    参数:
        input_video: 输入视频路径
        subtitle_file: 字幕文件路径
        output_video: 输出视频路径
    """
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-vf', f"subtitles={subtitle_file}:force_style="
               f"'Bold={bold},"  # 粗体(1=启用)
               f"Italic={italic},"  # 斜体(1=启用)
               f"Underline={underline},"  # 下划线(1=启用)
               f"FontName={font_name},"
               f"FontSize={font_size},"
               f"PrimaryColour={color},"
               "OutlineColour=&H000000&,"
               "BorderStyle=1'",
        '-c:a', 'copy',
        '-y',  # 自动覆盖输出文件
        output_video
    ]

    try:
        # 运行命令并捕获输出
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("字幕嵌入成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误发生，返回码: {e.returncode}")
        print("FFmpeg错误输出:")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"其他错误: {str(e)}")
        return False

@new_video.route('/new_video',methods=['POST'])
def new_video_():
    data = request.json

    # 提取JSON中的各个字段
    srt = data.get('srt')
    styles = data.get('styles')  # styles本身是一个JSON对象
    subtitle_path = data.get('subtitlePath')
    video_path = data.get('videoPath')
    font_size = styles.get('fontSize')
    color = styles.get('color')
    font_family = styles.get('fontFamily')
    bold = styles.get('bold')
    italic = styles.get('italic')
    underline = styles.get('underline')
    #覆写服务器的srt文件
    with open(subtitle_path, 'w', encoding='utf-8') as file:
        file.write(srt)

    name, extension = os.path.splitext(video_path)
    # 改写新视频的路径
    output_dir = f"{name}_new{extension}"

    #改动数据库中的
    with get_db() as db:
        video_info = db.query(Video).filter(Video.filepath == video_path).first()
        video_info.fontsize = font_size
        video_info.color = color
        video_info.fontfamily = font_family
        video_info.bold = bold
        video_info.italic = italic
        video_info.underline = underline
        video_info.upload_time = datetime.utcnow() + timedelta(hours=8)
        db.commit()

    success = embed_subtitle(
        input_video=video_path,
        subtitle_file=subtitle_path,
        output_video=output_dir,
        font_size=font_size,
        color=hex_to_ass_color(color),
        font_name=font_family,
        bold=int(bold),
        italic=int(italic),
        underline=int(underline)
    )
    #把原始视频的内容覆盖，暂时决定不需要
    # shutil.copyfile(output_dir, video_path)
    if success:
        return jsonify({"success": True, "video_url": output_dir})
    else:
        return jsonify({"success": False, "video_url": output_dir})
