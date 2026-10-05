
from pathlib import Path
import cv2

# 图片样本目录
SAMPLES_DIR = Path(__file__).resolve().parent / "samples"


# 图片检测函数
def inspect_image(filename):
    image_path = SAMPLES_DIR / filename

    # 文件不存在
    if not image_path.is_file():
        return "FILE_NOT_FOUND"

    # 文件存在，但无法解码
    image = cv2.imread(str(image_path))

    if image is None:
        return "DECODE_FAILED"

    # 正常图片
    height, width = image.shape[:2]
    print(f"    图片分辨率：{width} x {height}")

    return "OK"

# 获取图片分辨率
def get_image_resolution(filename):
    image_path = SAMPLES_DIR / filename

    if not image_path.is_file():
        return None

    image = cv2.imread(str(image_path))

    if image is None:
        return None

    height, width = image.shape[:2]

    return width, height


# 检查图片是否达到最低分辨率要求
def check_min_resolution(filename, min_width, min_height):
    resolution = get_image_resolution(filename)

    if resolution is None:
        return "IMAGE_INVALID"

    width, height = resolution

    if width >= min_width and height >= min_height:
        return "OK"

    return "RESOLUTION_TOO_LOW"

# 计算图片清晰度分数
def get_blur_score(filename):
    image_path = SAMPLES_DIR / filename

    if not image_path.is_file():
        return None

    image = cv2.imread(str(image_path))

    if image is None:
        return None

    # 转换为灰度图
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # 直方图均衡化：
    # 减弱整体亮度变化对边缘强度的影响
    normalized_gray = cv2.equalizeHist(gray)

    # Laplacian 方差作为清晰度原型指标
    score = cv2.Laplacian(
        normalized_gray,
        cv2.CV_64F
    ).var()

    return float(score)

# 判断图片是否模糊
def check_blur(filename, threshold):
    score = get_blur_score(filename)

    if score is None:
        return "IMAGE_INVALID"

    if score < threshold:
        return "BLURRY"

    return "OK"

# 获取图片平均亮度
def get_brightness_score(filename):
    image_path = SAMPLES_DIR / filename

    if not image_path.is_file():
        return None

    image = cv2.imread(str(image_path))

    if image is None:
        return None

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    mean_brightness = gray.mean()

    return float(mean_brightness)

# 判断图片曝光情况
def check_exposure(filename, dark_threshold, bright_threshold):
    brightness = get_brightness_score(filename)

    if brightness is None:
        return "IMAGE_INVALID"

    if brightness < dark_threshold:
        return "UNDEREXPOSED"

    if brightness > bright_threshold:
        return "OVEREXPOSED"

    return "OK"

# 原来的批量测试程序
def run_manual_tests():
    test_cases = [
        ("test_backup.jpg", "OK"),
        ("not_exist.jpg", "FILE_NOT_FOUND"),
        ("broken.jpg", "DECODE_FAILED")
    ]

    print("===== SmartVisionQA Automated Test =====")

    passed = 0

    for filename, expected in test_cases:
        print(f"\n正在测试：{filename}")

        actual = inspect_image(filename)

        print("预期结果：", expected)
        print("实际结果：", actual)

        if actual == expected:
            print("测试结果：PASS")
            passed += 1
        else:
            print("测试结果：FAIL")

    print("\n===== 测试报告 =====")
    print("总测试数：", len(test_cases))
    print("通过数量：", passed)
    print("失败数量：", len(test_cases) - passed)

    if passed != len(test_cases):
        raise SystemExit(1)


# 直接运行本文件时，才执行批量测试
if __name__ == "__main__":
    run_manual_tests()


