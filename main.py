from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl, validator
from fastapi.middleware.cors import CORSMiddleware

from generate_vid.gen import generate_video_internal
from generate_vid.script import gen_script_from_text

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
        return VidGenerationResponse(video_url=vid_dir, script=script)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
