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

    # 跳转到创蓝云智客户平台签名管理页面
    page.goto(f"{env_config['create_signature_url']}")

    # 填写签名名称（取自配置文件）
    page.get_by_role("textbox", name="* 签名名称").click()
    page.get_by_role("textbox", name="* 签名名称").fill(f"{env_config['signature']}")
    page.screenshot(path=os.path.join(sd, "fill_name.png"))

    # 选择签名类型
    page.get_by_role("combobox", name="* 签名类型").click()
    page.get_by_text("企业名称", exact=True).click()

    page.get_by_text("关联资质用途").click()
    # 选择签名归属为"他用"（签名归属他人实名认证主体，需上传授权书）
    page.get_by_role("radio", name="他用（签名为非本账号实名认证的企事业单位、商标等）").check()

    # 选择终端客户（取自配置文件）
    page.get_by_role("combobox", name="* 终端客户信息").click()
    page.get_by_text(f"{env_config['company']}").click()
    page.screenshot(path=os.path.join(sd, "select_customer.png"))

    # 提交审核
    page.get_by_role("button", name="提交审核").click()

    # 断言：等待任意弹窗出现后，再断言成功提示文字可见
    expect(page.get_by_text("您的签名已提交审核", exact=False)).to_be_visible(timeout=30000)
    page.screenshot(path=os.path.join(sd, "submit_success.png"))
    # 关闭成功提示弹窗
    page.get_by_role("button", name="我知道了").click()

    # 智能运营审核签名（新标签页）
    new_page = page.context.new_page()
    new_page.bring_to_front()
    new_page.goto(f"{env_config['smart_audit_signature_url']}")
    # 搜索刚提交的签名
    new_page.get_by_role("textbox", name="请输入签名搜索").click()
    new_page.get_by_role("textbox", name="请输入签名搜索").fill(f"{env_config['signature']}")
    new_page.get_by_role("button", name="搜 索").click()
    # 审核通过（first 防止多条记录时误点）
    new_page.get_by_text("通过", exact=True).first.click()
    # 弹窗二次确认
    new_page.get_by_role("button", name="确 认").click()
    #切换回原标签页
    page.bring_to_front()



