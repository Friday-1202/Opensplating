from pathlib import Path
from rosbags.highlevel import AnyReader

bagpath = Path(r"D:\AAE5303project\AMtown02 (1).bag")
outdir = Path(r"D:\AAE5303project\AMtown02_extracted\images")
outdir.mkdir(parents=True, exist_ok=True)

target_topic = "/left_camera/image/compressed"

count = 0

with AnyReader([bagpath]) as reader:
    connections = [c for c in reader.connections if c.topic == target_topic]

    if not connections:
        print(f"Topic not found: {target_topic}")
        raise SystemExit(1)

    for connection, timestamp, rawdata in reader.messages(connections=connections):
        msg = reader.deserialize(rawdata, connection.msgtype)

        # 用 bag 的时间戳命名，避免重名
        filename = outdir / f"{timestamp}.jpg"

        # CompressedImage 的 data 本身就是 jpg/jpeg 字节流
        with open(filename, "wb") as f:
            f.write(msg.data)

        count += 1
        if count % 100 == 0:
            print(f"exported {count} images")

print(f"Done. Exported {count} images to: {outdir}")