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
        "視覺小說", "第三屆創作者挑戰", "RPG", "科幻", "三結局", "戰鬥", "終端機解謎"
    ],
    # 2. 王子姬 Prince Hime
    "project-6516bec7-4053-4a7c-a45e-2d739be40b12": [
        "視覺小說", "RPG", "養成", "電子雞", "奇幻", "流動性別", "多結局"
    ],
    # 3. 唐詩小旅行：過故人莊
    "project-ac006859-4f72-4956-a83e-ddc2ed9a1c0a": [
        "視覺小說", "互動教材", "兒童教育", "全語音", "國語生字", "古詩考證"
    ],
    # 4. 起跑總在開始前
    "project-c0f31c1f-2b06-44d8-a62e-374bff81fd60": [
        "視覺小說", "第三屆創作者挑戰", "校園愛情", "RPG", "雙視角", "雙結局", "原創音樂"
    ],
    # 5. 仙泉·香布纏．無雙
    "project-e35e734b-478d-458b-9221-294f81398b59": [
        "RPG", "動作戰鬥", "無雙割草", "三國改編", "娘溺泉", "多人連線"
    ],
    # 6. 洛泉．袁真跡
    "project-6abb2d2f-123f-438c-8a36-57d914a42e52": [
        "視覺小說", "三國改編", "娘溺泉", "歷史改寫", "史料考證", "多卷長篇", "原創音樂"
    ],
    # 7. 仙泉．香布纏
    "project-1980dcc9-13b3-451c-8bf6-71b05bd5bfa9": [
        "視覺小說", "三國改編", "娘溺泉", "歷史改寫", "史料考證", "多結局", "原創音樂"
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
        "視覺小說", "第二屆創作者挑戰", "背包解謎", "調酒合成", "雙結局", "探索解謎"
    ],
    # 11. 淡藍與草木灰綠的雨幕
    "project-0b41ff6f-6947-464b-9ed2-c2cd05b87a5a": [
        "視覺小說", "第二屆創作者挑戰", "青梅竹馬", "背包解謎", "全語音", "雙結局"
    ],
    # 12. 最終遺忘的橘色餘燼
    "project-904c48a1-2797-4a7e-916a-75b1117e6211": [
        "視覺小說", "第二屆創作者挑戰", "背包解謎", "感官聯覺", "雙結局", "全語音", "治癒傷感"
    ],
    # 13. Larch 直播共創板：簡報、共創與練習
    "project-5e31d391-c23f-44aa-9811-c20cc2c5d12a": [
        "簡報插件", "教學範本", "直播共創", "小故事練習", "開源樣式"
    ],
    # 14. 咒泉．白帝城
    "project-4d2e8ae0-85c4-40ef-ba7b-85acc88290c5": [
        "視覺小說", "三國改編", "娘溺泉", "歷史改寫", "短篇故事"
    ],
    # 15. 空白也有質地
    "project-8dd92abf-410b-4f7d-a00f-8492c7193310": [
        "視覺小說", "森林宇宙", "童話治癒", "三結局", "角色故事", "短篇"
    ],
    # 16. 還沒送到的信
    "project-141b0223-9d1b-4077-8a5b-8b036485ee6a": [
        "視覺小說", "森林宇宙", "療癒日常", "雙結局", "全語音", "角色故事"
    ],
    # 17. 格莉奇傳訊來
    "project-b514c868-d1c6-4bd8-b08e-836cf934799d": [
        "視覺小說", "手機插件", "AI即時對話", "格莉奇", "日常互動"
    ],
    # 18. 咒泉．三結義
    "project-6e031e3a-f508-4d77-aaa2-795edb6a80f4": [
        "視覺小說", "三國改編", "娘溺泉", "全語音", "多結局", "歷史改寫", "人氣作品"
    ],
    # 19. 格莉奇與黑洞先生
    "project-bec1644c-0dfe-4447-86c0-0c592e2f939f": [
        "視覺小說", "七日創作者挑戰", "人氣第一", "全語音", "科幻治癒", "AI主播", "雙結局"
    ],
}

def update_project_tags(project_id, tags, api_key):
    url = f"{API_BASE}/api/agent/projects/{project_id}/publish"
    data = json.dumps({"tags": tags}).encode("utf-8")
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
        print(f"❌ [失敗] {project_id}: HTTP {e.code} - {e.read().decode('utf-8')}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ [異常] {project_id}: {e}", file=sys.stderr)
        return False

def main():
    api_key = os.environ.get("LARCH_API_KEY", "").strip()
    if not api_key:
        print("LARCH_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)
        
    print(f"開始批次更新 {len(TAGS_MAPPING)} 部作品的市集標籤...")
    success_count = 0
    for pid, tags in TAGS_MAPPING.items():
        if update_project_tags(pid, tags, api_key):
            success_count += 1
        time.sleep(0.3)
        
    print(f"\n更新完成！成功 {success_count} / {len(TAGS_MAPPING)} 部。")

if __name__ == "__main__":
    main()
