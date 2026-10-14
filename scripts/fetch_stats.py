#!/usr/bin/env python3
"""
Larch Works Stats & Daily Visitor
---------------------------------
1. Pings/browses public Larch work URLs & market games links.
2. Calls Larch REST API & Marketplace API to fetch live stats and ranking.
3. Updates data/works.json and data/history.json for GitHub Pages dashboard.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

# Constants
API_BASE = "https://larch.ink"
PUBLISHED_ENDPOINT = f"{API_BASE}/api/agent/published"
MARKETPLACE_ENDPOINT = f"{API_BASE}/api/marketplace"
CST = timezone(timedelta(hours=8))  # Asia/Taipei (UTC+8)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 (LarchShowcaseBot/1.0)"

def get_api_key():
    key = os.environ.get("LARCH_API_KEY", "").strip()
    if not key:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        if os.path.isfile(env_file):
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("LARCH_API_KEY="):
                        key = line.strip().split("=", 1)[1].strip("'\"")
                        break
    if not key:
        print("Error: LARCH_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return key

def fetch_published_data(api_key):
    print(f"Fetching published works from {PUBLISHED_ENDPOINT}...")
    req = urllib.request.Request(PUBLISHED_ENDPOINT)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept", "application/json")
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed = int((time.time() - start_time) * 1000)
            print(f"Successfully fetched {len(data.get('works', []))} author works in {elapsed}ms.")
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Failed to fetch published works: {e}", file=sys.stderr)
        sys.exit(1)

def fetch_marketplace_data():
    """Fetch public marketplace games list for global ranking and market URLs."""
    print(f"Fetching marketplace games list from {MARKETPLACE_ENDPOINT}...")
    req = urllib.request.Request(MARKETPLACE_ENDPOINT)
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept", "application/json")
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed = int((time.time() - start_time) * 1000)
            games = data.get("games", [])
            print(f"Successfully fetched {len(games)} marketplace games in {elapsed}ms.")
            return games
    except Exception as e:
        print(f"Warning: Could not fetch marketplace games: {e}", file=sys.stderr)
        return []

def ping_url(url, timeout=15):
    """Simulate browser visiting a URL and record status and response time."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = int((time.time() - start_time) * 1000)
            return {
                "url": url,
                "status": resp.status,
                "latency_ms": elapsed,
                "success": True,
                "error": None
            }
    except urllib.error.HTTPError as e:
        elapsed = int((time.time() - start_time) * 1000)
        return {
            "url": url,
            "status": e.code,
            "latency_ms": elapsed,
            "success": e.code == 200,
            "error": f"HTTP {e.code}"
        }
    except Exception as e:
        elapsed = int((time.time() - start_time) * 1000)
        return {
            "url": url,
            "status": 0,
            "latency_ms": elapsed,
            "success": False,
            "error": str(e)
        }

def visit_works(works):
    """Browse each work's public play URL and market game page."""
    print("Simulating daily visit to works & market pages...")
    results = []
    for w in works:
        title = w.get("title", "未命名作品")
        play_url = w.get("playUrl")
        market_url = w.get("marketUrl")
        
        # Ping play URL
        if play_url:
            res_play = ping_url(play_url)
            res_play["title"] = title
            res_play["type"] = "play"
            results.append(res_play)
            print(f"  [Play]   {title} -> {res_play['status']} ({res_play['latency_ms']}ms)")
            time.sleep(0.2)
            
        # Ping market game page
        if market_url:
            res_market = ping_url(market_url)
            res_market["title"] = title
            res_market["type"] = "market"
            results.append(res_market)
            print(f"  [Market] {title} -> {res_market['status']} ({res_market['latency_ms']}ms)")
            time.sleep(0.2)
            
    return results

def compute_summary(works, market_games):
    tot_views = sum(w.get("views", 0) for w in works)
    tot_plays = sum(w.get("plays", 0) for w in works)
    tot_likes = sum(w.get("likes", 0) for w in works)
    tot_comments = sum(w.get("comments", 0) for w in works)
    tot_unanswered = sum(w.get("unanswered", 0) for w in works)
    tot_danmaku = sum(w.get("danmaku", 0) for w in works)
    
    total_chapters = 0
    total_nodes = 0
    for w in works:
        chaps = w.get("chapters", [])
        total_chapters += len(chaps)
        total_nodes += sum(c.get("nodeCount", 0) for c in chaps)
        
    # Market rankings analysis
    top_10_count = sum(1 for w in works if w.get("marketRank", 999) <= 10)
    top_20_count = sum(1 for w in works if w.get("marketRank", 999) <= 20)
    
    return {
        "total_works": len(works),
        "total_views": tot_views,
        "total_plays": tot_plays,
        "total_likes": tot_likes,
        "total_comments": tot_comments,
        "total_unanswered": tot_unanswered,
        "total_danmaku": tot_danmaku,
        "total_chapters": total_chapters,
        "total_nodes": total_nodes,
        "market_total_games": len(market_games),
        "market_top_10_count": top_10_count,
        "market_top_20_count": top_20_count,
        "market_share_percent": round((len(works) / len(market_games) * 100), 1) if market_games else 0
    }

