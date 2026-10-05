from pathlib import Path

import pandas as pd

import image_inspector
import video_inspector
from utils import load_config, setup_logger, BASE_DIR


# =========================================================
# 基础路径
# =========================================================

PROJECT_DIR = Path(BASE_DIR)

IMAGE_DIR = PROJECT_DIR / "samples"
VIDEO_DIR = PROJECT_DIR / "video_samples"
REPORT_DIR = PROJECT_DIR / "reports"


# =========================================================
# 图片检测
# =========================================================

def evaluate_image(filename, cfg, logger):
    """
    对单张图片执行完整检测。
    返回统一格式的结果字典。
    """

    logger.info(f"正在检测图片: {filename}")

    try:
        # 1. 基础文件 / 解码检查
        io_status = image_inspector.inspect_image(filename)

        # 默认值
        resolution_status = "NOT_RUN"
        blur_status = "NOT_RUN"
        exposure_status = "NOT_RUN"

        width = None
        height = None

        blur_score = None
        brightness_score = None

        failure_reasons = []

        # 2. 只有图片正常解码后，才继续执行后续检查
        if io_status == "OK":

            # 获取实际分辨率
            resolution = image_inspector.get_image_resolution(filename)

            if resolution is not None:
                width, height = resolution

            # 分辨率检测
            resolution_status = image_inspector.check_min_resolution(
                filename,
                cfg["image"]["min_width"],
                cfg["image"]["min_height"]
            )

            # 清晰度分数
            blur_score = image_inspector.get_blur_score(filename)

            # 模糊检测
            blur_status = image_inspector.check_blur(
                filename,
                cfg["image"]["blur_threshold"]
            )

            # 平均亮度
            brightness_score = image_inspector.get_brightness_score(filename)

            # 曝光检测
            exposure_status = image_inspector.check_exposure(
                filename,
                cfg["image"]["dark_threshold"],
                cfg["image"]["bright_threshold"]
            )

            # 汇总失败原因
            if resolution_status != "OK":
                failure_reasons.append(resolution_status)

            if blur_status != "OK":
                failure_reasons.append(blur_status)

            if exposure_status != "OK":
                failure_reasons.append(exposure_status)

            # 最终判定
            if failure_reasons:
                verdict = "FAIL"
            else:
                verdict = "PASS"

        else:
            # 文件不存在 / 无法解码
            verdict = "FAIL"
            failure_reasons.append(io_status)

        return {
            "filename": filename,
            "file_type": "image",

            "io_status": io_status,

            "width": width,
            "height": height,

            "fps": None,
            "frame_count": None,
            "duration": None,

            "blur_score": (
                round(blur_score, 2)
                if blur_score is not None
                else None
            ),

            "brightness_score": (
                round(brightness_score, 2)
                if brightness_score is not None
                else None
            ),

            "resolution_status": resolution_status,
            "blur_status": blur_status,
            "exposure_status": exposure_status,

            "fps_status": "N/A",

            "verdict": verdict,

            "failure_reason": (
                "; ".join(failure_reasons)
                if failure_reasons
                else ""
            )
        }

    except Exception as exc:
        logger.exception(
            f"图片检测发生异常: {filename}"
        )

        return {
            "filename": filename,
            "file_type": "image",

            "io_status": "ERROR",

            "width": None,
            "height": None,

            "fps": None,
            "frame_count": None,
            "duration": None,

            "blur_score": None,
            "brightness_score": None,

            "resolution_status": "NOT_RUN",
            "blur_status": "NOT_RUN",
            "exposure_status": "NOT_RUN",

            "fps_status": "N/A",

            "verdict": "ERROR",

            "failure_reason": (
                f"{type(exc).__name__}: {exc}"
            )
        }


# =========================================================
# 视频检测
# =========================================================

def evaluate_video(filename, cfg, logger):
    """
    对单个视频执行完整检测。
    返回统一格式的结果字典。
    """

    logger.info(f"正在检测视频: {filename}")

    try:
        # 1. 基础视频检查
        inspect_result = video_inspector.inspect_video(filename)

        io_status = inspect_result.get(
            "status",
            "UNKNOWN"
        )

        # 默认值
        resolution_status = "NOT_RUN"
        fps_status = "NOT_RUN"

        width = None
        height = None

        fps = None
        frame_count = None
        duration = None

        failure_reasons = []

        # 2. 视频正常打开后继续检查
        if io_status == "OK":

            width = inspect_result.get("width")
            height = inspect_result.get("height")
            fps = inspect_result.get("fps")
            frame_count = inspect_result.get("frame_count")
            duration = inspect_result.get("duration")

            # 分辨率检测
            resolution_status = (
                video_inspector.check_video_resolution(
                    filename,
                    cfg["video"]["min_width"],
                    cfg["video"]["min_height"]
                )
            )

            # FPS 检测
            fps_status = (
                video_inspector.check_video_fps(
                    filename,
                    cfg["video"]["min_fps"]
                )
            )

            if resolution_status != "OK":
                failure_reasons.append(
                    resolution_status
                )

            if fps_status != "OK":
                failure_reasons.append(
                    fps_status
                )

            # 最终判定
            if failure_reasons:
                verdict = "FAIL"
            else:
                verdict = "PASS"

        else:
            # OPEN_FAILED / FILE_NOT_FOUND 等
            verdict = "FAIL"
            failure_reasons.append(io_status)

        return {
            "filename": filename,
            "file_type": "video",

            "io_status": io_status,

            "width": width,
            "height": height,

            "fps": (
                round(fps, 2)
                if fps is not None
                else None
            ),

            "frame_count": frame_count,

            "duration": (
                round(duration, 2)
                if duration is not None
                else None
            ),

            "blur_score": None,
            "brightness_score": None,

            "resolution_status": resolution_status,

            "blur_status": "N/A",
            "exposure_status": "N/A",

            "fps_status": fps_status,

            "verdict": verdict,

            "failure_reason": (
                "; ".join(failure_reasons)
                if failure_reasons
                else ""
            )
        }

    except Exception as exc:
        logger.exception(
            f"视频检测发生异常: {filename}"
        )

        return {
            "filename": filename,
            "file_type": "video",

            "io_status": "ERROR",

            "width": None,
            "height": None,

            "fps": None,
            "frame_count": None,
            "duration": None,

            "blur_score": None,
            "brightness_score": None,

            "resolution_status": "NOT_RUN",

            "blur_status": "N/A",
            "exposure_status": "N/A",

            "fps_status": "NOT_RUN",

            "verdict": "ERROR",

            "failure_reason": (
                f"{type(exc).__name__}: {exc}"
            )
        }


