import pytest
import json
import os
import base64
from datetime import datetime
from playwright.sync_api import Page, expect


class TestWeb():
    SCREENSHOT_DIR = "screenshot"
    REPORT_DIR = "report"
    TOKEN_FILE = "utils/token.json"


def test_send_constant_sms(browser_context,env_config):
    page = browser_context
    page.goto(f"{env_config['constant_send_url']}")
    page.wait_for_timeout(1000)

    # 截图：首页
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "c1_home.png"))

    page.get_by_role("link", name="短信发送", exact=True).click()
    page.get_by_role("button", name="短信群发").click()
    page.get_by_role("button", name="手动添加").click()
    page.get_by_role("dialog", name="手动添加").get_by_role("textbox").fill(f"{env_config['phone']}")
    page.get_by_role("button", name="确 定").click()

    # 截图：添加号码后
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "c2_add_number.png"))

    page.locator("#onlinesendForm").get_by_text("选择模板").click()
    page.get_by_role("textbox", name="模板内容 :").click()
    page.get_by_role("textbox", name="模板内容 :").fill(f"{env_config['constant_template']}")
    page.get_by_role("button", name="查 询").click()
    page.get_by_text("选择", exact=True).click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="提交短信群发任务").click()
    page.get_by_role("button", name="立即发送").click()

    # 截图：发送成功
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "c3_success.png"))

    # 验证发送成功
    expect(page.locator("html").get_by_role("document")).to_contain_text("已经成功提交发送")

def test_send_variable_sms(browser_context,env_config):
    page = browser_context
    page.goto(f"{env_config['variable_send_url']}")
    page.wait_for_timeout(1000)

    # 截图：首页
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "v1_home.png"))

    page.get_by_role("link", name="变量短信发送", exact=True).click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="短信群发").click()
    page.wait_for_timeout(500)

    page.locator("#onlinesendForm").get_by_text("选择模板").click()
    page.get_by_role("textbox", name="模板内容 :").click()
    page.get_by_role("textbox", name="模板内容 :").fill(f"{env_config['variable_template']}")
    page.get_by_role("button", name="查 询").click()
    page.get_by_text("选择", exact=True).click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="导入变量内容").click()

    # 等待导入文件对话框出现
    page.wait_for_timeout(1000)

    # 截图：导入文件对话框
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "v2_import_dialog.png"))

    # 使用 file chooser 来上传本地文件
    # 先点击上传区域触发文件选择器
    with page.expect_file_chooser() as fc_info:
        page.get_by_role("heading", name="点击或将文件拖拽到这里上传").click()
    file_chooser = fc_info.value

    # 设置要上传的本地文件路径（使用绝对路径）
    local_file_path = os.path.abspath("C:\\Users\\15274\\OneDrive\\guoneibianliang.txt")
    print(f"\n[INFO] 上传文件路径：{local_file_path}")

    # 设置文件
    file_chooser.set_files(local_file_path)

    page.wait_for_timeout(1000)
    page.get_by_role("button", name="开始上传").click()

    # 截图：上传完成
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "v3_uploaded.png"))

    page.get_by_role("button", name="提交短信群发任务").click()
    page.get_by_role("button", name="立即发送").click()

    # 截图：发送成功
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "v4_success.png"))

    # 验证发送成功
    expect(page.locator("html").get_by_role("document")).to_contain_text("已经成功提交发送")


