#!/usr/bin/env python3
"""
Pre-generates studio-grade native Japanese Neural MP3 audio files using
Microsoft Azure Neural Voices (ja-JP-NanamiNeural & ja-JP-KeitaNeural) via edge-tts.
100% Free, zero API key required. Output goes into www/audio/<fnv1a_hash>.mp3.
"""
import asyncio, json, os, re, sys

VOICE_FEMALE = "ja-JP-NanamiNeural"
VOICE_MALE = "ja-JP-KeitaNeural"

def fnv1a_hex(text: str) -> str:
    h = 2166136261
    for ch in text:
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return f"{h:08x}"

def collect_phrases(html_path: str):
    html = open(html_path, encoding="utf-8").read()
    m_sc = re.search(r"const SCENARIOS = (\{.*?\});\n      const EXTRA_CORE_VOCAB", html, re.S)
    m_ex = re.search(r"const EXTRA_CORE_VOCAB = (\[.*?\]);", html, re.S)
    if not m_sc or not m_ex:
        print("ERROR: Could not locate SCENARIOS/EXTRA_CORE_VOCAB in index.html")
        sys.exit(1)

    scenarios = json.loads(m_sc.group(1))
    extra = json.loads(m_ex.group(1))

    # Map hash -> (text, voice)
    items = {}
    def add(txt, voice=VOICE_FEMALE):
        t = str(txt or "").strip()
        if not t:
            return
        k = fnv1a_hex(t)
        if k not in items:
            items[k] = (t, voice)

    # Test sentence
    add("こんにちは！今日も楽しく日本語を練習しましょう。", VOICE_FEMALE)

    for v in extra:
        add(v.get("word"), VOICE_FEMALE)
        add(v.get("exPlain"), VOICE_FEMALE)

    for sc in scenarios.values():
        for v in sc.get("vocab", []):
            add(v.get("word"), VOICE_FEMALE)
            add(v.get("exPlain"), VOICE_FEMALE)
        for g in sc.get("grammar", []):
            add("".join(g.get("answer", [])), VOICE_FEMALE)
            add(g.get("polite"), VOICE_FEMALE)
            add(g.get("casual"), VOICE_FEMALE)
        for d in sc.get("dialogue", []):
            v_pick = VOICE_MALE if d.get("speaker") == "나" else VOICE_FEMALE
            add(d.get("plain"), v_pick)
        rp = sc.get("roleplay", {})
        for key in ("openingPolite", "openingCasual", "fallbackPolite", "fallbackCasual"):
            if key in rp:
                add(rp[key].get("jp"), VOICE_FEMALE)
        for q in rp.get("quickRepliesPolite", []) + rp.get("quickRepliesCasual", []):
            add(q, VOICE_FEMALE)
        for r in rp.get("rescues", []):
            add(r.get("polite"), VOICE_FEMALE)
            add(r.get("casual"), VOICE_FEMALE)
        for rule in rp.get("replyRules", []):
            if "polite" in rule:
                add(rule["polite"].get("jp"), VOICE_FEMALE)
            if "casual" in rule:
                add(rule["casual"].get("jp"), VOICE_FEMALE)
    return items

async def synthesize_all():
    import edge_tts
    html_path = os.path.join("www", "index.html")
    out_dir = os.path.join("www", "audio")
    os.makedirs(out_dir, exist_ok=True)
    items = collect_phrases(html_path)
    print(f"Total unique Japanese phrases to synthesize (Azure Neural): {len(items)}")

    sem = asyncio.Semaphore(12)
    ok_count = 0
    fail_count = 0

    async def worker(h, text, voice):
        nonlocal ok_count, fail_count
        out_file = os.path.join(out_dir, f"{h}.mp3")
        if os.path.exists(out_file) and os.path.getsize(out_file) > 500:
            ok_count += 1
            return
        async with sem:
            for attempt in range(3):
                try:
                    comm = edge_tts.Communicate(text, voice)
                    await comm.save(out_file)
                    if os.path.exists(out_file) and os.path.getsize(out_file) > 200:
                        ok_count += 1
                        return
                except Exception:
                    await asyncio.sleep(0.5 * (attempt + 1))
            fail_count += 1

    await asyncio.gather(*(worker(h, t, v) for h, (t, v) in items.items()))
    print(f"Azure Neural Japanese Audio Generation Done: {ok_count} OK, {fail_count} failed.")

if __name__ == "__main__":
    asyncio.run(synthesize_all())
