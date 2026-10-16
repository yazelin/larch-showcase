# Larch Showcase & Analytics Dashboard

林亞澤（@yaze）的 Larch 作品數據同步與看板。

**公開展示頁在 blog 的 [/larch/](https://yazelin.github.io/larch/)**：版面跟 blog 同一套，數字與簡介每次開頁從這個 repo 的 `data/works.json` 讀（同網域）。所以 `data/works.json` 的欄位名稱（`summary.total_*`、`works[].id/title/description/coverUrl/playUrl/tags/publishedAt/marketRank/views/plays/likes/comments`）改了，blog 那頁會跟著壞。這裡的 `index.html` 只做轉址，原本的看板在 `dashboard.html`。

透過 GitHub Actions 每天定時自動巡檢作品連結、呼叫 Larch 官方 API 同步最新數據（總瀏覽數、遊玩次數、獲得愛心、讀者留言、章節節點數），並自動發佈至 GitHub Pages。

---

## 🌟 核心特色

1. **專屬作品展示牆（GitHub Pages）**：
   - 沉浸式現代設計，支援暗黑 / 淺色模式切換。
   - KPI 統計卡片：累積總瀏覽（10,000+）、總遊玩次數、獲贈愛心、留言數與未回覆待覆提示。
   - 快速篩選與排序：依瀏覽數、遊玩數、愛心、發布日期排序；支援標籤（視覺小說、創作者挑戰等）與即時文字搜尋。
   - 作品卡片：高清封面、AI 揭露標籤（重度 AI / 局部 AI / 純手繪）、版本號、章節卡片數明細彈窗、一鍵直達「立即遊玩」。
2. **GitHub Actions 每日排程巡檢**：
   - 每天固定於台灣時間上午 10:00（UTC 02:00）自動喚醒執行。
   - 逐一瀏覽巡檢每一部作品的公開遊玩頁面（`play/market/...`），紀錄 HTTP 狀態碼與網路延遲。
   - 呼叫 `https://larch.ink/api/agent/published` 抓取最新官方數據。
   - 比對前一日歷史數據，計算「今日新增瀏覽 / 愛心 / 留言」。
3. **零外部依賴、極致輕量**：
   - 數據收集腳本使用 Python 3 原生標準庫（`urllib`、`json`、`time`），無須 `pip install` 任何套件，Actions 秒級完成。
   - 網頁前端使用純靜態 HTML + Tailwind CSS + Vanilla JS，讀取 `data/works.json`，免後端伺服器。
4. **機密安全保護**：
   - Larch API Key 存放於 GitHub Secrets（`LARCH_API_KEY`），不在儲存庫代碼或前端暴露 Bearer Token。

---

## 📁 專案架構

```
larch-showcase/
├── .github/
│   └── workflows/
│       └── update-stats.yml    # GitHub Actions：每日定時排程、巡檢抓取數據與部署 Pages
├── scripts/
│   └── fetch_stats.py          # 核心 Python 腳本：瀏覽作品、呼叫 API、計算 Delta、生成摘要
├── data/
│   ├── works.json              # 當前所有作品最新數據與當日巡檢結果
│   └── history.json            # 每日數據快照與歷史變化追蹤
├── index.html                  # 轉址到 yazelin.github.io/larch/(公開展示頁搬進 blog)
├── dashboard.html              # 作者自己看的數據看板(原本的展示頁)
├── style.css                   # 展示頁面客製化樣式與特效
├── app.js                      # 前端展示邏輯、過濾、排序與彈窗控制
├── .gitignore
├── LICENSE                     # MIT License
└── README.md
```

---

## ⚙️ GitHub 設定流程

### 1. 設定 Larch API Key (GitHub Secret)
1. 進入本 GitHub Repository 頁面。
2. 點選 **Settings** > **Secrets and variables** > **Actions**。
3. 點選 **New repository secret**：
   - **Name**: `LARCH_API_KEY`
   - **Secret**: 填入你的 Larch Bearer Token（例如 `larch_81b4...`）。
4. 點選 **Add secret** 儲存。

### 2. 開啟 GitHub Pages
1. 進入 Repository 的 **Settings** > **Pages**。
2. 在 **Build and deployment** > **Source** 下拉選單中，選擇 **GitHub Actions**。
3. 當 Actions 工作流程執行完畢後，即可於專屬網址瀏覽展示頁面（例如 `https://yazelin.github.io/larch-showcase/`）。

### 3. 手動觸發測試
如果不希望等待每天排程，可隨時手動觸發：
1. 點選 GitHub 儲存庫上方的 **Actions** 分頁。
2. 在左側清單選擇 **Daily Larch Works Sync & Showcase Deploy**。
3. 點選右側 **Run workflow** 按鈕即可立即執行巡檢與數據同步。

---

## 💻 本地測試與開發

1. **抓取最新數據**：
   ```bash
   LARCH_API_KEY="your_api_key_here" python3 scripts/fetch_stats.py
   ```
2. **本地啟動預覽**：
   ```bash
   python3 -m http.server 8000
   ```
   在瀏覽器開啟 `http://localhost:8000` 即可預覽展示頁面。

---

## 📄 License

MIT © 林亞澤 (Yaze Lin)

---

作者：[GitHub](https://github.com/yazelin) | [Facebook](https://www.facebook.com/yaze.lin.gm) | [Buy Me a Coffee](https://buymeacoffee.com/yazelin)
