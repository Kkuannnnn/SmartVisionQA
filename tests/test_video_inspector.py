import os
import sys
import pytest

# 将项目根目录加入 sys.path，确保能导入 video_inspector 模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import video_inspector

from video_inspector import inspect_video, check_video_resolution, check_video_fps

def test_video_file_not_found():
    """测试不存在的视频文件"""
    result = inspect_video("not_exist_video.mp4")
    assert result["status"] == "FILE_NOT_FOUND"

def test_video_normal():
    """测试正常视频文件"""
    result = inspect_video("test_video.mp4")
    assert result["status"] == "OK"
    # 根据刚才的真实测量，断言各项指标都大于 0
    assert result["width"] > 0
    assert result["height"] > 0
    assert result["fps"] > 0
    assert result["frame_count"] > 0
    assert result["duration"] > 0


def test_video_resolution_too_low():
    """低分辨率视频在要求 1280x720 时应该失败"""
    assert check_video_resolution(
        "low_resolution_video.mp4",
        1280,
        720
    ) == "RESOLUTION_TOO_LOW"

def test_video_resolution_ok():
    """960x544 在要求 640x480 时应该通过"""
    assert check_video_resolution("test_video.mp4", 640, 480) == "OK"

def test_video_fps_too_low():
    """30fps 在要求 60fps 时应该失败"""
    assert check_video_fps("test_video.mp4", 60) == "FPS_TOO_LOW"

def test_video_fps_boundary_ok():
    """30fps 刚好等于 30fps 要求，应该通过"""
    assert check_video_fps("test_video.mp4", 30) == "OK"

def test_video_invalid_file():
    """不存在的视频，应返回 VIDEO_INVALID"""
    assert check_video_resolution("not_exist_video.mp4", 1280, 720) == "VIDEO_INVALID"
    assert check_video_fps("not_exist_video.mp4", 30) == "VIDEO_INVALID"


def test_video_broken_open_failed():
    """测试损坏视频：文件存在，但无法正常打开，预期返回 OPEN_FAILED"""
    # 这里请确认 video_inspector.py 中打开失败返回的状态是 "OPEN_FAILED"
    result = inspect_video("broken_video.mp4")
    assert result["status"] == "OPEN_FAILED"


def test_video_low_resolution_spec():
    """测试低分辨率视频规格检测：640x480 在要求 1280x720 时，预期返回 RESOLUTION_TOO_LOW"""
    result = check_video_resolution("low_resolution_video.mp4", 1280, 720)
    assert result == "RESOLUTION_TOO_LOW"

def test_video_empty_file():
    """测试空文件（0字节）：文件存在，无法打开，预期返回 OPEN_FAILED"""
    result = inspect_video("empty_video.mp4")
    assert result["status"] == "OPEN_FAILED"



@pytest.mark.parametrize(
    "mock_fps, expected",
    [
        (28.9, "FPS_TOO_LOW"),
        (29.0, "OK"),
        (29.1, "OK"),
        (30.0, "OK"),
    ]
)
def test_video_fps_boundary_with_mock(
    monkeypatch,
    mock_fps,
    expected
):
    # 模拟 inspect_video 返回指定 FPS
    def mock_inspect_video(filename):
        return {
            "status": "OK",
            "fps": mock_fps
        }

    monkeypatch.setattr(
        video_inspector,
        "inspect_video",
        mock_inspect_video
    )

    actual = check_video_fps(
        "fake_video.mp4",
        min_fps=30,
        tolerance=1.0
    )

    assert actual == expected



@pytest.mark.parametrize(
    "width, height, expected",
    [
        (1279, 720, "RESOLUTION_TOO_LOW"),
        (1280, 720, "OK"),
        (1281, 720, "OK"),
        (720, 1279, "RESOLUTION_TOO_LOW"),
        (720, 1280, "OK"),
        (720, 1281, "OK"),
    ]
)
def test_video_resolution_boundary_with_mock(
    monkeypatch,
    width,
    height,
    expected
):
    def mock_inspect_video(filename):
        return {
            "status": "OK",
            "width": width,
            "height": height
        }

    monkeypatch.setattr(
        video_inspector,
        "inspect_video",
        mock_inspect_video
    )

    actual = check_video_resolution(
        "fake_video.mp4",
        1280,
        720
    )

    assert actual == expected