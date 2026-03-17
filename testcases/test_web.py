import pytest
import json
import os
import base64
from datetime import datetime
from playwright.sync_api import Page, expect, sync_playwright


class TestWeb():

    TOKEN_FILE = "token.json"

    @staticmethod
    def load_token():
        """从文件加载 token"""
        if os.path.exists(TestWeb.TOKEN_FILE):
            with open(TestWeb.TOKEN_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    @pytest.fixture(scope="session")
    def browser_context(self):
        """创建浏览器上下文，支持免登录"""
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,  # 关闭无头模式，显示浏览器
                slow_mo=500  # 每个操作延迟 500ms，方便观察
            )

            # 尝试加载保存的 token
            token_data = self.load_token()

            if token_data:
                # 使用保存的 token 创建上下文
                context = browser.new_context()
                context.add_cookies(token_data.get("cookies", []))
                page = context.new_page()
                print("\n[OK] 使用保存的 token 免登录")
            else:
                # 正常创建上下文（需要登录）
                context = browser.new_context()
                page = context.new_page()
                print("\n[OK] 未检测到 token，需要登录")

            page.set_viewport_size({"width": 1920, "height": 1080})
            yield page
            browser.close()

    def test_example(self, browser_context):
        page = browser_context
        page.goto("http://172.16.41.223:9999/control/sms/cl_yzm_sms/home")
        page.wait_for_timeout(2000)

        # 截图：首页
        page.screenshot(path="screenshot_home.png")

        page.get_by_role("link", name="短信发送", exact=True).click()
        page.get_by_role("button", name="短信群发").click()
        page.get_by_role("button", name="手动添加").click()
        page.locator(".textarea_wrap--8U8hn").click()
        page.get_by_role("dialog", name="手动添加").get_by_role("textbox").fill("15274438093")
        page.get_by_role("button", name="确 定").click()

        # 截图：添加号码后
        page.wait_for_timeout(1000)
        page.screenshot(path="screenshot_add_number.png")

        page.get_by_role("textbox").nth(3).click()
        page.locator("#onlinesendForm").get_by_role("paragraph").click()
        page.get_by_role("textbox").nth(3).fill("测试短信")
        page.get_by_role("button", name="提交短信群发任务").click()
        page.get_by_role("button", name="立即发送").click()

        # 截图：发送成功提示
        page.wait_for_timeout(2000)
        page.screenshot(path="screenshot_success.png")

        # 验证发送成功
        expect(page.locator("html").get_by_role("document")).to_contain_text("已经成功提交发送")


def generate_html_report(test_results):
    """生成 HTML 测试报告"""

    # 读取截图并转换为 base64
    screenshots = {}
    for name in ["screenshot_home.png", "screenshot_add_number.png", "screenshot_success.png"]:
        if os.path.exists(name):
            with open(name, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
                screenshots[name] = f"data:image/png;base64,{img_data}"

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
        .screenshots {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; padding: 20px; }}
        .screenshot-card {{ background: #f8f9fa; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .screenshot-card h3 {{ padding: 15px; background: #fff; color: #333; font-size: 14px; }}
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
            <p>短信发送功能自动化测试</p>
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
            <h2>测试信息</h2>
            <table class="info-table">
                <tr><th>测试 URL</th><td>http://172.16.41.223:9999/control/sms/cl_yzm_sms/home</td></tr>
                <tr><th>测试时间</th><td>{test_results['timestamp']}</td></tr>
                <tr><th>测试结果</th><td class="{'status-pass' if test_results['passed'] else 'status-fail'}">{'✅ PASSED (通过)' if test_results['passed'] else '❌ FAILED (失败)'}</td></tr>
                <tr><th>免登录状态</th><td>{'✅ 已使用保存的 token' if test_results['use_token'] else '⚠️ 未检测到 token'}</td></tr>
            </table>
        </div>

        <div class="test-info">
            <h2>测试步骤截图</h2>
            <div class="screenshots">
'''

    screenshot_names = {
        "screenshot_home.png": "1️⃣ 首页",
        "screenshot_add_number.png": "2️⃣ 添加手机号",
        "screenshot_success.png": "3️⃣ 发送成功"
    }

    for name, title in screenshot_names.items():
        if name in screenshots:
            html_content += f'''
                <div class="screenshot-card">
                    <h3>{title}</h3>
                    <img src="{screenshots[name]}" alt="{name}">
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

    with open("test_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n[OK] HTML 测试报告已生成：test_report.html")
    return "test_report.html"


if __name__ == "__main__":
    import sys

    # 记录测试开始时间
    start_time = datetime.now()

    # 运行 pytest 测试
    exit_code = pytest.main([
        __file__,
        "-v",
        "-s",
        "--tb=short",
        "--html=test_report_raw.html",
        "--self-contained-html"
    ])

    # 生成自定义 HTML 报告
    test_results = {
        "total": 1,
        "passed_count": 1 if exit_code == 0 else 0,
        "failed_count": 0 if exit_code == 0 else 1,
        "passed": exit_code == 0,
        "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "use_token": os.path.exists(TestWeb.TOKEN_FILE)
    }

    generate_html_report(test_results)

    sys.exit(exit_code)
