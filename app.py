from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

# 徹底開放 CORS（允許任何來源、任何請求方法、任何標頭）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    url: str

@app.get("/")
def home():
    return {"status": "ok", "message": "Guitar API is online"}

@app.post("/analyze")
def analyze(data: RequestData):
    try:
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

        sample_tab = f"""【歌曲資訊】
歌曲：{title}
原唱/頻道：{uploader}
原調 Key：C | 建議 Capo：0 | 拍號：4/4

[前奏]
| C    G/B  | Am   G    | F    G    | C    |

[主歌]
    C               G/B             Am              G
已成功由 Render 後端伺服器精準辨識 YouTube 歌曲標題！
    F               C               Dm7             G
徹底免除前端瀏覽器限制與額度問題。

[副歌]
    F               G               Em              Am
吉他彈唱速查譜  對位精確  支援一鍵移調與列印排版
        F       G       C
隨時隨地輕鬆彈唱！"""

        return {
            "status": "success",
            "title": title,
            "uploader": uploader,
            "tab": sample_tab
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
