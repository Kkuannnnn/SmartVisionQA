from pathlib import Path
import cv2


VIDEO_DIR = Path(__file__).resolve().parent / "video_samples"


def inspect_video(filename):
    video_path = VIDEO_DIR / filename

    # 1. 检查视频文件是否存在
    if not video_path.is_file():
        return {
            "status": "FILE_NOT_FOUND"
        }

    # 2. 尝试打开视频
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        return {
            "status": "OPEN_FAILED"
        }

    # 3. 获取视频基本信息
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 防止 fps 为 0 时除零
    if fps > 0:
        duration = frame_count / fps
    else:
        duration = 0

    cap.release()

    return {
        "status": "OK",
        "width": width,
        "height": height,
        "fps": fps,
        "frame_count": frame_count,
        "duration": duration
    }


def check_video_resolution(filename, min_width, min_height):
    result = inspect_video(filename)

    if result["status"] != "OK":
        return "VIDEO_INVALID"

    width = result["width"]
    height = result["height"]

    # 使用长边 / 短边判断，兼容横屏和竖屏视频
    actual_long = max(width, height)
    actual_short = min(width, height)

    required_long = max(min_width, min_height)
    required_short = min(min_width, min_height)

    if (
        actual_long >= required_long
        and actual_short >= required_short
    ):
        return "OK"

    return "RESOLUTION_TOO_LOW"


def check_video_fps(filename, min_fps, tolerance=1.0):
    result = inspect_video(filename)

    if result["status"] != "OK":
        return "VIDEO_INVALID"

    fps = result["fps"]

    if fps is None or fps <= 0:
        return "FPS_INVALID"

    # 允许一定容差，例如要求 30 FPS 时，29 FPS 也可接受
    if fps >= min_fps - tolerance:
        return "OK"

    return "FPS_TOO_LOW"


if __name__ == "__main__":
    result = inspect_video("test_video.mp4")

    print("===== SmartVisionQA Video Inspector =====")
    print("状态：", result["status"])

    if result["status"] == "OK":
        print("分辨率：", result["width"], "x", result["height"])
        print("FPS：", round(result["fps"], 2))
        print("总帧数：", result["frame_count"])
        print("时长：", round(result["duration"], 2), "秒")

    print("\n===== 规格检测 =====")
    # 我们的视频是 960x544，要求 1280x720 肯定会失败（验证低规格检测）
    print("分辨率检测 (要求 1280x720):", check_video_resolution("test_video.mp4", 1280, 720))
    # 我们的视频是 30fps，要求 30fps 刚好通过（验证边界值）
    print("帧率检测 (要求 30 FPS):", check_video_fps("test_video.mp4", 30))