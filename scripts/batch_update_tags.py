#!/usr/bin/env python3
"""
Batch update Larch marketplace listing tags for all works
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error

API_BASE = "https://larch.ink"

TAGS_MAPPING = {
    # 1. 十一分鐘
    "project-fc97ad09-681c-47f9-80b9-e12753877b9c": [
        "視覺小說", "第三屆創作者挑戰", "RPG", "科幻", "多結局", "戰鬥", "終端機解謎"
    ],
    # 2. 王子姬 Prince Hime
    "project-6516bec7-4053-4a7c-a45e-2d739be40b12": [
        "視覺小說", "RPG", "養成", "虛擬寵物", "奇幻", "多結局"
    ],
    # 3. 唐詩小旅行：過故人莊
    "project-ac006859-4f72-4956-a83e-ddc2ed9a1c0a": [
        "視覺小說", "互動教材", "兒童教育", "全語音", "國語生字", "古詩考證"
    ],
    # 4. 起跑總在開始前
    "project-c0f31c1f-2b06-44d8-a62e-374bff81fd60": [
        "視覺小說", "第三屆創作者挑戰", "校園愛情", "RPG", "雙視角", "多結局", "專屬配樂"
    ],
    # 5. 仙泉·香布纏．無雙
    "project-e35e734b-478d-458b-9221-294f81398b59": [
        "RPG", "動作戰鬥", "無雙割草", "三國改編", "娘溺泉", "多人連線"
    ],
    # 6. 洛泉．袁真跡
    "project-6abb2d2f-123f-438c-8a36-57d914a42e52": [
        "視覺小說", "三國改編", "娘溺泉", "歷史改寫", "史料考證", "多卷長篇", "專屬配樂"
    ],
    # 7. 仙泉．香布纏
    "project-1980dcc9-13b3-451c-8bf6-71b05bd5bfa9": [
        "視覺小說", "三國改編", "娘溺泉", "歷史改寫", "多結局", "專屬配樂"
    ],
    # 8. 小遊戲集合・示範
    "project-892df123-4806-4343-95be-44f1c65056e4": [
        "小遊戲", "插件示範", "教學範本", "開源", "互動遊樂園"
    ],
    # 9. 格莉奇與黑洞先生・調查篇
    "project-d2fea918-c0eb-4ab6-aefb-2fe9a75dc7c4": [
        "視覺小說", "第二屆創作者挑戰", "解謎調查", "科幻", "多結局", "AI主播"
    ],
    # 10. 晚霞是舌尖最後的刺痛
    "project-8cb1ab7e-891c-46b4-bd38-df29060e5717": [
        "視覺小說", "第二屆創作者挑戰", "背包解謎", "調酒合成", "多結局", "探索解謎"
    ],
    # 11. 淡藍與草木灰綠的雨幕
    "project-0b41ff6f-6947-464b-9ed2-c2cd05b87a5a": [
        "視覺小說", "第二屆創作者挑戰", "青梅竹馬", "背包解謎", "全語音", "多結局"
    ],
    # 12. 最終遺忘的橘色餘燼
    "project-904c48a1-2797-4a7e-916a-75b1117e6211": [
        "視覺小說", "第二屆創作者挑戰", "背包解謎", "感官聯覺", "多結局", "全語音"
    ],
    # 13. Larch 直播共創板：簡報、共創與練習
    "project-5e31d391-c23f-44aa-9811-c20cc2c5d12a": [
        "簡報插件", "教學範本", "直播共創", "開源樣式"
    ],
    # 14. 咒泉．白帝城
    "project-4d2e8ae0-85c4-40ef-ba7b-85acc88290c5": [
        "視覺小說", "三國改編", "娘溺泉", "歷史改寫", "短篇故事"
    ],
    # 15. 空白也有質地
    "project-8dd92abf-410b-4f7d-a00f-8492c7193310": [
        "視覺小說", "森林宇宙", "童話治癒", "多結局", "角色故事"
    ],
    # 16. 還沒送到的信
    "project-141b0223-9d1b-4077-8a5b-8b036485ee6a": [
        "視覺小說", "森林宇宙", "療癒日常", "多結局", "全語音", "角色故事"
    ],
    # 17. 格莉奇傳訊來
    "project-b514c868-d1c6-4bd8-b08e-836cf934799d": [
        "視覺小說", "手機插件", "AI即時對話", "格莉奇", "日常互動"
    ],
    # 18. 咒泉．三結義
    "project-6e031e3a-f508-4d77-aaa2-795edb6a80f4": [
        "視覺小說", "三國改編", "娘溺泉", "全語音", "多結局", "歷史改寫", "爆笑喜劇"
    ],
    # 19. 格莉奇與黑洞先生
    "project-bec1644c-0dfe-4447-86c0-0c592e2f939f": [
        "視覺小說", "七日創作者挑戰", "全語音", "科幻治癒", "AI主播", "多結局"
    ],
}

def update_project_tags(project_id, tags, api_key, max_retries=3):
    url = f"{API_BASE}/api/agent/projects/{project_id}/publish"
    data = json.dumps({"tags": tags}).encode("utf-8")
    
    for attempt in range(max_retries):
        req = urllib.request.Request(url, data=data, method="PATCH")
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0 (compatible; LarchShowcaseBot/1.0)")
        
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                game = res_data.get("game", {})
                title = game.get("title", project_id)
                updated_tags = game.get("tags", [])
                print(f"✅ [成功] {title}")
                print(f"   新標籤: {updated_tags}")
                return True
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            if e.code == 429:
                wait_sec = (attempt + 1) * 3
                print(f"⏳ [限流 429] {project_id} 等待 {wait_sec} 秒後重試 (第 {attempt+1} 次)...")
                time.sleep(wait_sec)
                continue
            print(f"❌ [失敗] {project_id}: HTTP {e.code} - {err_body}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"❌ [異常] {project_id}: {e}", file=sys.stderr)
            return False
    return False

def fetch_current_published(api_key):
    url = f"{API_BASE}/api/agent/published"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; LarchShowcaseBot/1.0)")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {w.get("projectId"): w for w in data.get("works", [])}
    except Exception as e:
        print(f"Warning: could not fetch current published works: {e}", file=sys.stderr)
        return {}

def main():
    api_key = os.environ.get("LARCH_API_KEY", "").strip()
    if not api_key:
        print("LARCH_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)
        
    print(f"取得目前作品狀態並檢查標籤差分...")
    current_works = fetch_current_published(api_key)
    
    success_count = 0
    skipped_count = 0
    for pid, new_tags in TAGS_MAPPING.items():
        curr_work = current_works.get(pid, {})
        curr_tags = curr_work.get("tags", [])
        title = curr_work.get("title", pid)
        
        if sorted(curr_tags) == sorted(new_tags):
            print(f"⏩ [已是最新] {title}: {curr_tags}")
            skipped_count += 1
            continue
            
        print(f"\n🔄 準備更新: {title}")
        print(f"   原標籤: {curr_tags}")
        print(f"   新標籤: {new_tags}")
        if update_project_tags(pid, new_tags, api_key):
            success_count += 1
        time.sleep(2.0)
        
    print(f"\n標籤更新統計：成功更新 {success_count} 部，已是最新跳過 {skipped_count} 部，共 {len(TAGS_MAPPING)} 部。")

if __name__ == "__main__":
    main()

