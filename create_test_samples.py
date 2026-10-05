from pathlib import Path
import cv2

BASE_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = BASE_DIR / "samples"

source_path = SAMPLES_DIR / "test_backup.jpg"
output_path = SAMPLES_DIR / "low_resolution.jpg"

image = cv2.imread(str(source_path))

if image is None:
    print("源图片读取失败")
else:
    low_res_image = cv2.resize(image, (640, 480))
    cv2.imwrite(str(output_path), low_res_image)

    print("低分辨率测试图片生成成功")
    print("保存位置：", output_path)
    print("分辨率：640 x 480")

# 生成模糊测试图片
blurred_path = SAMPLES_DIR / "blurred.jpg"

source_image = cv2.imread(str(source_path))

if source_image is None:
    print("无法生成模糊图片：源图片读取失败")
else:
    blurred_image = cv2.GaussianBlur(
        source_image,
        (31, 31),
        0
    )

    cv2.imwrite(str(blurred_path), blurred_image)

    print("模糊测试图片生成成功")
    print("保存位置：", blurred_path)



# 生成过暗测试图片
dark_path = SAMPLES_DIR / "dark.jpg"

source_image = cv2.imread(str(source_path))

if source_image is not None:
    dark_image = cv2.convertScaleAbs(
        source_image,
        alpha=0.35,
        beta=0
    )

    cv2.imwrite(str(dark_path), dark_image)

    print("过暗测试图片生成成功")
    print("保存位置：", dark_path)


# 生成过亮测试图片
bright_path = SAMPLES_DIR / "bright.jpg"

if source_image is not None:
    bright_image = cv2.convertScaleAbs(
        source_image,
        alpha=1.4,
        beta=80
    )

    cv2.imwrite(str(bright_path), bright_image)

    print("过亮测试图片生成成功")
    print("保存位置：", bright_path)