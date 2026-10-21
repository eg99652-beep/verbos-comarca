import asyncio, re, sys, subprocess, json, pathlib
import edge_tts

html = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2])
block = re.search(r"const VERBS = `(.*?)`", html, re.S).group(1)
SPOKEN = {"1|read": "red", "2|read": "red", "0|tear": "tare"}
texts = set()
for line in block.strip().split("\n"):
    forms = line.split("|")[:3]
    for i, f in enumerate(forms):
        texts.add(", ".join(SPOKEN.get(f"{i}|{w}", w) for w in f.split("/")))
slug = lambda t: re.sub(r"[^a-z]+", "-", t.lower()).strip("-")
VOICES = {"us-f": "en-US-AvaNeural", "us-m": "en-US-AndrewNeural", "gb-f": "en-GB-SoniaNeural", "gb-m": "en-GB-RyanNeural"}
sem = asyncio.Semaphore(8)

async def one(key, voice, text):
    d = out / key; d.mkdir(parents=True, exist_ok=True)
    dst = d / f"{slug(text)}.mp3"
    if dst.exists(): return
    raw = d / f"{slug(text)}.raw.mp3"
    async with sem:
        for attempt in range(4):
            try:
                await edge_tts.Communicate(text + ".", voice).save(str(raw)); break
            except Exception as e:
                await asyncio.sleep(2 * (attempt + 1))
        else:
            print("FAIL", key, text); return
    proc = await asyncio.create_subprocess_exec("ffmpeg", "-loglevel", "error", "-y", "-i", str(raw),
        "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.05",
        "-ac", "1", "-b:a", "40k", str(dst))
    await proc.wait(); raw.unlink()

async def main():
    await asyncio.gather(*(one(k, v, t) for k, v in VOICES.items() for t in sorted(texts)))
    print(len(texts), "textos x", len(VOICES), "voces")
asyncio.run(main())
