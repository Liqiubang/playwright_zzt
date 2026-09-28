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
    # 跳转到模板管理页面
    page.goto(f"{env_config['create_template_url']}")
    page.get_by_role("textbox", name="* 模板名称 :").click()
    page.get_by_role("textbox", name="* 模板名称 :").fill("测试自动化模板")
    page.get_by_role("paragraph").filter(has_text="请输入模版内容，点击{x}后插入变量").click()
    page.get_by_role("paragraph").filter(has_text="请输入模版内容，点击{x}后插入变量").click()
    page.get_by_role("textbox").filter(has_text="请输入模版内容，点击{x}后插入变量").fill(f"{env_config['constant_template']}")
    page.get_by_role("button", name="提交审核").click()
    page.get_by_role("button", name="我知道了").click()

    # 智能运营审核常量模板
    new_page = page.context.new_page()
    new_page.bring_to_front()
    new_page.goto(f"{env_config['smart_audit_template_url']}")
    # 按模板内容搜索刚提交的常量模板
    new_page.get_by_role("textbox", name="模板内容").click()
    new_page.get_by_role("textbox", name="模板内容").fill(f"{env_config['constant_template']}")
    new_page.get_by_role("button", name="搜 索").click()
    # 审核通过
    new_page.get_by_text("通过", exact=True).first.click()
    new_page.get_by_role("button", name="确 认").click()


    # ===== 新建变量模板 =====
    page.bring_to_front()
    page.goto(f"{env_config['create_template_url']}")
    page.get_by_role("textbox", name="* 模板名称 :").click()
    page.get_by_role("textbox", name="* 模板名称 :").fill("测试自动化模板")
    page.get_by_role("paragraph").filter(has_text="请输入模版内容，点击{x}后插入变量").click()
    page.get_by_role("paragraph").filter(has_text="请输入模版内容，点击{x}后插入变量").click()
    page.get_by_role("textbox").filter(has_text="请输入模版内容，点击{x}后插入变量").fill(f"{env_config['variable_template']}")
    # page.locator(".sms-col > .sms-select > .sms-select-selector > .sms-select-selection-item").click()
    page.get_by_role("combobox").nth(1).click()
    page.get_by_text("字符型").click()
    # 填写变量长度：通过输入框后缀“个字”唯一定位长度输入框，避免按 textbox 索引误选
    length_input = page.locator(".ant-input-affix-wrapper:has-text('个字') input")
    length_input.wait_for(state="visible", timeout=5000)
    length_input.click()
    length_input.fill("10")
    page.get_by_role("button", name="提交审核").click()
    page.get_by_role("button", name="我知道了").click()

    # 智能运营审核变量模板
    new_page = page.context.new_page()
    new_page.bring_to_front()
    new_page.goto(f"{env_config['smart_audit_template_url']}")
    # 按模板内容搜索刚提交的变量模板
    new_page.get_by_role("textbox", name="模板内容").click()
    new_page.get_by_role("textbox", name="模板内容").fill(f"{env_config['variable_template']}")
    new_page.get_by_role("button", name="搜 索").click()
    # 审核通过
    new_page.get_by_text("通过", exact=True).first.click()
    new_page.get_by_role("button", name="确 认").click()
    # 切换回原标签页
    page.bring_to_front()