# =========================================================
# 批量测试
# =========================================================

def run_batch_tests():

    # 1. 加载配置和日志
    cfg = load_config()
    logger = setup_logger()

    logger.info(
        "========== 开始 SmartVisionQA 批量测试 =========="
    )

    results = []

    # =====================================================
    # 2. 扫描图片
    # =====================================================

    if IMAGE_DIR.exists():

        image_files = sorted(
            [
                path
                for path in IMAGE_DIR.iterdir()
                if path.is_file()
                and path.suffix.lower()
                in {
                    ".jpg",
                    ".jpeg",
                    ".png"
                }
            ]
        )

        for image_path in image_files:

            result = evaluate_image(
                image_path.name,
                cfg,
                logger
            )

            results.append(result)

    else:
        logger.warning(
            f"图片目录不存在: {IMAGE_DIR}"
        )

    # =====================================================
    # 3. 扫描视频
    # =====================================================

    if VIDEO_DIR.exists():

        video_files = sorted(
            [
                path
                for path in VIDEO_DIR.iterdir()
                if path.is_file()
                and path.suffix.lower()
                in {
                    ".mp4",
                    ".avi",
                    ".mov",
                    ".mkv"
                }
            ]
        )

        for video_path in video_files:

            result = evaluate_video(
                video_path.name,
                cfg,
                logger
            )

            results.append(result)

    else:
        logger.warning(
            f"视频目录不存在: {VIDEO_DIR}"
        )

    # =====================================================
    # 4. 创建报告目录
    # =====================================================

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # =====================================================
    # 5. 构造 DataFrame
    # =====================================================

    columns = [
        "filename",
        "file_type",

        "io_status",

        "width",
        "height",

        "fps",
        "frame_count",
        "duration",

        "blur_score",
        "brightness_score",

        "resolution_status",
        "blur_status",
        "exposure_status",
        "fps_status",

        "verdict",
        "failure_reason"
    ]

    df = pd.DataFrame(
        results,
        columns=columns
    )

    # =====================================================
    # 6. 输出 CSV
    # =====================================================

    csv_path = (
        REPORT_DIR
        / "test_report.csv"
    )

    df.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig"
    )

    logger.info(
        f"批量测试完成，共处理 {len(df)} 个文件。"
    )

    logger.info(
        f"CSV 报告已保存至: {csv_path}"
    )

    # =====================================================
    # 7. 测试统计
    # =====================================================

    print()
    print(
        "===== SmartVisionQA 测试统计 ====="
    )

    total = len(df)

    if total == 0:

        print(
            "没有发现可测试的媒体文件。"
        )

        logger.warning(
            "未发现可测试的媒体文件。"
        )

        return df

    passed = int(
        (df["verdict"] == "PASS").sum()
    )

    failed = int(
        (df["verdict"] == "FAIL").sum()
    )

    errors = int(
        (df["verdict"] == "ERROR").sum()
    )

    pass_rate = (
        passed / total * 100
    )

    print(
        f"总文件数：{total}"
    )

    print(
        f"PASS：{passed}"
    )

    print(
        f"FAIL：{failed}"
    )

    print(
        f"ERROR：{errors}"
    )

    print(
        f"通过率：{pass_rate:.2f}%"
    )

    print()
    print("各状态分布：")

    print(
        df["verdict"]
        .value_counts()
    )

    print(
        "================================="
    )

    # =====================================================
    # 8. 打印异常文件
    # =====================================================

    failed_df = df[
        df["verdict"] != "PASS"
    ]

    if not failed_df.empty:

        print()
        print(
            "===== 异常文件 ====="
        )

        print(
            failed_df[
                [
                    "filename",
                    "file_type",
                    "verdict",
                    "failure_reason"
                ]
            ].to_string(
                index=False
            )
        )

    return df


# =========================================================
# 程序入口
# =========================================================

if __name__ == "__main__":
    run_batch_tests()