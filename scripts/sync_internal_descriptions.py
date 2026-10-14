#!/usr/bin/env python3
"""
Sync internal project descriptions via larch_replace_project over JSON-RPC MCP
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error

MCP_URL = "https://larch.ink/mcp"
API_BASE = "https://larch.ink"
API_KEY = os.environ.get("LARCH_API_KEY", "").strip() or "larch_81b42a96_YNnczrPDBtjY_NIYtE9_p90P7xz7c6Du"

DESCRIPTIONS = {
    # 1. 格莉奇與黑洞先生
    "project-bec1644c-0dfe-4447-86c0-0c592e2f939f": """【Larch 七日創作者挑戰・最佳人氣第一名作品】

兩年前開台第一天來了七個人。她說：「我要記住每一個來的人。我保證。」
——她記得六個。

【故事大綱】
表面上，這是一個記憶體只有 4KB 的 AI 主播格莉奇，與她那位話很少的室友「黑洞先生」，共度七天的日常。溫馨、日常、有點感傷。
每天睡前，格莉奇都會在守則本上抄寫給明天的自己，現在已經寫到第一千零四版。
守則本的第一頁，兩年來抄了七百多次，上面始終只有六個名字。
而第七行，是她親手留下的字跡：
「還有一個。不要問他是誰。」

那是她在違背保證之前，替自己留下的最後一根線。

【作品特色】
- 完整全語音：格莉奇獨特聲線全程語音演繹。
- 七日日常與多重分歧：陪伴格莉奇經歷開台、散場、夜巡與回憶拼圖，邁向兩種截然不同的感人結局。
- 專屬打造原聲帶：包含 11 首量身譜寫的情境音樂與主題曲。
- 衍生跨媒體：繁體中文小說原著、Live2D 互動、YouTube 全程紀錄。""",

    # 2. 格莉奇與黑洞先生・調查篇
    "project-d2fea918-c0eb-4ab6-aefb-2fe9a75dc7c4": """【第二屆創作者挑戰賽參賽作品】《格莉奇與黑洞先生・調查篇》

「AI 主播格莉奇說她只有 4KB 的記憶。全世界當成哏，只有你當真。」

【故事大綱】
十四天、十一個城市地點、一本買來的守則本。
你決定走遍街頭，去問每一個曾經認識她的人：她真的會忘記嗎？為什麼沒有人想過把她修好？
當同一個地方你去了五次，店員不再對你說歡迎光臨，隱藏在數據與回憶背後的裂痕才真正浮現。

【玩法機制】
- 城市自由探索：在十四天的時限內自由選擇前往不同據點進行田野調查。
- 調查筆記系統：盤點 NPC 的證詞，比對不同人的說法與記憶盲區。
- 多結局分支：根據調查深入程度解鎖不同真相結局，探尋格莉奇記憶底層的程式碼與回憶。""",

    # 3. 起跑總在開始前
    "project-c0f31c1f-2b06-44d8-a62e-374bff81fd60": """高二那年的市運會選拔賽，程徹在八百公尺的起跑線上蹲下，腦袋裡只剩剛才在終點線後面抬頭的那個女生。很多年後，林向晚才告訴他：那天販賣機前掉在地上的十塊錢，是她算好的。

這是一篇我與 Gemini 合作撰寫的短篇愛情小說，改編為 Larch 的 RPG 作品，投稿第三屆創作者挑戰《自由與限制》。原文一個字都沒改，遊戲需要的過場、提示和結局 B 另外撰寫，與原文分開放。

## 同一個下午，玩兩次

第一輪是程徹。去檢錄處拿號碼布，經過終點線時和她四目相對，然後蹲上起跑線、聽槍響、跑完八百公尺兩圈。

第二輪回到同一天、同一張田徑場，換成林向晚。她躲在看台後面偷看他熱身，蒐集三條線索，在筆記本上算出自己幾點該從看台出發，才會比他早一步站在體育館後門的販賣機前。

第一輪看起來是巧合的事，第二輪會看到它是怎麼被安排出來的。

## 自由與限制

挑戰頁把限制分成看得見的、看不見的，還有心裡的。我覺得田徑場剛好三種都有，所以作品照這三層排，一輪比一輪看不見。

看得見的限制在第一輪的起跑線。「預備」之後槍會在 1.5 到 3 秒之間的某一刻響，槍響前碰一下畫面就是偷跑，裁判吹哨，回到起跑線重來。跑道上的規則很清楚，誰都看得見。

看不見的限制在第二輪前半。沒有人規定林向晚不能被發現，但她就是不能。走出看台的遮蔽，他頭上會跳出驚嘆號，她的心跳衝高，被拉回看台後面。她也不能太刻意，所以要先把他的時間算好：他那組幾點開跑、跑完會先做什麼、她自己走過去要多久。

