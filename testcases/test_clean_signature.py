"""
test_signature_template.py - 签名与模板管理测试用例

测试流程：新建签名 -> 提交审核 -> 搜索签名 -> 删除签名 -> 新建模板 -> 提交审核 -> 搜索模板 -> 删除模板
"""

import os
from playwright.sync_api import expect

PROJECT_ROOT = r"C:\Users\15274\PycharmProjects\playwright_test"
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshot")


def test_clean_signature(browser_context, env_config):
    page = browser_context

    # 智能运营删除签名
    new_page = page.context.new_page()
    new_page.bring_to_front()
    new_page.goto("https://smart-operation.new253.com/child-risk/review/sign-apply")
    new_page.locator(".smart-risk-select-selector").first.click()
    new_page.get_by_text("审核通过").click()
    new_page.get_by_role("textbox", name="请输入签名搜索").click()
    new_page.get_by_role("textbox", name="请输入签名搜索").fill("prod自动化测试签名")
    new_page.get_by_role("button", name="搜 索").click()
    new_page.get_by_text("删除", exact=True).first.click()
    new_page.get_by_role("button", name="确 认").click()

    # 智能运营删除签名子端口
    new_page.goto("https://smart-operation.new253.com/child-resource/pass-support/subport")
    new_page.wait_for_timeout(3000)
    new_page.get_by_role("textbox").first.click()
    new_page.get_by_role("textbox").first.fill("prod自动化测试签名")
    new_page.get_by_role("button", name="搜 索").click()
    new_page.wait_for_timeout(2000)
    new_page.get_by_text("条/页").click()
    new_page.get_by_text("100 条/页").click()
    new_page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tmpl_delete_subport.png"))
    new_page.get_by_role("checkbox", name="Select all").check()
    new_page.get_by_role("button", name="批量停用").click()
    new_page.wait_for_timeout(1000)
    new_page.get_by_role("dialog").get_by_text("测试", exact=True).click()
    new_page.get_by_role("button", name="确 认").click()
    new_page.get_by_role("button", name="确 定").click()







