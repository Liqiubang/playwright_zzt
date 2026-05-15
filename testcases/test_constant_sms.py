"""
test_constant_sms.py - 固定短信群发测试用例

测试流程：打开发送页面 -> 手动添加手机号 -> 选择模板 -> 提交群发任务 -> 立即发送
"""

import os
from playwright.sync_api import expect

PROJECT_ROOT = r"C:\Users\15274\PycharmProjects\playwright_test"
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshot")


def test_send_constant_sms(browser_context, env_config):
    """测试固定短信群发功能"""
    page = browser_context
    sd = SCREENSHOT_DIR

    # 打开固定短信发送页面
    page.goto(f"{env_config['constant_send_url']}")
    page.screenshot(path=os.path.join(sd, "c1_home.png"))

    # 进入短信群发功能
    page.get_by_role("link", name="短信发送", exact=True).click()
    page.get_by_role("button", name="短信群发").click()

    # 手动添加手机号
    page.get_by_role("button", name="手动添加").click()
    page.get_by_role("dialog", name="手动添加").get_by_role("textbox").fill(f"{env_config['phone']}")
    page.get_by_role("button", name="确 定").click()
    page.screenshot(path=os.path.join(sd, "c1_add_number.png"))

    # 选择短信模板
    page.locator("#onlinesendForm").get_by_text("选择模板").click()
    page.get_by_role("textbox", name="模板内容 :").click()
    page.get_by_role("textbox", name="模板内容 :").fill(f"{env_config['constant_template']}")
    page.get_by_role("button", name="查 询").click()
    page.locator("table tbody tr a").filter(has_text="选择").first.click()

    # 提交群发任务并立即发送
    page.get_by_role("button", name="提交短信群发任务").click()
    page.get_by_role("button", name="立即发送").click()
    page.screenshot(path=os.path.join(sd, "c1_success.png"))

    # 断言：验证发送成功
    expect(
        page.locator("html").get_by_role("document").filter(has_text="已经成功提交发送")
    ).to_be_visible()
