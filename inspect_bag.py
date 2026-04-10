from pathlib import Path
from rosbags.highlevel import AnyReader

bagpath = Path(r"D:\AAE5303project\AMtown02 (1).bag")

with AnyReader([bagpath]) as reader:
    print("Topics in bag:\n")
    for c in reader.connections:
        print(f"topic={c.topic} | msgtype={c.msgtype}")