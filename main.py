import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl, validator
from fastapi.middleware.cors import CORSMiddleware

from content_producer import ContentData, ContentProducer
from generate_vid.gen import generate_video_internal
from generate_vid.script import gen_script_from_text
import uuid

content_producer = ContentProducer()

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="./frontend/dist", html=True), name="static")


class VidGenerationRequest(BaseModel):
    text: str


class VidGenerationResponse(BaseModel):
    video_url: str
    script: str


@app.post("/generate_video/", response_model=VidGenerationResponse)
async def generate_video(vid: VidGenerationRequest):
    try:
        # Generate video and return absolute directory
        vid_dir = generate_video_internal(vid.text)
        script = gen_script_from_text(vid.text)
        # creates the video, written to final_clip_0.mp4 or final_clip_1.mp4
        content_producer.invoke([ContentData("tech_science", script, vid_dir)])
        # create the url to the video
        out_dir1 = "out/final_clip_0.mp4"
        out_dir2 = "out/final_clip_1.mp4"
        vid_dir = out_dir1 if os.path.exists(out_dir1) else out_dir2
        # move the video to the static directory (outdata) and rename with unique name
        unique_name = uuid.uuid4().hex
        vid_dir2 = f"outdata/{unique_name}.mp4"
        # move the video to the outdata directory
        os.rename(vid_dir, vid_dir2)
        return VidGenerationResponse(video_url=vid_dir2, script=script)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
