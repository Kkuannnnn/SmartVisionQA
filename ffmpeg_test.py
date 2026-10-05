import subprocess
import json
import os


# ffprobe 路径
ffprobe_path = r"D:\ffmpeg\bin\ffprobe.exe"


def get_video_metadata(filepath, timeout=10):
    """
    使用 ffprobe 获取视频元数据。

    返回：
    - 成功：ffprobe 解析后的 JSON 字典
    - 失败：{"error": "..."}
    """

    # 1. 检查 ffprobe 是否存在
    if not os.path.exists(ffprobe_path):
        return {
            "error": f"找不到 ffprobe.exe，请检查路径: {ffprobe_path}"
        }

    cmd = [
        ffprobe_path,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        filepath
    ]

    try:
        # 2. 执行 ffprobe
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout
        )

        # 3. ffprobe 执行失败
        if result.returncode != 0:
            return {
                "error": "FFPROBE_FAILED",
                "returncode": result.returncode,
                "stderr": result.stderr
            }

        # 4. JSON 解析
        try:
            metadata = json.loads(result.stdout)

        except json.JSONDecodeError:
            return {
                "error": "INVALID_JSON"
            }

        # 5. 检查是否包含视频流
        video_stream = next(
            (
                stream
                for stream in metadata.get("streams", [])
                if stream.get("codec_type") == "video"
            ),
            None
        )

        if video_stream is None:
            return {
                "error": "NO_VIDEO_STREAM"
            }

        return metadata

    except subprocess.TimeoutExpired:
        return {
            "error": "FFPROBE_TIMEOUT"
        }

    except Exception as e:
        return {
            "error": str(e)
        }


if __name__ == "__main__":
    video_path = r"video_samples\test_video.mp4"

    meta = get_video_metadata(video_path)

    if "error" in meta:
        print("失败:", meta["error"])

    else:
        video_stream = next(
            (
                stream
                for stream in meta.get("streams", [])
                if stream.get("codec_type") == "video"
            ),
            None
        )

        print("成功获取视频元数据！")

        print(
            "编码格式 (codec):",
            video_stream.get("codec_name")
        )

        print(
            "分辨率:",
            video_stream.get("width"),
            "x",
            video_stream.get("height")
        )

        print(
            "码率 (bitrate):",
            meta.get("format", {}).get("bit_rate"),
            "bps"
        )

        print(
            "时长 (duration):",
            meta.get("format", {}).get("duration"),
            "秒"
        )