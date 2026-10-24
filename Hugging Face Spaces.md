Hugging Face Spaces 提供永久免費的 Python 伺服器環境，非常適合用來跑 FastAPI 與 yt-dlp。

1. 註冊並建立 Space：
- 前往 Hugging Face 註冊並登入帳號。
- 點擊右上角頭像，選擇 New Space。
- 設定資訊：
  - Space name：例如 youtube-guitar-backend
  - Space SDK：選擇 Docker（選擇 Blank Docker）或 Gradio（若選擇 Docker 最乾淨穩定）。
  - Space Hardware：選擇預設的 Free CPU（免費）。
  - 隱私權選擇 Public。
  - 點擊 Create Space。

2. 上傳後端檔案：
在該 Space 的 Files 標籤頁中，新增以下兩個檔案：

- 檔案 1：requirements.txt
```
fastapi
uvicorn
yt-dlp
pydantic
```
- 檔案 2：Dockerfile
```
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```
- 檔案 3：app.py
```
import yt_dlp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 允許 GitHub Pages 呼叫
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    url: str

@app.post("/analyze")
def analyze(data: RequestData):
    try:
        # 使用 yt-dlp 解析 YouTube 真實影片資訊
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=False)
            title = info.get('title', '未知歌曲')
            uploader = info.get('uploader', '未知歌手')

        # 依據抓到的正確歌名回傳吉他譜（可在此擴充 BTC 音訊和弦模型）
        sample_tab = f"""【歌曲資訊】
```
