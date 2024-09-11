from IPython.display import display, Image, Audio
from dotenv import load_dotenv

import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
import time
from openai import OpenAI
import os
import requests


load_dotenv()
client = OpenAI()


video = cv2.VideoCapture("../CjenmVectorStore/wedding_video.mp4")

base64Frames = []
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))


# display_handle = display(None, display_id=True)
# for img in base64Frames:
#     display_handle.update(Image(data=base64.b64decode(img.encode("utf-8"))))
#     time.sleep(0.025)


PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "이것은 제가 업로드하려는 동영상의 프레임들입니다. 동영상과 함께 업로드할 수 있는 매력적인 설명을 작성해 주세요.",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0:50:10]),
        ],
    },
]
params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 200,
}

result = client.chat.completions.create(**params)
print(result.choices[0].message.content)