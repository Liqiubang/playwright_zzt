"""
test_signature_template.py - 签名与模板管理测试用例

测试流程：新建签名 -> 提交审核 -> 搜索签名 -> 删除签名 -> 新建模板 -> 提交审核 -> 搜索模板 -> 删除模板
"""

import os
from playwright.sync_api import expect

PROJECT_ROOT = r"C:\Users\15274\PycharmProjects\playwright_test"
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshot")


def test_template(browser_context, env_config):
    page = browser_context
    sd = SCREENSHOT_DIR

    # ===== 新建常量模板 =====
    page.goto(f"{env_config['create_template_url']}")

    page.get_by_role("button", name="新建模板").click()

    page.get_by_role("textbox", name="* 模板名称").click()
    page.get_by_role("textbox", name="* 模板名称").fill("测试自动化模板")
    page.screenshot(path=os.path.join(sd, "new_template_form.png"))

    page.locator("input#signature").click(force=True)
    page.wait_for_selector(".sms-select-item-option-content", timeout=5000)
    page.locator(".sms-select-item-option-content").filter(has_text=f"{env_config['signature']}").click()

    page.get_by_role("paragraph").nth(4).click()
    page.get_by_role("paragraph").nth(4).click()
    page.get_by_role("textbox").nth(3).fill(f"{env_config['constant_template']}")

    page.locator(".sms-cascader-picker-label").click()
    page.get_by_role("menuitem", name="业务管理和服务类 right").click()
    page.get_by_role("menuitem", name="其他用途").click()

    page.get_by_role("radio", name="拒收请回复R").check()

    page.get_by_role("button", name="提交审核").click()
    page.screenshot(path=os.path.join(sd, "submit_template_success.png"))
    page.get_by_role("button", name="我知道了").click()

    # 智能运营审核常量模板
    new_page = page.context.new_page()
    new_page.bring_to_front()
    new_page.goto("https://smart-operation.new253.com/child-risk/review/text-tem")
    new_page.get_by_role("textbox", name="模板内容").click()
    new_page.get_by_role("textbox", name="模板内容").fill("prod自动化")
    new_page.get_by_role("button", name="搜 索").click()
    new_page.get_by_text("通过", exact=True).first.click()
    new_page.get_by_role("button", name="确 认").click()
    # 切换回原标签页
    page.bring_to_front()

    # ===== 新建变量模板 =====
    page.get_by_role("button", name="新建模板").click()

    page.get_by_role("textbox", name="* 模板名称").click()
    page.get_by_role("textbox", name="* 模板名称").fill("测试自动化模板")
    page.screenshot(path=os.path.join(sd, "new_var_template_form.png"))

    page.locator("input#signature").click(force=True)
    page.wait_for_selector(".sms-select-item-option-content", timeout=5000)
    page.locator(".sms-select-item-option-content").filter(has_text=f"{env_config['signature']}").click()

    page.get_by_role("paragraph").nth(4).click()
    page.get_by_role("paragraph").nth(4).click()
    page.get_by_role("textbox").nth(3).fill(f"{env_config['variable_template']}")

    page.locator(".sms-col > .sms-select > .sms-select-selector > .sms-select-selection-item").click()
    page.get_by_text("字符型", exact=True).click()
    page.get_by_role("textbox").nth(4).click()
    page.get_by_role("textbox").nth(4).fill("10")

    page.locator(".sms-cascader-picker-label").click()
    page.get_by_role("menuitem", name="业务管理和服务类 right").click()
    page.get_by_role("menuitem", name="其他用途").click()

    page.get_by_role("radio", name="拒收请回复R").check()

    page.get_by_role("button", name="提交审核").click()
    page.screenshot(path=os.path.join(sd, "submit_var_template_success.png"))
    page.get_by_role("button", name="我知道了").click()

    # 智能运营审核变量模板
    new_page = page.context.new_page()
    new_page.bring_to_front()
    new_page.goto("https://smart-operation.new253.com/child-risk/review/text-tem")
    new_page.get_by_role("textbox", name="模板内容").click()
    new_page.get_by_role("textbox", name="模板内容").fill("prod自动化")
    new_page.get_by_role("button", name="搜 索").click()
    new_page.get_by_text("通过", exact=True).first.click()
    new_page.get_by_role("button", name="确 认").click()
    # 切换回原标签页
    page.bring_to_front()