import cv2
import os

# 获取当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(BASE_DIR, "video_samples")
SOURCE_VIDEO = os.path.join(VIDEO_DIR, "test_video.mp4")

def create_low_resolution_video():
    """读取原视频，缩小尺寸后另存为低分辨率视频"""
    cap = cv2.VideoCapture(SOURCE_VIDEO)
    if not cap.isOpened():
        print("❌ 无法打开原视频，请检查 test_video.mp4 是否存在")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    target_width, target_height = 640, 480

    # 设置视频编码器与输出对象（mp4v 是 MP4 的标准编码）
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_path = os.path.join(VIDEO_DIR, "low_resolution_video.mp4")
    out = cv2.VideoWriter(output_path, fourcc, fps, (target_width, target_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 读到视频末尾，退出循环
        # 把每一帧缩小成 640x480
        resized_frame = cv2.resize(frame, (target_width, target_height))
        out.write(resized_frame)

    cap.release()
    out.release()
    print(f"✅ 已生成低分辨率视频: {output_path}")

def create_broken_video():
    """生成一个包含垃圾数据的损坏视频文件"""
    broken_path = os.path.join(VIDEO_DIR, "broken_video.mp4")
    with open(broken_path, "wb") as f:
        # 写入一段毫无意义的文本数据，模拟文件损坏
        f.write(b"THIS IS NOT A REAL VIDEO FILE. GARBAGE DATA FOR TESTING DECODE FAILURE.")
    print(f"✅ 已生成损坏视频: {broken_path}")

def create_empty_video():
    """生成一个 0 字节的空视频文件"""
    empty_path = os.path.join(VIDEO_DIR, "empty_video.mp4")
    with open(empty_path, "wb") as f:
        pass  # 不写入任何内容，直接创建空文件
    print(f"✅ 已生成空视频: {empty_path}")

if __name__ == "__main__":
    create_low_resolution_video()
    create_broken_video()
    create_empty_video()  # 新增这行