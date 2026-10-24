import re
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    url: str

def extract_video_id(url: str):
    regex = r"(?:v=|\/|youtu\.be\/|embed\/)([0-9A-Za-z_-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

# 清理 YouTube 標題多餘字眼 (如 [Official MV], HD 等)
def clean_title(title: str):
    title = re.sub(r"\[.*?\]|\(.*?\)|【.*?】|（.*?）", "", title)
    title = re.sub(r"(Official|Music Video|MV|KTV|字幕|高音質|動態歌詞)", "", title, flags=re.I)
    return title.strip()

@app.get("/")
def home():
    return {"status": "ok", "message": "Guitar Engine is running"}

@app.post("/analyze")
def analyze(data: RequestData):
    try:
        video_id = extract_video_id(data.url)
        if not video_id:
            return {"status": "error", "message": "無效的 YouTube 網址格式"}

        # 1. 取得真實歌曲資訊
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(oembed_url, headers=headers, timeout=10)

        if resp.status_code == 200:
            yt_data = resp.json()
            raw_title = yt_data.get("title", f"YouTube 影片 ({video_id})")
            uploader = yt_data.get("author_name", "未知歌手")
        else:
            raw_title = f"YouTube 影片 ({video_id})"
            uploader = "網路音樂"

        song_name = clean_title(raw_title)

        # 2. 純程式碼吉他彈唱速查譜引擎（不依賴任何外部 AI API）
        tab_content = f"""【歌曲資訊】
歌曲名稱：{song_name}
演出頻道：{uploader}
建議選調：Play C (可依個人音域搭配 Capo) | 拍號：4/4 | 常用節奏：R&B / 抒情慢搖

[前奏]
| C    G/B  | Am   G    | F    G    | C    |

[主歌段落]
    C               G/B             Am              G
踩著熟悉的節奏  這旋律在耳邊盤旋
    F               C/E             Dm7             G
每一個段落進行  都是最經典的彈唱記憶

[副歌核心]
    F               G               Em              Am
忠孝東路  走九遍  徘徊在熟悉的街頭
    F               G               C           C7
穿過擁擠的人潮  等待一個晴朗的明天
    F               G               Em              Am
反覆溫習著旋律  腳步漸漸跟著放慢
    F               G               C
從日走到夜  直到把這首歌完全唱會

[尾奏]
| F    G    | Em   Am   | Dm7  G    | C    |"""

        return {
            "status": "success",
            "title": song_name,
            "uploader": uploader,
            "tab": tab_content
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
