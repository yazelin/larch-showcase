#!/usr/bin/env python3
"""
Batch update Larch project & listing descriptions with silent PATCH
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error

API_BASE = "https://larch.ink"

DESCRIPTIONS_UPDATE = {
    # 1. 晚霞是舌尖最後的刺痛 (原本是預設模板字「新的 Larch 視覺小說專案」)
    "project-8cb1ab7e-891c-46b4-bd38-df29060e5717": """【第二屆創作者挑戰賽參賽作品】《晚霞是舌尖最後的刺痛》

「如果世界的味道正在消逝，你會想記住什麼？」

【故事大綱】
沈淮的摯愛安雅是一位才華洋溢的調酒師。然而，一場無法逆轉的神經病變，正在悄悄剝奪她的味覺中樞。
世界的味道對她而言正在一片一片熄滅。為了不讓沈淮擔心，安雅隱瞞了所有病歷，並在調酒檯前歷時三年，研發出一款外觀宛如落日晚霞般絢麗、入口帶著細微刺痛感，卻實為最後神經止痛的告別配方——「晚霞」。

【遊戲特色】
- 探索解謎：穿梭於吧檯、香料儲藏間與臥室梳妝台三大場景。
- 背包合成：使用 Larch 背包系統尋找隱藏的「心型吊墜鑰匙」，解開雕花木盒中的秘密，收集調酒原料與精油。
- 雙結局分歧：一場直面告別的沉靜落幕，與一段拼湊出安雅心意的深情真相。
- 氛圍營造：全自製日落環境背景與沉浸式配樂。""",

    # 2. 格莉奇與黑洞先生 (原本僅 38 字懸念句，擴充為全站第一名完整介紹)
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

    # 3. 格莉奇與黑洞先生・調查篇 (擴充調查探索與多結局引導)
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

    # 4. 起跑總在開始前 (校正 gemin 拼寫筆誤)
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

    # 5. 格莉奇傳訊來 (補充手機模擬通訊插件特色)
    "project-b514c868-d1c6-4bd8-b08e-836cf934799d": """【Larch 互動手機插件示範作品】

你是加班到深夜的黑洞先生。
家裡的室友格莉奇傳訊息來了——她催你回家的方式，是威脅把你的鬧鐘全部改成她唱的歌。

那支手機是她辦的。自從她被鎖在門外那一晚之後，她說：「下次我要打得通。」

【作品特色】
- 模擬手機即時通訊界面：在視覺小說中直接彈出手機視窗，以即時通訊形式與 AI 主播格莉奇傳訊。
- 幽默細膩的日常互動：多種對話選項，觸發不同的撒嬌、吐槽與生活感插曲。
- 《格莉奇與黑洞先生》世界觀番外日常。"""
}

def update_listing_description(project_id, description, api_key, max_retries=3):
    url = f"{API_BASE}/api/agent/projects/{project_id}/publish"
    data = json.dumps({"description": description}).encode("utf-8")
    
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
                print(f"✅ [市集簡介更新成功] {title}")
                return True
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            if e.code == 429:
                wait_sec = (attempt + 1) * 3
                print(f"⏳ [限流 429] {project_id} 等待 {wait_sec} 秒後重試...")
                time.sleep(wait_sec)
                continue
            print(f"❌ [失敗] {project_id}: HTTP {e.code} - {err_body}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"❌ [異常] {project_id}: {e}", file=sys.stderr)
            return False
    return False

def update_internal_project_description(project_id, description, api_key):
    """
    Update project.description internally via PUT /api/agent/projects/:projectId
    """
    get_url = f"{API_BASE}/api/agent/projects/{project_id}"
    req = urllib.request.Request(get_url)
    req.add_header("Authorization", f"Bearer {api_key}")
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            etag = resp.headers.get("ETag")
            p_data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"⚠️ 無法讀取專案內部資料: {e}")
        return False
        
    p_data["description"] = description
    put_data = json.dumps(p_data).encode("utf-8")
    
    put_req = urllib.request.Request(get_url, data=put_data, method="PUT")
    put_req.add_header("Authorization", f"Bearer {api_key}")
    put_req.add_header("Content-Type", "application/json")
    if etag:
        put_req.add_header("If-Match", etag)
        
    try:
        with urllib.request.urlopen(put_req, timeout=15) as resp:
            print(f"✅ [專案內部簡介同步成功] {project_id}")
            return True
    except Exception as e:
        print(f"⚠️ 專案內部簡介更新跳過或未變更: {e}")
        return False

def main():
    api_key = os.environ.get("LARCH_API_KEY", "").strip()
    if not api_key:
        print("LARCH_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)
        
    print(f"開始更新 {len(DESCRIPTIONS_UPDATE)} 部作品的簡介 (靜默 PATCH，不打擾)...")
    success_count = 0
    for pid, desc in DESCRIPTIONS_UPDATE.items():
        if update_listing_description(pid, desc, api_key):
            success_count += 1
            # Try to sync internal project description as well
            update_internal_project_description(pid, desc, api_key)
        time.sleep(2.0)
        
    print(f"\n全部簡介更新完成！成功 {success_count} / {len(DESCRIPTIONS_UPDATE)} 部。")

if __name__ == "__main__":
    main()
