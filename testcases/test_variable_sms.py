"""
test_variable_sms.py - 变量短信群发测试用例

测试流程：打开发送页面 -> 选择模板 -> 导入变量文件 -> 提交群发任务 -> 立即发送
"""

import os
from playwright.sync_api import expect

PROJECT_ROOT = r"C:\Users\15274\PycharmProjects\playwright_test"
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshot")


def test_send_variable_sms(browser_context, env_config):
    """测试变量短信群发功能"""
    page = browser_context
    sd = SCREENSHOT_DIR

    # 打开变量短信发送页面
    page.goto(f"{env_config['variable_send_url']}")
    page.screenshot(path=os.path.join(sd, "c2_home.png"))

    # 进入变量短信群发功能
    page.get_by_role("link", name="变量短信发送", exact=True).click()
    page.get_by_role("button", name="短信群发").click()

    # 选择短信模板
    page.locator("#onlinesendForm").get_by_text("选择模板").click()
    page.get_by_role("textbox", name="模板内容 :").click()
    page.get_by_role("textbox", name="模板内容 :").fill(f"{env_config['variable_template']}")
    page.get_by_role("button", name="查 询").click()
    page.locator("table tbody tr a").filter(has_text="选择").first.click()

    # 导入变量内容文件
    page.get_by_role("button", name="导入变量内容").click()
    page.screenshot(path=os.path.join(sd, "c2_import_dialog.png"))

    with page.expect_file_chooser() as fc_info:
        page.get_by_role("heading", name="点击或将文件拖拽到这里上传").click()
    file_chooser = fc_info.value
    local_file_path = os.path.abspath(r"C:\Users\15274\OneDrive\guoneibianliang.txt")
    print(f"\n[INFO] 上传文件路径：{local_file_path}")
    file_chooser.set_files(local_file_path)

    # 开始上传并等待完成
    page.get_by_role("button", name="开始上传").click()
    page.screenshot(path=os.path.join(sd, "c2_uploaded.png"))

    # 提交群发任务并立即发送
    page.get_by_role("button", name="提交短信群发任务").click()
    page.get_by_role("button", name="立即发送").click()
    page.screenshot(path=os.path.join(sd, "c2_success.png"))

    # 断言：验证发送成功
    expect(
        page.locator("html").get_by_role("document").filter(has_text="已经成功提交发送")
    ).to_be_visible()
