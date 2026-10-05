import subprocess

import ffmpeg_test


def test_ffprobe_failed(monkeypatch):
    """
    模拟 ffprobe 执行失败：
    returncode != 0
    """

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=["ffprobe"],
            returncode=1,
            stdout="",
            stderr="mock ffprobe error"
        )

    monkeypatch.setattr(
        ffmpeg_test.os.path,
        "exists",
        lambda path: True
    )

    monkeypatch.setattr(
        ffmpeg_test.subprocess,
        "run",
        mock_run
    )

    result = ffmpeg_test.get_video_metadata(
        "fake_video.mp4"
    )

    assert result["error"] == "FFPROBE_FAILED"
    assert result["returncode"] == 1


def test_ffprobe_timeout(monkeypatch):
    """
    模拟 ffprobe 执行超时
    """

    def mock_run(*args, **kwargs):
        raise subprocess.TimeoutExpired(
            cmd="ffprobe",
            timeout=10
        )

    monkeypatch.setattr(
        ffmpeg_test.os.path,
        "exists",
        lambda path: True
    )

    monkeypatch.setattr(
        ffmpeg_test.subprocess,
        "run",
        mock_run
    )

    result = ffmpeg_test.get_video_metadata(
        "fake_video.mp4"
    )

    assert result["error"] == "FFPROBE_TIMEOUT"


def test_ffprobe_invalid_json(monkeypatch):
    """
    模拟 ffprobe 成功执行，
    但返回内容不是合法 JSON
    """

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=["ffprobe"],
            returncode=0,
            stdout="this is not json",
            stderr=""
        )

    monkeypatch.setattr(
        ffmpeg_test.os.path,
        "exists",
        lambda path: True
    )

    monkeypatch.setattr(
        ffmpeg_test.subprocess,
        "run",
        mock_run
    )

    result = ffmpeg_test.get_video_metadata(
        "fake_video.mp4"
    )

    assert result["error"] == "INVALID_JSON"


def test_ffprobe_no_video_stream(monkeypatch):
    """
    模拟 ffprobe 返回合法 JSON，
    但其中没有 video stream
    """

    fake_json = """
    {
        "streams": [
            {
                "codec_type": "audio",
                "codec_name": "aac"
            }
        ],
        "format": {
            "duration": "3.0"
        }
    }
    """

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=["ffprobe"],
            returncode=0,
            stdout=fake_json,
            stderr=""
        )

    monkeypatch.setattr(
        ffmpeg_test.os.path,
        "exists",
        lambda path: True
    )

    monkeypatch.setattr(
        ffmpeg_test.subprocess,
        "run",
        mock_run
    )

    result = ffmpeg_test.get_video_metadata(
        "fake_video.mp4"
    )

    assert result["error"] == "NO_VIDEO_STREAM"


def test_ffprobe_normal(monkeypatch):
    """
    模拟 ffprobe 正常返回视频元数据
    """

    fake_json = """
    {
        "streams": [
            {
                "codec_type": "video",
                "codec_name": "hevc",
                "width": 720,
                "height": 1280
            }
        ],
        "format": {
            "bit_rate": "1041827",
            "duration": "3.181111"
        }
    }
    """

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=["ffprobe"],
            returncode=0,
            stdout=fake_json,
            stderr=""
        )

    monkeypatch.setattr(
        ffmpeg_test.os.path,
        "exists",
        lambda path: True
    )

    monkeypatch.setattr(
        ffmpeg_test.subprocess,
        "run",
        mock_run
    )

    result = ffmpeg_test.get_video_metadata(
        "fake_video.mp4"
    )

    assert "error" not in result

    video_stream = next(
        stream
        for stream in result["streams"]
        if stream["codec_type"] == "video"
    )

    assert video_stream["codec_name"] == "hevc"
    assert video_stream["width"] == 720
    assert video_stream["height"] == 1280

    assert result["format"]["bit_rate"] == "1041827"
    assert result["format"]["duration"] == "3.181111"