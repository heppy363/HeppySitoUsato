from pathlib import Path
import time


Path("/tmp/worker-ready").write_text("ready", encoding="utf-8")

while True:
    time.sleep(60)
