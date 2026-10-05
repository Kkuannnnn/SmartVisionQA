# SmartVisionQA——图片/视频自动化测试原型

## 📖 项目背景
本项目是一个基于 Python、OpenCV 和 pytest 搭建的图片/视频自动化测试原型，旨在对多媒体文件进行文件完整性、规格合规性及基础画质异常的自动化检测，并生成结构化测试报告。

⚠️ **重要声明**：本项目属于**自动化测试原型**，主要目的是验证测试开发流程，不涉及复杂计算机视觉算法，检测指标（如拉普拉斯方差）也非工业级画质评价标准。

## 🛠️ 技术栈
- Python 3.11
- OpenCV (图像处理、视频读取)
- FFmpeg / ffprobe (视频元数据提取)
- pytest (自动化测试框架)
- Pandas (测试结果汇总)
- PyYAML (配置加载)
- logging (日志记录)

## 📁 目录结构
```text
SmartVisionQA/
├── samples/                # 图片测试样本
├── video_samples/          # 视频测试样本
├── tests/                  # pytest 测试用例
├── logs/                   # 测试日志输出
├── reports/                # CSV 和 HTML 测试报告
├── config.yaml             # 测试阈值配置
├── image_inspector.py      # 图片检测模块
├── video_inspector.py      # 视频检测模块
├── run_tests.py            # 批量测试执行入口
├── generate_report.py      # HTML 报告生成器
└── requirements.txt