def generate_html_report(test_results):
    """生成 HTML 测试报告"""

    # 确保报告目录存在
    os.makedirs(TestWeb.REPORT_DIR, exist_ok=True)

    # 读取截图并转换为 base64
    screenshots_constant = {}
    screenshot_files_constant = [
        ("c1_home.png", "1️⃣ 首页"),
        ("c2_add_number.png", "2️⃣ 添加手机号"),
        ("c3_success.png", "3️⃣ 发送成功")
    ]

    screenshots_variable = {}
    screenshot_files_variable = [
        ("v1_home.png", "1️⃣ 首页"),
        ("v2_import_dialog.png", "2️⃣ 导入文件对话框"),
        ("v3_uploaded.png", "3️⃣ 文件上传完成"),
        ("v4_success.png", "4️⃣ 发送成功")
    ]

    for filename, title in screenshot_files_constant:
        filepath = os.path.join(TestWeb.SCREENSHOT_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
                screenshots_constant[filename] = f"data:image/png;base64,{img_data}"

    for filename, title in screenshot_files_variable:
        filepath = os.path.join(TestWeb.SCREENSHOT_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
                screenshots_variable[filename] = f"data:image/png;base64,{img_data}"

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自动化测试报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; padding: 30px; border-radius: 8px 8px 0 0; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .summary {{ display: flex; padding: 20px; gap: 20px; background: #f8f9fa; border-bottom: 1px solid #eee; }}
        .summary-card {{ flex: 1; background: #fff; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .summary-card.success {{ border-left: 4px solid #28a745; }}
        .summary-card.fail {{ border-left: 4px solid #dc3545; }}
        .summary-card .count {{ font-size: 36px; font-weight: bold; color: #333; }}
        .summary-card .label {{ color: #666; margin-top: 5px; }}
        .test-info {{ padding: 20px; }}
        .test-info h2 {{ color: #333; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #667eea; }}
        .info-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        .info-table th, .info-table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        .info-table th {{ background: #f8f9fa; color: #333; font-weight: 600; }}
        .case-section {{ margin: 20px; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
        .case-section h2 {{ color: #333; margin-bottom: 15px; }}
        .case-result {{ display: inline-block; padding: 5px 15px; border-radius: 4px; color: #fff; font-weight: bold; }}
        .case-result.pass {{ background: #28a745; }}
        .case-result.fail {{ background: #dc3545; }}
        .screenshots {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 20px; }}
        .screenshot-card {{ background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .screenshot-card h3 {{ padding: 15px; background: #f8f9fa; color: #333; font-size: 14px; border-bottom: 1px solid #eee; }}
        .screenshot-card img {{ width: 100%; height: auto; display: block; }}
        .footer {{ padding: 20px; text-align: center; color: #666; border-top: 1px solid #eee; }}
        .status-pass {{ color: #28a745; font-weight: bold; }}
        .status-fail {{ color: #dc3545; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 自动化测试报告</h1>
            <p>短信发送功能自动化测试（固定短信 + 变量短信）</p>
        </div>

        <div class="summary">
            <div class="summary-card {'success' if test_results['passed'] else 'fail'}">
                <div class="count">{test_results['total']}</div>
                <div class="label">总测试数</div>
            </div>
            <div class="summary-card {'success' if test_results['passed'] else 'fail'}">
                <div class="count" style="color: {'#28a745' if test_results['passed'] else '#dc3545'}">{test_results['passed_count']}</div>
                <div class="label">通过</div>
            </div>
            <div class="summary-card {'success' if not test_results['passed'] else ''}">
                <div class="count" style="color: {'#dc3545' if not test_results['passed'] else '#28a745'}">{test_results['failed_count']}</div>
                <div class="label">失败</div>
            </div>
        </div>

        <div class="test-info">
            <h2>测试概要</h2>
            <table class="info-table">
                <tr><th>测试 URL</th><td>http://172.16.41.223:9999/control/sms/cl_yzm_sms/home</td></tr>
                <tr><th>测试时间</th><td>{test_results['timestamp']}</td></tr>
                <tr><th>整体结果</th><td class="{'status-pass' if test_results['passed'] else 'status-fail'}">{'✅ PASSED (通过)' if test_results['passed'] else '❌ FAILED (失败)'}</td></tr>
                <tr><th>免登录状态</th><td>{'✅ 已使用保存的 token' if test_results['use_token'] else '⚠️ 未检测到 token'}</td></tr>
            </table>
        </div>
'''

    # 用例 1：固定短信发送
    case1_result = test_results['cases'].get('testcases/test_web.py::test_send_constant_sms', {})
    case1_passed = case1_result.get('passed', False)
    html_content += f'''
        <div class="case-section">
            <h2>用例 1：固定短信发送 <span class="case-result {'pass' if case1_passed else 'fail'}">{'PASSED' if case1_passed else 'FAILED'}</span></h2>
            <table class="info-table">
                <tr><th>测试说明</th><td>手动添加手机号，发送固定内容的短信</td></tr>
                <tr><th>测试结果</th><td class="{'status-pass' if case1_passed else 'status-fail'}">{'✅ 通过' if case1_passed else '❌ 失败'}</td></tr>
            </table>
            <h3 style="margin-top: 20px; color: #333;">测试步骤截图</h3>
            <div class="screenshots">
'''
    for filename, title in screenshot_files_constant:
        if filename in screenshots_constant:
            html_content += f'''
                <div class="screenshot-card">
                    <h3>{title}</h3>
                    <img src="{screenshots_constant[filename]}" alt="{filename}">
                </div>
'''
    html_content += '''
            </div>
        </div>
'''

    # 用例 2：变量短信发送
    case2_result = test_results['cases'].get('testcases/test_web.py::test_send_variable_sms', {})
    case2_passed = case2_result.get('passed', False)
    html_content += f'''
        <div class="case-section">
            <h2>用例 2：变量短信发送 <span class="case-result {'pass' if case2_passed else 'fail'}">{'PASSED' if case2_passed else 'FAILED'}</span></h2>
            <table class="info-table">
                <tr><th>测试说明</th><td>导入文件，发送变量内容的短信</td></tr>
                <tr><th>测试结果</th><td class="{'status-pass' if case2_passed else 'status-fail'}">{'✅ 通过' if case2_passed else '❌ 失败'}</td></tr>
            </table>
            <h3 style="margin-top: 20px; color: #333;">测试步骤截图</h3>
            <div class="screenshots">
'''
    for filename, title in screenshot_files_variable:
        if filename in screenshots_variable:
            html_content += f'''
                <div class="screenshot-card">
                    <h3>{title}</h3>
                    <img src="{screenshots_variable[filename]}" alt="{filename}">
                </div>
'''
    html_content += '''
            </div>
        </div>

        <div class="footer">
            <p>Generated by Playwright Automation Test</p>
        </div>
    </div>
</body>
</html>
'''

    report_path = os.path.join(TestWeb.REPORT_DIR, "test_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n[OK] HTML 测试报告已生成：{report_path}")
    return report_path


if __name__ == "__main__":
    import sys

    # 确保截图目录和报告目录存在
    os.makedirs(TestWeb.SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(TestWeb.REPORT_DIR, exist_ok=True)

    # 记录测试开始时间
    start_time = datetime.now()

    # 运行 pytest 测试，生成 JSON 报告
    json_report_path = os.path.join(TestWeb.REPORT_DIR, "report.json")
    exit_code = pytest.main([
        __file__,
        "-v",
        "-s",
        "--tb=short",
        f"--json-report",
        f"--json-report-file={json_report_path}"
    ])

    # 读取 JSON 报告
    test_results = {
        "total": 2,
        "passed_count": 0,
        "failed_count": 0,
        "passed": exit_code == 0,
        "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "use_token": os.path.exists(TestWeb.TOKEN_FILE),
        "cases": {}
    }

    if os.path.exists(json_report_path):
        with open(json_report_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)
            for test in report_data.get("tests", []):
                test_name = test.get("nodeid", "")
                status = test.get("outcome", "failed")  # JSON 报告中使用 outcome 字段
                test_results["cases"][test_name] = {"passed": status == "passed"}
                if status == "passed":
                    test_results["passed_count"] += 1
                else:
                    test_results["failed_count"] += 1

    generate_html_report(test_results)

    sys.exit(exit_code)
