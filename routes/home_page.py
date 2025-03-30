from flask import Blueprint,render_template,request,jsonify,url_for
from db.db_init import get_db
import os
from db.db_table import Video,User
from model.const import *
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import librosa


home = Blueprint('home', __name__)

#音画分离
def extract_audio(video_path, output_audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path, codec="pcm_s16le")  # WAV格式，兼容性更好
    audio.close()
    video.close()

#切分音频为5秒一段
def split_audio(audio_path, chunk_length_ms=3000, output_dir="./static/chunks"):
    audio = AudioSegment.from_wav(audio_path)
    os.makedirs(output_dir, exist_ok=True)

    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        start = i
        end = i + chunk_length_ms
        chunk = audio[start:end]
        chunk_name = f"{output_dir}/chunk_{i}.wav"
        chunk.export(chunk_name, format="wav")
        chunks.append({"path": chunk_name, "start": start / 1000, "end": end / 1000})  # 转为秒
    return chunks


def seconds_to_srt_time_format(seconds):
    """
    将秒数转换为SRT格式的时间戳（小时:分钟:秒数,毫秒数）
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

@home.route('/',methods=['GET','POST'])
def home_page():
    if request.method == 'POST':
        file = request.files['file']#有request.files和request.form两种形式，前端和后端交互时由Flask区分
        username = request.form.get('username')
        # 转换为视频存储的绝对路径
        absolute_path_video = os.path.join(os.path.join(os.path.dirname(__file__), "..", UPLOAD_VIDEO),file.filename)
        # print(os.path.dirname(__file__))
        # print(os.path.join(os.path.dirname(__file__), "..", UPLOAD))
        # print(absolute_path_video)
        # print(os.path.join(os.path.join(os.path.dirname(__file__), ".", UPLOAD),file.filename))
        # 保存文件到指定目录
        file.save(absolute_path_video)
        new_path = os.path.join(UPLOAD_VIDEO, file.filename)

        extract_audio("./static/上海话测试.mp4", AUDIO)
        audio_chunks = split_audio(AUDIO)
        checkpoint_path = './checkpoint-1020'  # 你的 checkpoint 文件夹
        processor = Wav2Vec2Processor.from_pretrained(checkpoint_path)
        model = Wav2Vec2ForCTC.from_pretrained(checkpoint_path)
        model.eval()

        def transcribe_chunk(chunk_path):
            # 读取为音频本身的流状格式
            audio, sr = librosa.load(chunk_path, sr=16000)
            """对音频进行解码"""
            inputs = processor(audio, return_tensors="pt", sampling_rate=16000)
            logits = model(**inputs).logits
            pred_ids = torch.argmax(logits, dim=-1)
            text = processor.batch_decode(pred_ids, skip_special_tokens=True)
            print(text[0])
            return text[0] if text else ""

        for chunk in audio_chunks:
            text = transcribe_chunk(chunk["path"])  # 将音频文件翻译成文字
            chunk["text"] = text



        with open(SRT, "w", encoding="utf-8") as f:
            for i, seg in enumerate(audio_chunks, 1):  # 因为SRT要求开始的index为1
                start_time = seconds_to_srt_time_format(seg['start'])
                end_time = seconds_to_srt_time_format(seg['end'])
                f.write(f"{i}\n{start_time} --> {end_time}\n{seg['text']}\n\n")

        del model
        del processor
        srt_path = SRT.replace("./", "")
        #还需要通过username查找出user_id
        with get_db() as db:
            user = db.query(User).filter(User.username == username).first()
            new_file = Video(user_id = user.id,filename=file.filename,filepath=new_path,srtpath=srt_path)
            # 添加到会话
            db.add(new_file)
            # 提交会话，将数据保存到数据库
            db.commit()
            return jsonify({"flag": "Success", "file_path": new_file.filepath,"subtitle_path":new_file.srtpath})
    elif request.method == 'GET':
        return render_template("主界面.html")