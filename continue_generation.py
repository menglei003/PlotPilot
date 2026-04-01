#!/usr/bin/env python3
"""Generate remaining chapters 16-100"""
import asyncio
import httpx
import json
from datetime import datetime

async def generate_batch(from_ch: int, to_ch: int):
    url = "http://localhost:8007/api/v1/novels/novel-1775066530753/hosted-write-stream"
    payload = {
        "from_chapter": from_ch,
        "to_chapter": to_ch,
        "auto_save": True,
        "auto_outline": True
    }

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting chapters {from_ch}-{to_ch}")

    async with httpx.AsyncClient(timeout=600.0) as client:
        async with client.stream("POST", url, json=payload) as response:
            if response.status_code != 200:
                print(f"ERROR: Status {response.status_code}")
                return False

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    try:
                        event = json.loads(line[6:])
                        event_type = event.get("type")

                        if event_type == "chapter_start":
                            ch = event.get("chapter")
                            print(f"  Chapter {ch} starting...")

                        elif event_type == "saved":
                            if event.get("ok"):
                                ch = event.get("chapter")
                                print(f"  Chapter {ch} saved!")

                        elif event_type == "error":
                            print(f"  ERROR: {event.get('message')}")
                            return False

                    except json.JSONDecodeError:
                        pass

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Batch {from_ch}-{to_ch} complete!")
    return True

async def main():
    print("="*60)
    print("Continuing Chapter Generation: 16-100")
    print("="*60)

    # Generate in batches of 10
    for start in range(16, 101, 10):
        end = min(start + 9, 100)
        success = await generate_batch(start, end)
        if not success:
            print(f"\nStopped at batch {start}-{end}")
            break
        await asyncio.sleep(1)

    print("\n" + "="*60)
    print("Generation Complete!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
