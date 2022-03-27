from fastapi import FastAPI, File, UploadFile
from fastapi.params import Form
from starlette.middleware.cors import CORSMiddleware
import speech_recognition as sr
from youtube_transcript_api import YouTubeTranscriptApi
import json
from pytube import YouTube
from moviepy.editor import *
import os


def catclip(namevid: str, pathoutclip: str, startclip: int, endclip: int):
    clip = VideoFileClip(namevid).subclip(startclip, endclip)
    final_clip = concatenate_videoclips([clip])
    final_clip.write_videofile(pathoutclip)


def save_file(filename, data, path):
    p = path + filename
    with open(p, 'wb') as f:
        f.write(data)
    return p


def remove_nois_from_str(str0: str):
    return str0.replace("?", "").replace("!", "").replace("[", "").replace("]", "").replace(" ", "")


def savefile(path: str, data: list):
    out_file = open(path + ".json", "w")
    json.dump(data, out_file, indent=2)
    out_file.close()


def save_data(newitem: str, path: str):
    data = open(path + "data.txt", "a")
    data.write("\n" + newitem + "?")
    data.close()


app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/AudioAnalysis/")
async def create_upload_file(audio_data: UploadFile):
    contents = await audio_data.read()
    p = save_file(audio_data.filename, contents, 'audio\\')
    r = sr.Recognizer()
    with sr.AudioFile(p) as source:
        t = r.record(source)
        t2 = r.recognize_google(t)
    return t2


@app.get("/transcptation/")
async def gettranscptation(idvid: str = Form(...)):
    return YouTubeTranscriptApi.get_transcript(idvid)


@app.post("/savevid/")
async def savevid(idvid: str = Form(...)):
    data = YouTubeTranscriptApi.get_transcript(idvid)
    yt = YouTube("https://www.youtube.com/watch?v=" + idvid)
    stream = yt.streams.get_by_itag(22)
    stream.download("C:/xa/htdocs/webs/vid/")
    path = "C:/xa/htdocs/webs/vid/" + yt.title

    savefile(path, data)
    save_data(yt.title + "?", "C:/xa/htdocs/webs/vid/")
    os.mkdir(path)

    supdata = []
    count = 1
    flag = 1
    startpoint = int(data[0]["start"])

    for item in data:
        if (flag % 5 == 0):
            print(catclip(path + ".mp4", path + "/" + str(count) + ".mp4", startpoint, int(item["start"]) + .7))
            print(supdata)
            savefile(path + "/" + str(count), supdata)
            supdata = []
            startpoint = int(item["start"])
            count += 1
        flag += 1
        supdata.append(item)
    save_data(str(count - 1), path + "/")
    return data

@app.post("/SaveVidWithoutCut/")
async def savevid(idvid: str = Form(...), startpoint: str = Form(...), endpoint: str = Form(...)):
    data = YouTubeTranscriptApi.get_transcript(idvid)
    yt = YouTube("https://www.youtube.com/watch?v=" + idvid)
    stream = yt.streams.get_by_itag(22)
    stream.download("C:/xa/htdocs/webs/vid/")
    path = "C:/xa/htdocs/webs/vid/" + yt.title

    savefile(path, data)
    save_data(yt.title + "?", "C:/xa/htdocs/webs/vid/")
    os.mkdir(path)