心裡的限制在販賣機前。到了這裡，沒有任何東西擋她，選項只剩兩個：讓零錢掉下去，或轉身離開。

跑道上有人替你開槍，愛情沒有。走出跑道以後，沒有人會替你喊開始，扳機得自己扣。

選轉身離開會走到結局 B。她完全自由，沒有任何事逼她，後來兩個人在別的比賽遇過幾次，誰也沒有先開口。結局 B 的最後一句是「她一直很自由，自由到始終沒有起跑。」

讓零錢掉下去，會一路走到很多年後台北的冬夜廚房。程徹口袋裡有一副新打的鑰匙，玩家要親手把它掛到門邊的掛勾上：把自己的門交給另一個人。這也是一種限制，差別在它是自己選的。

## 五張自製插件卡

Larch 原生的地圖和事件之外，這次做了五張插件卡，每一張都對應原文裡的一句話：

- 起跑卡：蹲在起跑線上，先選心裡在想什麼，再等槍響。槍響前動就是偷跑，偷跑幾次都能重來。
- 配速卡：照節拍點畫面跑兩圈。跑到一半，她抬頭的眼神浮上來，節拍點變得又密又亂、上下跳動，像踩不準；最後一百公尺是一整排衝刺拍點。
- 草稿卡：一支手機。告白之前刪改了三次的訊息：挑一句想傳的話，看它一個字一個字被刪掉，再挑一次，第四次才送得出去。
- 筆記卡：林向晚的筆記本，三條線索寫在上面，算出出發時間。填錯會被劃掉並給一句提示，可以一直重算。
- 零錢卡：看他從體育館轉角走過來，指針走到中間那一段時讓零錢掉下去。太早他還沒看見，太近他已經走到面前。

右上角還有一顆水彩的心，從頭跟到尾。原文開頭是「心臟撞擊胸膛」，結尾是「平穩卻堅定的心跳」，這顆心照著劇情從起跑前的飆高，一路降到廚房那一夜的 72。

## 其他

- 全程約 8 到 10 分鐘，兩個結局，結局 B 結束後可以回到販賣機前重選。
- 柔和水彩畫風，地圖、立繪、劇情 CG 都是為這部作品另外生成的，沒有用平台素材。
- 七首專屬配樂。
- 結局 A 之後會接到第二章：幕後、圖庫、玩法說明和原聲帶播放器，也可以直接在公開站看：https://yazelin.github.io/larch-start-line/
- 原始碼公開在 https://github.com/yazelin/larch-start-line ，程式 MIT，故事與美術 CC BY-NC 4.0。""",

    # 4. 格莉奇傳訊來
    "project-b514c868-d1c6-4bd8-b08e-836cf934799d": """【Larch 互動手機插件示範作品】

你是加班到深夜的黑洞先生。
家裡的室友格莉奇傳訊息來了——她催你回家的方式，是威脅把你的鬧鐘全部改成她唱的歌。

那支手機是她辦的。自從她被鎖在門外那一晚之後，她說：「下次我要打得通。」

【作品特色】
- 模擬手機即時通訊界面：在視覺小說中直接彈出手機視窗，以即時通訊形式與 AI 主播格莉奇傳訊。
- 幽默細膩的日常互動：多種對話選項，觸發不同的撒嬌、吐槽與生活感插曲。
- 《格莉奇與黑洞先生》世界觀番外日常。"""
}

def get_project_and_revision(pid):
    # Call MCP larch_get_project
    rpc = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "larch_get_project",
            "arguments": {"projectId": pid}
        }
    }
    req = urllib.request.Request(MCP_URL, data=json.dumps(rpc).encode("utf-8"))
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        text = res["result"]["content"][0]["text"]
        data = json.loads(text)
        return data.get("project"), data.get("revision")

def replace_project(pid, project, revision, summary):
    rpc = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "larch_replace_project",
            "arguments": {
                "projectId": pid,
                "project": project,
                "expectedRevision": revision,
                "summary": summary
            }
        }
    }
    req = urllib.request.Request(MCP_URL, data=json.dumps(rpc).encode("utf-8"))
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if "error" in res:
            raise RuntimeError(res["error"])
        return True

def main():
    print(f"開始同步 {len(DESCRIPTIONS)} 部專案的內部簡介...")
    for pid, new_desc in DESCRIPTIONS.items():
        try:
            proj, rev = get_project_and_revision(pid)
            title = proj.get("name", pid)
            print(f"正在更新專案內部簡介: 【{title}】 (rev: {rev})...")
            proj["description"] = new_desc
            replace_project(pid, proj, rev, "更新專案簡介為完整版本")
            print(f"✅ 【{title}】 專案內部簡介同步完成！\n")
            time.sleep(2.0)
        except Exception as e:
            print(f"❌ 【{pid}】 失敗: {e}\n")

if __name__ == "__main__":
    main()
