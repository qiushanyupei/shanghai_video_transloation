# import subprocess
# def hex_to_ass_color(hex_color):
#     """Convert #RRGGBB to &HBBGGRR& (ASS/SSA format)"""
#     if hex_color.startswith("#"):
#         hex_color = hex_color[1:]  # Remove #
#     if len(hex_color) != 6:
#         raise ValueError("Color must be in #RRGGBB format")
#     rr = hex_color[0:2]  # Red
#     gg = hex_color[2:4]  # Green
#     bb = hex_color[4:6]  # Blue
#     return f"&H{bb}{gg}{rr}&"  # Reorder to BBGGRR
# def embed_subtitle(input_video, subtitle_file, output_video,font_size,color):
#     """
#     使用FFmpeg硬嵌入SRT字幕到视频
#
#     参数:
#         input_video: 输入视频路径
#         subtitle_file: 字幕文件路径
#         output_video: 输出视频路径
#     """
#     cmd = [
#         'ffmpeg',
#         '-i', input_video,
#         '-vf', f"subtitles={subtitle_file}:force_style="
#                f"'FontSize={font_size},"
#                f"PrimaryColour={color},"
#                "OutlineColour=&H000000&,",
#         '-c:a', 'copy',
#         '-y',  # 自动覆盖输出文件
#         output_video
#     ]
#
#     try:
#         # 运行命令并捕获输出
#         result = subprocess.run(
#             cmd,
#             check=True,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         print("字幕嵌入成功！")
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"错误发生，返回码: {e.returncode}")
#         print("FFmpeg错误输出:")
#         print(e.stderr)
#         return False
#     except Exception as e:
#         print(f"其他错误: {str(e)}")
#         return False
#
#
# # 使用示例
# success = embed_subtitle(
#     input_video='../static/上海话测试.mp4',
#     subtitle_file='../static/output_上海话测试.srt',
#     output_video='../static/output_new.mp4',
#     font_size="24px",
#     color=hex_to_ass_color("#ff0000")
# )
#
# if success:
#     print("处理完成！输出文件: output.mp4")
# else:
#     print("处理失败，请检查错误信息")
import os
video_path = "static\上海话测试.mp4"
# file_path, file_name = os.path.split(video_path)
# print(video_path)
# print(file_path)
# 分离文件名和扩展名
name, extension = os.path.splitext(video_path)
print(name)
print(extension)
#
# # 添加 "_new" 到文件名中
# new_file_name = f"{name}_new{extension}"