"""
test_signature_template.py - 签名与模板管理测试用例

测试流程：新建签名 -> 提交审核 -> 搜索签名 -> 删除签名 -> 新建模板 -> 提交审核 -> 搜索模板 -> 删除模板
"""

import os
from playwright.sync_api import expect

PROJECT_ROOT = r"C:\Users\15274\PycharmProjects\playwright_test"
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshot")



def test_clean_template(browser_context, env_config):
    page = browser_context

    # 关闭可能残留的弹窗
    try:
        page.locator(".ant-modal-wrap").evaluate("el => el.style.display = 'none'")
    except Exception:
        pass

    # 自助通删除常量模板
    page.goto("https://www.chuanglan.com/control/sms/cl_market_sms/template")
    page.get_by_role("textbox", name="请输入搜索关键词").click()
    page.get_by_role("textbox", name="请输入搜索关键词").fill("测试自动化模板")
    page.get_by_role("button", name="搜 索").click()
    page.wait_for_timeout(2000)
    page.get_by_role("checkbox").first.check()
    page.get_by_role("button", name="批量删除模板").click()
    page.get_by_role("button", name="确 定").click()

    expect(page.get_by_text("删除模板成功")).to_be_visible()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tmpl_delete_result.png"))