def update_history(summary, works, history_path, today_str):
    history = []
    if os.path.isfile(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception as e:
            print(f"Warning: could not read history file: {e}")
            history = []
            
    delta = {
        "views": 0,
        "plays": 0,
        "likes": 0,
        "comments": 0
    }
    
    prev_entry = None
    existing_today_index = None
    
    for idx, entry in enumerate(history):
        if entry.get("date") == today_str:
            existing_today_index = idx
        else:
            prev_entry = entry
            
    if prev_entry:
        delta["views"] = summary["total_views"] - prev_entry.get("total_views", summary["total_views"])
        delta["plays"] = summary["total_plays"] - prev_entry.get("total_plays", summary["total_plays"])
        delta["likes"] = summary["total_likes"] - prev_entry.get("total_likes", summary["total_likes"])
        delta["comments"] = summary["total_comments"] - prev_entry.get("total_comments", summary["total_comments"])
        
    works_snapshot = {}
    for w in works:
        wid = w.get("id")
        works_snapshot[wid] = {
            "views": w.get("views", 0),
            "plays": w.get("plays", 0),
            "likes": w.get("likes", 0),
            "comments": w.get("comments", 0),
            "marketRank": w.get("marketRank")
        }
        
    today_snapshot = {
        "date": today_str,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_views": summary["total_views"],
        "total_plays": summary["total_plays"],
        "total_likes": summary["total_likes"],
        "total_comments": summary["total_comments"],
        "total_works": summary["total_works"],
        "works": works_snapshot
    }
    
    if existing_today_index is not None:
        history[existing_today_index] = today_snapshot
    else:
        history.append(today_snapshot)
        
    if len(history) > 90:
        history = history[-90:]
        
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
        
    return delta

def write_step_summary(summary, delta, works, ping_results):
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_file:
        return
        
    lines = []
    lines.append("# 🎮 Larch 作品數據與市集巡檢回報")
    lines.append("")
    lines.append(f"**更新時間 (CST)**: `{datetime.now(CST).strftime('%Y-%m-%d %H:%M:%S')}`")
    lines.append("")
    lines.append(f"> 🏆 **Larch 市集表現**：全站共 {summary.get('market_total_games', 91)} 款遊戲，林亞澤共有 **{summary['total_works']} 款**（佔全站 {summary.get('market_share_percent', 20)}%），**全站 Top 10 獨佔 {summary.get('market_top_10_count', 5)} 席**！")
    lines.append("")
    lines.append("### 📊 總計數據看板")
    lines.append("")
    lines.append("| 指標 | 當前總數 | 今日變化 |")
    lines.append("|---|---|---|")
    lines.append(f"| 👁️ 總瀏覽數 | **{summary['total_views']:,}** | `+{delta['views']:,}` |")
    lines.append(f"| 🎮 總遊玩數 | **{summary['total_plays']:,}** | `+{delta['plays']:,}` |")
    lines.append(f"| ❤️ 累計愛心 | **{summary['total_likes']:,}** | `+{delta['likes']:,}` |")
    lines.append(f"| 💬 總留言數 | **{summary['total_comments']:,}** | `+{delta['comments']:,}` |")
    lines.append(f"| ⏳ 未回覆留言 | **{summary['total_unanswered']}** | - |")
    lines.append(f"| 📚 上架作品數 | **{summary['total_works']}** 部 | - |")
    lines.append("")
    lines.append("### 🏆 市集排行與作品清單")
    lines.append("")
    lines.append("| 市集排名 | 封面 | 作品名稱 | 瀏覽 | 遊玩 | 愛心 | 留言 | 巡檢狀態 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    
    sorted_works = sorted(works, key=lambda x: x.get("views", 0), reverse=True)
    ping_map = {p["url"]: p for p in ping_results}
    
    for w in sorted_works:
        title = w.get("title", "")
        play_url = w.get("playUrl", "")
        cover = w.get("coverUrl", "")
        img_tag = f'<img src="{cover}" width="50" style="border-radius:4px;" />' if cover else ""
        rank_str = f"🏅 #{w.get('marketRank')}" if w.get("marketRank") else "-"
        views = f"{w.get('views', 0):,}"
        plays = f"{w.get('plays', 0):,}"
        likes = f"{w.get('likes', 0)}"
        comments = f"{w.get('comments', 0)}"
        if w.get("unanswered", 0) > 0:
            comments += f" (⚠️ {w.get('unanswered')})"
            
        ping_info = ping_map.get(play_url, {})
        status_badge = "✅ 200" if ping_info.get("status") == 200 else f"⚠️ {ping_info.get('status', 'ERR')}"
        
        lines.append(f"| **{rank_str}** | {img_tag} | [{title}]({play_url}) | {views} | {plays} | {likes} | {comments} | {status_badge} ({ping_info.get('latency_ms', 0)}ms) |")
        
    lines.append("")
    try:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as e:
        print(f"Could not write to GITHUB_STEP_SUMMARY: {e}")

def main():
    api_key = get_api_key()
    
    # 1. Fetch authenticated author works
    data = fetch_published_data(api_key)
    works = data.get("works", [])
    
    # 2. Fetch public marketplace games list
    market_games = fetch_marketplace_data()
    
    # Calculate marketplace rank by views
    sorted_market = sorted(market_games, key=lambda x: x.get("views", 0), reverse=True)
    market_rank_map = {}
    market_game_map = {}
    for rank_idx, g in enumerate(sorted_market, 1):
        gid = g.get("id")
        market_rank_map[gid] = rank_idx
        market_game_map[gid] = g
    
    # 3. Enrich work objects with URLs and Market ranking
    for w in works:
        wid = w.get("id")
        author = w.get("authorHandle", "yaze")
        slug = w.get("customSlug") or wid
        w["playUrl"] = f"https://larch.ink/play/market/{author}/{slug}"
        w["workUrl"] = f"https://larch.ink/work/{slug}"
        w["authorUrl"] = f"https://larch.ink/@{author}/{slug}"
        # Direct game page inside https://larch.ink/market?section=games
        w["marketUrl"] = f"https://larch.ink/market?section=games&game={wid}"
        
        # Attach marketplace info
        mg = market_game_map.get(wid)
        if mg:
            w["marketRank"] = market_rank_map.get(wid)
            w["authorAvatar"] = mg.get("authorAvatar")
            w["format"] = mg.get("format")
            w["marketNodeCount"] = mg.get("nodeCount")
        else:
            w["marketRank"] = market_rank_map.get(wid)
    
    # 4. Daily ping / browse public works and market pages
    ping_results = visit_works(works)
    
    # 5. Compute summary
    summary = compute_summary(works, market_games)
    
    # 6. Time info
    now_utc = datetime.now(timezone.utc)
    now_cst = now_utc.astimezone(CST)
    today_str = now_cst.strftime("%Y-%m-%d")
    
    # 7. History tracking
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    history_path = os.path.join(data_dir, "history.json")
    delta = update_history(summary, works, history_path, today_str)
    
    # 8. Output data/works.json
    output_data = {
        "updated_at": now_utc.isoformat(),
        "updated_at_cst": now_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "author": "yaze",
        "market_section_url": "https://larch.ink/market?section=games",
        "summary": summary,
        "delta": delta,
        "works": works,
        "ping_results": ping_results
    }
    
    works_path = os.path.join(data_dir, "works.json")
    with open(works_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"Saved latest data with marketplace info to {works_path}")
    
    # 9. GitHub Step Summary
    write_step_summary(summary, delta, works, ping_results)
    
    print("\n--- Summary ---")
    print(f"Total Works: {summary['total_works']} / {summary.get('market_total_games', 91)} on Larch Market")
    print(f"Top 10 Games on Market: {summary.get('market_top_10_count', 0)} works")
    print(f"Total Views: {summary['total_views']} (+{delta['views']} today)")
    print(f"Total Plays: {summary['total_plays']} (+{delta['plays']} today)")
    print(f"Total Likes: {summary['total_likes']} (+{delta['likes']} today)")
    print(f"Total Comments: {summary['total_comments']} (+{delta['comments']} today)")
    print("Done!")

if __name__ == "__main__":
    main()
