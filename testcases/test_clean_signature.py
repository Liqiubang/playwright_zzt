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
    new_page.goto(f"{env_config['smart_audit_signature_url']}")
    # 筛选状态为"审核通过"的签名
    new_page.locator(".smart-risk-select-selector").first.click()
    new_page.get_by_text("审核通过", exact=True).click()
    # 搜索目标签名
    new_page.get_by_role("textbox", name="请输入签名搜索").click()
    new_page.get_by_role("textbox", name="请输入签名搜索").fill(f"{env_config['signature']}")
    new_page.get_by_role("button", name="搜 索").click()
    # 删除并确认
    new_page.get_by_text("删除", exact=True).first.click()
    new_page.get_by_role("button", name="确 认").click()
    new_page.wait_for_timeout(2000)
    new_page.screenshot(path=os.path.join(SCREENSHOT_DIR, "sig_delete_result.png"))
    # 断言：确认删除成功提示可见（页面提示为"删除成功"）
    expect(new_page.get_by_text("删除成功", exact=True)).to_be_visible(timeout=30000)

    # 智能运营删除签名子端口
    new_page.goto(f"{env_config['smart_signature_subport_url']}")
    # 等待页面加载完成
    new_page.wait_for_timeout(3000)
    # 搜索目标签名的子端口记录
    new_page.get_by_role("textbox").first.click()
    new_page.get_by_role("textbox").first.fill(f"{env_config['signature']}")
    new_page.get_by_role("button", name="搜 索").click()
    new_page.wait_for_timeout(2000)
    # 切换每页显示 100 条，确保全选时覆盖所有记录
    new_page.get_by_text("条/页").click()
    new_page.get_by_text("100 条/页").click()
    # 全选所有记录
    new_page.get_by_role("checkbox", name="Select all").check()
    # 批量停用
    new_page.get_by_role("button", name="批量停用").click()
    new_page.wait_for_timeout(1000)
    # 停用原因选择"测试"
    new_page.get_by_role("dialog").get_by_text("测试", exact=True).click()
    new_page.get_by_role("button", name="确 认").click()
    new_page.get_by_role("button", name="确 定").click()
    new_page.screenshot(path=os.path.join(SCREENSHOT_DIR, "sig_delete_subport.png"))







