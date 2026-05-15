"""
test_signature_template.py - 签名与模板管理测试用例

测试流程：新建签名 -> 提交审核 -> 搜索签名 -> 删除签名 -> 新建模板 -> 提交审核 -> 搜索模板 -> 删除模板
"""

import os
from playwright.sync_api import expect

PROJECT_ROOT = r"C:\Users\15274\PycharmProjects\playwright_test"
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshot")


def test_signature(browser_context, env_config):
    page = browser_context
    sd = SCREENSHOT_DIR

    # ===== 签名部分 =====

    page.goto(f"{env_config['create_signature_url']}")

    page.get_by_role("button", name="新建签名").click()

    page.get_by_role("textbox", name="* 签名名称").click()
    page.get_by_role("textbox", name="* 签名名称").fill(f"{env_config['signature']}")
    page.screenshot(path=os.path.join(sd, "fill_name.png"))

    page.get_by_role("combobox", name="* 行业选择").click()
    page.get_by_text("网络游戏").click()

    page.get_by_role("combobox", name="* 签名类型").click()
    page.get_by_text("企业名称").click()

    page.get_by_role("radio", name="他用(签名为他人实名认证的企业事业单位、APP、商标等)").check()

    page.get_by_role("textbox", name="* APP/官网链接").click()
    page.get_by_role("textbox", name="* APP/官网链接").fill("1")

    page.get_by_role("combobox", name="* 终端客户信息").click()
    page.get_by_text(f"{env_config['company']}").click()
    page.screenshot(path=os.path.join(sd, "select_customer.png"))

    # 上传签名授权书
    auth_file = os.path.join(PROJECT_ROOT, "签名授权书.png")
    with page.expect_file_chooser() as fc_info:
        page.locator(".sms-upload").nth(2).click()
    file_chooser = fc_info.value
    file_chooser.set_files(auth_file)
    page.wait_for_timeout(3000)
    page.screenshot(path=os.path.join(sd, "upload_auth.png"))

    # 提交审核
    page.get_by_role("button", name="提交审核").click()

    expect(page.get_by_text("您的签名已提交审核", exact=False)).to_be_visible(timeout=10000)
    page.screenshot(path=os.path.join(sd, "submit_success.png"))
    page.get_by_role("button", name="我知道了").click()

    # 智能运营审核签名（新标签页）
    new_page = page.context.new_page()
    new_page.bring_to_front()
    new_page.goto("https://smart-operation.new253.com/child-risk/review/sign-apply")
    new_page.get_by_role("textbox", name="请输入签名搜索").click()
    new_page.get_by_role("textbox", name="请输入签名搜索").fill("prod自动化测试签名")
    new_page.get_by_role("button", name="搜 索").click()
    new_page.get_by_text("通过", exact=True).first.click()
    new_page.get_by_role("button", name="确 认").click()
    #切换回原标签页
    page.bring_to_front()



