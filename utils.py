import os
import yaml
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_config(config_path=None):
    if config_path is None:
        config_path = os.path.join(BASE_DIR, "config.yaml")
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def setup_logger(log_name="SmartVisionQA"):
    """初始化日志系统，同时输出到文件和控制台"""
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # 文件处理器：记录到 logs/test_run.log
        log_dir = os.path.join(BASE_DIR, "logs")
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(log_dir, "test_run.log"), encoding='utf-8')

        # 控制台处理器：输出到终端
        console_handler = logging.StreamHandler()

        # 设置格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    cfg = load_config()
    logger = setup_logger()
    logger.info("✅ 配置加载成功！")
    logger.info(
        f"图片最低要求: {cfg['image']['min_width']}x{cfg['image']['min_height']}, 模糊阈值: {cfg['image']['blur_threshold']}")
    logger.info(f"视频最低帧率: {cfg['video']['min_fps']} FPS")