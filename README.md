# SmartVisionQA —— 图片 / 视频自动化测试原型

![Python](https://img.shields.io/badge/Python-3.11-blue)
![pytest](https://img.shields.io/badge/pytest-39%20tests-green)
![CI](https://github.com/Kkuannnnn/SmartVisionQA/actions/workflows/test.yml/badge.svg)

## 📖 项目简介

SmartVisionQA 是一个基于 Python、OpenCV、pytest 和 FFmpeg / ffprobe 搭建的多媒体自动化测试原型。

项目面向图片与视频质量验证场景，实现文件完整性、分辨率、帧率、模糊、曝光及视频元数据等规则检测，并支持异常样本测试、边界值测试、Mock 外部依赖、批量测试以及 CSV / HTML 测试报告生成。

项目重点不在复杂计算机视觉算法，而在于实践一套较完整的测试开发流程：

```text
测试样本
    ↓
检测模块
    ↓
规则判断
    ↓
pytest 自动化测试
    ↓
批量执行
    ↓
日志与结构化报告
    ↓
GitHub Actions 自动回归
```

> ⚠️ 本项目属于自动化测试学习与验证原型。
> 模糊度、曝光等指标使用实验性规则，不代表工业级图像质量评价标准。

---

## 🛠️ 技术栈

- Python 3.11
- OpenCV
  - 图片解码
  - 视频读取
  - 分辨率 / FPS 获取
  - 灰度处理
  - Laplacian 清晰度计算
- FFmpeg / ffprobe
  - 视频编码格式
  - 码率
  - 时长
  - 视频流元数据
- pytest
  - 参数化测试
  - 边界值测试
  - Mock / monkeypatch
  - 自动化回归测试
- Pandas
  - 测试结果汇总
  - CSV 报告生成
- PyYAML
  - 测试阈值配置
- logging
  - 测试执行日志
- GitHub Actions
  - 持续集成与自动回归

---

## 📁 项目结构

```text
SmartVisionQA/
├── .github/
│   └── workflows/
│       └── test.yml               # GitHub Actions CI
│
├── samples/                       # 图片测试样本
│   ├── test_backup.jpg            # 正常图片
│   ├── blurred.jpg                # 模糊图片
│   ├── bright.jpg                 # 过曝图片
│   ├── dark.jpg                   # 欠曝图片
│   ├── low_resolution.jpg         # 低分辨率图片
│   └── broken.jpg                 # 损坏图片
│
├── video_samples/                 # 视频测试样本
│   ├── test_video.mp4             # 正常视频
│   ├── low_resolution_video.mp4   # 低分辨率视频
│   ├── broken_video.mp4           # 损坏视频
│   └── empty_video.mp4            # 空视频文件
│
├── tests/
│   ├── test_image_inspector.py    # 图片测试
│   ├── test_video_inspector.py    # 视频及边界测试
│   └── test_ffmpeg.py             # ffprobe Mock 测试
│
├── reports/
│   ├── test_report.csv            # CSV 测试报告
│   └── test_report.html           # HTML 测试报告
│
├── config.yaml                    # 测试阈值配置
├── image_inspector.py             # 图片检测模块
├── video_inspector.py             # 视频检测模块
├── ffmpeg_test.py                 # ffprobe 元数据获取
├── create_test_samples.py         # 图片异常样本生成
├── create_video_samples.py        # 视频异常样本生成
├── run_tests.py                   # 批量检测入口
├── generate_report.py             # HTML 报告生成
├── utils.py                       # 配置及日志工具
├── requirements.txt
└── README.md
```

---

## ✅ 已实现功能

### 1. 图片基础检测

支持检测：

- 文件不存在
- 图片解码失败
- 图片分辨率
- 低分辨率异常

典型状态：

```text
OK
FILE_NOT_FOUND
DECODE_FAILED
RESOLUTION_TOO_LOW
```

---

### 2. 图片模糊检测

使用灰度图与 Laplacian 方差构建基础清晰度指标。

为了降低亮度变化对模糊检测的影响，在计算 Laplacian 前加入灰度直方图均衡化。

实验样本中：

```text
正常图片 blur score   ≈ 59.23
模糊图片 blur score   ≈ 5.54
欠曝图片 blur score   ≈ 73.82
```

当前实验阈值：

```text
blur_threshold = 20
```

当：

```text
blur_score < threshold
```

时返回：

```text
BLURRY
```

该阈值仅针对当前测试样本进行实验性标定。

---

### 3. 曝光检测

根据灰度平均值检测：

```text
UNDEREXPOSED
OK
OVEREXPOSED
```

当前实验配置：

```text
dark_threshold = 70
bright_threshold = 200
```

---

### 4. 视频基础检测

基于 OpenCV 获取：

- 视频宽度
- 视频高度
- FPS
- 总帧数
- 视频时长

并检测：

```text
FILE_NOT_FOUND
OPEN_FAILED
RESOLUTION_TOO_LOW
FPS_TOO_LOW
FPS_INVALID
```

---

### 5. 横屏 / 竖屏分辨率兼容

初版规则直接判断：

```python
width >= min_width and height >= min_height
```

会导致：

```text
720 × 1280
```

的竖屏视频在 `1280 × 720` 规格下被错误判定失败。

项目后续改为：

```text
实际长边 >= 要求长边
且
实际短边 >= 要求短边
```

从而同时兼容：

```text
1280 × 720
720 × 1280
```

---

### 6. FPS 容差

视频标称帧率与实际读取结果可能存在差异，例如：

```text
29.0
29.97
30.0
```

因此帧率检测支持容差：

```python
fps >= min_fps - tolerance
```

当前默认：

```text
tolerance = 1.0
```

例如最低规格为：

```text
30 FPS
```

则：

```text
29 FPS
```

仍可按当前规则判定为符合要求。

---

## 🧪 pytest 自动化测试

项目当前包含约 **39 项自动化测试**，覆盖图片、视频、边界值及 ffprobe 异常场景。

运行：

```bash
python -m pytest -v
```

当前本地与 GitHub Actions 回归测试均可全部通过。

---

## 🎯 边界值测试

项目针对 FPS 和分辨率增加边界值测试。

### FPS

最低规格：

```text
30 FPS
```

容差：

```text
1 FPS
```

测试：

```text
28.9 → FPS_TOO_LOW
29.0 → OK
29.1 → OK
30.0 → OK
```

---

### 分辨率

最低规格：

```text
1280 × 720
```

横屏：

```text
1279 × 720 → FAIL
1280 × 720 → PASS
1281 × 720 → PASS
```

竖屏：

```text
720 × 1279 → FAIL
720 × 1280 → PASS
720 × 1281 → PASS
```

---

## 🧩 Mock 外部依赖测试

为了避免单元测试真实依赖 ffprobe 进程状态，使用 pytest `monkeypatch` 对外部调用进行 Mock。

当前覆盖：

```text
正常 ffprobe JSON
ffprobe 非 0 返回码
ffprobe 执行超时
非法 JSON
不存在 video stream
```

对应异常状态：

```text
FFPROBE_FAILED
FFPROBE_TIMEOUT
INVALID_JSON
NO_VIDEO_STREAM
```

这样可以在不真实破坏 FFmpeg 环境的情况下稳定测试异常处理逻辑。

---

## 📊 批量测试

运行：

```bash
python run_tests.py
```

程序会扫描：

```text
samples/
video_samples/
```

并为每个文件生成：

```text
io_status
resolution_status
blur_status
exposure_status
fps_status
verdict
failure_reason
```

最终统一划分为：

```text
PASS
FAIL
ERROR
```

其中：

- `PASS`：文件正常且满足当前检测规则
- `FAIL`：测试正常执行，但样本违反规格或存在预期异常
- `ERROR`：测试执行过程本身发生异常

---

## 📄 测试报告

批量测试结果写入：

```text
reports/test_report.csv
```

运行：

```bash
python generate_report.py
```

生成：

```text
reports/test_report.html
```

HTML 报告包含：

- 总文件数
- PASS 数量
- FAIL 数量
- ERROR 数量
- 通过率
- 各文件详细检测结果
- 失败原因

---

## ⚙️ 配置文件

检测阈值集中存放于：

```text
config.yaml
```

避免将业务规格分散硬编码到不同模块。

示例：

```yaml
image:
  min_width: 1920
  min_height: 1080
  blur_threshold: 20
  dark_threshold: 70
  bright_threshold: 200

video:
  min_width: 1280
  min_height: 720
  min_fps: 30
```

---

## 🔄 GitHub Actions CI

项目已经配置 GitHub Actions：

```text
.github/workflows/test.yml
```

每次：

```text
push
或
pull request
```

GitHub 会自动执行：

```text
Checkout
↓
安装 Python 3.11
↓
安装 requirements.txt
↓
运行 pytest
↓
输出 CI 结果
```

当前 CI 已成功运行。

---

## 🚀 安装与运行

### 1. 克隆项目

```bash
git clone https://github.com/Kkuannnnn/SmartVisionQA.git
cd SmartVisionQA
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行 pytest

```bash
python -m pytest -v
```

### 4. 执行批量检测

```bash
python run_tests.py
```

### 5. 生成 HTML 报告

```bash
python generate_report.py
```

---

## ⚠️ 当前局限

本项目属于测试开发学习原型，目前仍存在以下限制：

1. 模糊检测使用 Laplacian 方差，结果会受到图像内容、噪声和分辨率影响。
2. 曝光检测基于全图平均灰度，不能替代专业曝光评价算法。
3. 当前阈值主要基于有限测试样本进行实验性标定。
4. FPS 使用固定容差规则，尚未区分不同视频规格和帧率标准。
5. ffprobe 当前本地调用路径依赖具体 FFmpeg 安装环境，需要进一步改为环境变量或 PATH 自动发现。
6. 当前项目主要验证测试开发流程，不属于工业级 Image Quality Assessment 系统。

---

## 📌 项目总结

SmartVisionQA 从一个基础图片 / 视频检测脚本逐步扩展为包含：

```text
异常样本
参数化测试
边界值测试
Mock 外部依赖
配置管理
日志记录
批量执行
CSV / HTML 报告
GitHub Actions CI
```

的多媒体自动化测试原型。

项目重点体现自动化测试场景中的：

```text
测试用例设计
边界分析
异常处理
误报定位
回归测试
外部依赖 Mock
持续集成
```

而非复杂计算机视觉算法本身。