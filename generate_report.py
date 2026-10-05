from pathlib import Path

import pandas as pd


# =========================================================
# 基础路径
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = (
    BASE_DIR
    / "reports"
    / "test_report.csv"
)

HTML_PATH = (
    BASE_DIR
    / "reports"
    / "test_report.html"
)


# =========================================================
# HTML 报告生成
# =========================================================

def generate_html_report():

    # -----------------------------------------------------
    # 1. 检查 CSV 是否存在
    # -----------------------------------------------------

    if not CSV_PATH.exists():
        print(
            "找不到 test_report.csv，请先运行 run_tests.py"
        )
        return

    # -----------------------------------------------------
    # 2. 读取测试结果
    # -----------------------------------------------------

    df = pd.read_csv(CSV_PATH)

    if df.empty:
        print("测试报告为空，没有可展示的数据。")
        return

    # -----------------------------------------------------
    # 3. 计算统计信息
    # -----------------------------------------------------

    total = len(df)

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
        if total > 0
        else 0
    )

    # -----------------------------------------------------
    # 4. 将 verdict 转成带颜色的 HTML
    # -----------------------------------------------------

    def format_verdict(value):

        if value == "PASS":
            return (
                '<span class="status-pass">'
                'PASS'
                '</span>'
            )

        if value == "FAIL":
            return (
                '<span class="status-fail">'
                'FAIL'
                '</span>'
            )

        if value == "ERROR":
            return (
                '<span class="status-error">'
                'ERROR'
                '</span>'
            )

        return str(value)

    display_df = df.copy()

    display_df["verdict"] = (
        display_df["verdict"]
        .apply(format_verdict)
    )

    # -----------------------------------------------------
    # 5. 生成表格 HTML
    # -----------------------------------------------------

    table_html = display_df.to_html(
        index=False,
        escape=False,
        classes="result-table"
    )

    # -----------------------------------------------------
    # 6. 构造完整 HTML
    # -----------------------------------------------------

    html_content = f"""
<!DOCTYPE html>

<html lang="zh-CN">

<head>

<meta charset="UTF-8">

<title>SmartVisionQA 自动化测试报告</title>

<style>

body {{
    font-family:
        Arial,
        "Microsoft YaHei",
        sans-serif;

    margin: 30px;

    background-color: #f5f7fa;

    color: #333;
}}

.container {{
    max-width: 1500px;

    margin: auto;

    background-color: white;

    padding: 30px;

    border-radius: 10px;

    box-shadow:
        0 2px 10px
        rgba(0, 0, 0, 0.08);
}}

h1 {{
    margin-top: 0;

    color: #222;
}}

.subtitle {{
    color: #666;

    margin-bottom: 30px;
}}

.summary {{
    display: flex;

    flex-wrap: wrap;

    gap: 15px;

    margin-bottom: 30px;
}}

.card {{
    min-width: 150px;

    padding: 18px;

    border-radius: 8px;

    background-color: #f0f2f5;
}}

.card-title {{
    font-size: 14px;

    color: #666;

    margin-bottom: 8px;
}}

.card-value {{
    font-size: 26px;

    font-weight: bold;
}}

.pass-card {{
    background-color: #e8f5e9;
}}

.fail-card {{
    background-color: #ffebee;
}}

.error-card {{
    background-color: #fff3e0;
}}

.rate-card {{
    background-color: #e3f2fd;
}}

.status-pass {{
    color: #16803c;

    font-weight: bold;
}}

.status-fail {{
    color: #d32f2f;

    font-weight: bold;
}}

.status-error {{
    color: #ef6c00;

    font-weight: bold;
}}

.table-wrapper {{
    overflow-x: auto;
}}

.result-table {{
    width: 100%;

    border-collapse: collapse;

    margin-top: 20px;

    font-size: 14px;
}}

.result-table th {{
    background-color: #263238;

    color: white;

    padding: 10px;

    text-align: left;

    white-space: nowrap;
}}

.result-table td {{
    border-bottom:
        1px solid #ddd;

    padding: 9px;

    vertical-align: top;
}}

.result-table tr:nth-child(even) {{
    background-color: #f8f9fa;
}}

.result-table tr:hover {{
    background-color: #eef3f8;
}}

.footer {{
    margin-top: 30px;

    color: #888;

    font-size: 13px;
}}

</style>

</head>


<body>

<div class="container">

<h1>
SmartVisionQA 自动化测试报告
</h1>

<div class="subtitle">
图片 / 视频自动化质量检测原型
</div>


<div class="summary">

<div class="card">
<div class="card-title">
总测试文件
</div>

<div class="card-value">
{total}
</div>
</div>


<div class="card pass-card">
<div class="card-title">
PASS
</div>

<div class="card-value">
{passed}
</div>
</div>


<div class="card fail-card">
<div class="card-title">
FAIL
</div>

<div class="card-value">
{failed}
</div>
</div>


<div class="card error-card">
<div class="card-title">
ERROR
</div>

<div class="card-value">
{errors}
</div>
</div>


<div class="card rate-card">
<div class="card-title">
通过率
</div>

<div class="card-value">
{pass_rate:.2f}%
</div>
</div>

</div>


<h2>
测试明细
</h2>

<div class="table-wrapper">

{table_html}

</div>


<div class="footer">

SmartVisionQA 为多媒体自动化测试原型。
模糊、曝光等指标为实验性规则，
不代表工业级画质评价标准。

</div>

</div>

</body>

</html>
"""

    # -----------------------------------------------------
    # 7. 写入 HTML 文件
    # -----------------------------------------------------

    HTML_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        HTML_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            html_content
        )

    # -----------------------------------------------------
    # 8. 输出结果
    # -----------------------------------------------------

    print(
        f"HTML 报告已生成：{HTML_PATH}"
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


# =========================================================
# 程序入口
# =========================================================

if __name__ == "__main__":
    generate_html_report()