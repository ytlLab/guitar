# guitar
├── app.py              # 後端 API (使用 Python FastAPI / Gradio)</br>
├── requirements.txt    # 依賴套件清單</br>
└── index.html          # 先前做好的吉他譜前端介面</br>

[GitHub Repo] (存放你的前後端開源專案程式碼)
     │
     ▼ 自動同步部署
[Hugging Face Spaces (免費 Python 後端)]
  1. 接收前端傳來的 YouTube 網址
  2. 後端使用 yt-dlp 下載音訊串流
  3. 使用開源和弦辨識模型 (如 BTC / Chordino) 抓取和弦拍點
  4. 使用開源 Whisper 模型取得歌詞對位
     │
     ▼ 回傳標準吉他譜 JSON
[GitHub Pages / 前端網頁] (漂亮的吉他彈唱介面，支援一鍵移調與列印)
