import pytest

from image_inspector import (
    inspect_image,
    check_min_resolution,
    get_blur_score,
    check_blur,
    get_brightness_score,
    check_exposure
)

from utils import load_config


# =========================================================
# 读取统一配置
# =========================================================

CFG = load_config()


# =========================================================
# 1. 图片基础读取 / 解码测试
# =========================================================

@pytest.mark.parametrize(
    "filename, expected",
    [
        ("test_backup.jpg", "OK"),
        ("not_exist.jpg", "FILE_NOT_FOUND"),
        ("broken.jpg", "DECODE_FAILED"),
    ]
)
def test_inspect_image(filename, expected):
    actual = inspect_image(filename)

    assert actual == expected


# =========================================================
# 2. 正常图片分辨率测试
# =========================================================

@pytest.mark.parametrize(
    "min_width, min_height, expected",
    [
        (1920, 1080, "OK"),
        (4000, 3000, "OK"),
        (5000, 4000, "RESOLUTION_TOO_LOW"),
    ]
)
def test_min_resolution(
    min_width,
    min_height,
    expected
):
    actual = check_min_resolution(
        "test_backup.jpg",
        min_width,
        min_height
    )

    assert actual == expected


# =========================================================
# 3. 真实低分辨率异常图片
# =========================================================

def test_real_low_resolution_image():
    actual = check_min_resolution(
        "low_resolution.jpg",
        CFG["image"]["min_width"],
        CFG["image"]["min_height"]
    )

    assert actual == "RESOLUTION_TOO_LOW"


# =========================================================
# 4. 模糊后清晰度分数应下降
# =========================================================

def test_blurred_image_has_lower_score():
    normal_score = get_blur_score(
        "test_backup.jpg"
    )

    blurred_score = get_blur_score(
        "blurred.jpg"
    )

    assert normal_score is not None
    assert blurred_score is not None

    assert normal_score > blurred_score


# =========================================================
# 5. 模糊自动判定
# =========================================================

@pytest.mark.parametrize(
    "filename, expected",
    [
        ("test_backup.jpg", "OK"),
        ("blurred.jpg", "BLURRY"),
    ]
)
def test_blur_detection(
    filename,
    expected
):
    actual = check_blur(
        filename,
        threshold=CFG["image"]["blur_threshold"]
    )

    assert actual == expected


# =========================================================
# 6. 亮度关系测试
# =========================================================

def test_brightness_order():
    dark_score = get_brightness_score(
        "dark.jpg"
    )

    normal_score = get_brightness_score(
        "test_backup.jpg"
    )

    bright_score = get_brightness_score(
        "bright.jpg"
    )

    assert dark_score is not None
    assert normal_score is not None
    assert bright_score is not None

    assert (
        dark_score
        < normal_score
        < bright_score
    )


# =========================================================
# 7. 曝光状态自动判定
# =========================================================

@pytest.mark.parametrize(
    "filename, expected",
    [
        ("dark.jpg", "UNDEREXPOSED"),
        ("test_backup.jpg", "OK"),
        ("bright.jpg", "OVEREXPOSED"),
    ]
)
def test_exposure_detection(
    filename,
    expected
):
    actual = check_exposure(
        filename,
        dark_threshold=CFG["image"]["dark_threshold"],
        bright_threshold=CFG["image"]["bright_threshold"]
    )

    assert actual == expected