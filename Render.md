## 第一步：在 GitHub 準備好 2 個後端檔案
請進入你的 GitHub 儲存庫（Repository），確認或新增以下兩個檔案在專案的根目錄：

1. 新增檔案：requirements.txt
```
fastapi
uvicorn
yt-dlp
pydantic
```
2. 新增檔案：app.py
```
import yt_dlp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 啟用 CORS 跨來源允許（讓你的 GitHub Pages 可以順利呼叫）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    url: str

# 根目錄健康檢查
@app.get("/")
def home():
    return {"status": "ok", "message": "Guitar API is online"}

# 解析 YouTube 核心路由
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
```

## 第二步：登入 Render 並建立免費 Web Service
1. 前往官網：進入 Render.com，點擊右上角 GET STARTED 或 Sign In。
2. 選擇 GitHub 登入：直接點擊 GitHub 授權登入（免綁信用卡）。
3. 建立新服務：
  - 進入主頁面後，點擊右上角的藍色按鈕 New +。
  - 在選單中選擇 Web Service。
4. 連結 GitHub 儲存庫：
  - 選擇 Build and deploy from a Git repository，點擊 Next。
  - 在 Repository 清單中找到你的專案，點擊右邊的 Connect（若沒看到，點擊下方的 Configure access on GitHub 勾選授權你的專案）。
5. 填寫部署參數（關鍵設定）：
  - Name：輸入 guitar-backend（或任意英文字母）
  - Region：選預設即可（例如 Singapore 或 Oregon）
  - Branch：選擇 main
  - Root Directory：留空不用填
  - Language：選擇 Python 3
  - Build Command：填入：
    ```
    Bash
    pip install -r requirements.txt
    ```
  - Start Command：填入：
    ```
    Bash
    uvicorn app:app --host 0.0.0.0 --port $PORT
    ```
  - Instance Type（費用方案）：往下滾動，務必確認選擇標註 Free（$0/month） 的方案。
6. 點擊建立：點擊頁面最下方的 Create Web Service。
