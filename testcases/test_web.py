import re

import pytest
import json
import os
import base64
from datetime import datetime
from playwright.sync_api import Page, expect


class TestWeb():
    PROJECT_ROOT = r"C:\Users\15274\PycharmProjects\playwright_test"
    SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshot")
    REPORT_DIR = os.path.join(PROJECT_ROOT, "report")
    TOKEN_FILE = os.path.join(PROJECT_ROOT, "utils", "token.json")

def test_signature_and_template(browser_context, env_config):
    page = browser_context
    sd = TestWeb.SCREENSHOT_DIR

    # ===== 签名部分 =====

    # 步骤1：导航到签名管理页面
    page.goto(f"{env_config['create_signature_url']}")

    # 步骤2：点击"新建签名"按钮，打开新建表单
    page.get_by_role("button", name="新建签名").click()
    # 截图：新建签名表单已弹出
    page.screenshot(path=os.path.join(sd, "s02_new_signature_form.png"))

    # 步骤3：点击签名名称输入框并填写签名名称（来自配置）
    page.get_by_role("textbox", name="* 签名名称").click()
    page.get_by_role("textbox", name="* 签名名称").fill(f"{env_config['signature']}")
    # 截图：签名名称已填写
    page.screenshot(path=os.path.join(sd, "s03_fill_name.png"))

    # 步骤4：点击"行业选择"下拉框，选择"网络游戏"
    page.get_by_role("combobox", name="* 行业选择").click()
    page.get_by_text("网络游戏").click()


    # 步骤5：点击"签名类型"下拉框，选择"企业名称"
    page.get_by_role("combobox", name="* 签名类型").click()
    page.get_by_text("企业名称").click()


    # 步骤6：选择"他用"单选按钮（force=True 绕过遮挡层）
    page.get_by_role("radio", name="他用(签名为他人实名认证的企业事业单位、APP、商标等)").check()


    # 步骤7：点击"APP/官网链接"输入框并填写链接（填"1"占位）
    page.get_by_role("textbox", name="* APP/官网链接").click()
    page.get_by_role("textbox", name="* APP/官网链接").fill("1")


    # 步骤8：点击"终端客户信息"下拉框，选择"深圳市天视通技术有限公司"
    page.get_by_role("combobox", name="* 终端客户信息").click()
    page.get_by_text(f"{env_config['company']}").click()
    # 截图：终端客户已选择
    page.screenshot(path=os.path.join(sd, "s08_select_customer.png"))

    # 步骤8.5：上传签名授权书（"他用"模式必填证明材料）
    auth_file = os.path.join(TestWeb.PROJECT_ROOT, "testdata", "authorization.png")
    with page.expect_file_chooser() as fc_info:
        page.locator(".sms-upload").first.click()
    file_chooser = fc_info.value
    file_chooser.set_files(auth_file)
    # 截图：授权书已上传
    page.screenshot(path=os.path.join(sd, "s09_upload_auth.png"))

    # 步骤9：点击"提交审核"按钮，等待后端响应后截图
    page.get_by_role("button", name="提交审核").click()

    # 步骤10：断言成功弹窗出现（弹窗文本包含该关键词即可），点击"我知道了"关闭弹窗
    expect(page.get_by_text("您的签名已提交审核", exact=False)).to_be_visible(timeout=10000)
    # 截图：提交成功弹窗可见
    page.screenshot(path=os.path.join(sd, "s10_submit_success.png"))
    page.get_by_role("button", name="我知道了").click()

    # # 步骤11：智能运营后台 - 打开新标签页审核签名
    # page2 = page.context.new_page()
    # page2.goto(f"{env_config['smart_audit_signature_url']}")
    # page2.screenshot(path=os.path.join(sd, "s11_smart_audit_page.png"))
    #
    # # 步骤12：搜索签名
    # page2.get_by_role("textbox", name="请输入签名搜索").click()
    # page2.get_by_role("textbox", name="请输入签名搜索").fill(f"{env_config['signature']}")
    # page2.get_by_role("button", name="搜 索").click()
    # page2.wait_for_timeout(2000)
    # page2.screenshot(path=os.path.join(sd, "s12_smart_search_result.png"))
    #
    # # 步骤13：驳回签名
    # page2.get_by_text("驳回", exact=True).click()
    # page2.get_by_text("测试驳回", exact=True).click()
    # page2.screenshot(path=os.path.join(sd, "s13_smart_reject_dialog.png"))
    # page2.get_by_role("button", name="确 认").click()
    # page2.get_by_role("button", name="确 认").click()
    # page2.wait_for_timeout(2000)
    # page2.screenshot(path=os.path.join(sd, "s14_smart_reject_done.png"))
    #
    # # 步骤14：切回自助通页面，搜索并删除被驳回的签名
    # page.bring_to_front()
    # page.wait_for_timeout(2000)
    # page.screenshot(path=os.path.join(sd, "s15_back_to_signature_page.png"))

    # 步骤15：在搜索框中输入签名名称并点击"搜 索"，等待结果加载后截图
    page.get_by_role("textbox", name="请输入搜索关键词").click()
    page.get_by_role("textbox", name="请输入搜索关键词").fill(f"{env_config['signature']}")
    # 点击搜索按钮，触发列表刷新
    page.get_by_role("button", name="搜 索").click()
    # 等待搜索结果中出现签名名称文本，确认数据已加载
    expect(page.get_by_text(env_config['signature'])).to_be_visible(timeout=10000)

    # 步骤16：点击列表中第一个"删除"链接，弹出确认对话框后确认删除

    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(sd, "s17_after_delete.png"))
    page.get_by_text("删除").first.click()
    page.get_by_role("button", name="确 定").click()

    # 断言：验证删除签名成功提示可见（toast消失很快，必须立即断言）
    expect(page.get_by_text("删除签名成功")).to_be_visible()
    # 截图：删除成功 toast 提示
    page.screenshot(path=os.path.join(sd, "s18_delete_result.png"))

    # ===== 模板部分 =====

    # 步骤17：导航到模板管理页面
    page.goto(f"{env_config['create_template_url']}")
    # 截图：模板管理页面
    page.screenshot(path=os.path.join(sd, "t01_template_page.png"))

    # 步骤18：点击"新建模板"按钮，打开新建表单
    page.get_by_role("button", name="新建模板").click()
    # 截图：新建模板表单已弹出
    page.screenshot(path=os.path.join(sd, "t02_new_template_form.png"))

    # 步骤19：填写模板名称
    page.get_by_role("textbox", name="* 模板名称").click()
    page.get_by_role("textbox", name="* 模板名称").fill("测试模板")

    # 步骤20：点击关联签名下拉框（通过 id 定位，force=True 绕过 sms-select-selection-item 遮挡）
    page.locator("input#signature").click(force=True)
    # 等待下拉选项渲染完成后选择"创蓝云智"
    page.wait_for_selector(".sms-select-item-option-content", timeout=5000)
    page.locator(".sms-select-item-option-content").filter(has_text="创蓝云智").click()
    # 截图：模板表单基本信息已填写
    page.screenshot(path=os.path.join(sd, "t03_fill_template_form.png"))

    # 步骤21：点击模板内容编辑区域（第5个 paragraph）激活输入
    page.get_by_role("paragraph").nth(4).click()
    page.get_by_role("paragraph").nth(4).click()
    # 步骤22：在第4个文本框中填写模板正文内容（来自配置）
    page.get_by_role("textbox").nth(3).fill(f"{env_config['template']}")

    # 步骤23：点击模板类型级联选择器，依次选择"业务管理和服务类 > 其他用途"
    page.locator(".sms-cascader-picker-label").click()
    page.get_by_role("menuitem", name="业务管理和服务类 right").click()
    page.get_by_role("menuitem", name="其他用途").click()

    # 步骤24：勾选退订方式"拒收请回复R"单选项
    page.get_by_role("radio", name="拒收请回复R").check()
    # 截图：提交前表单完整状态
    page.screenshot(path=os.path.join(sd, "t04_before_submit.png"))

    # 步骤25：点击"提交审核"按钮，等待后端响应后截图
    page.get_by_role("button", name="提交审核").click()


    # 步骤26：点击"我知道了"关闭提交成功弹窗
    page.get_by_role("button", name="我知道了").click()

    # 步骤27：删除模板
    page.get_by_text("标题").click()
    page.get_by_text("内容", exact=True).click()
    page.get_by_role("textbox", name="请输入搜索关键词").click()
    page.get_by_role("textbox", name="请输入搜索关键词").fill(f"{env_config['template']}")
    page.get_by_role("button", name="搜 索").click()

    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(sd, "t05_after_delete.png"))
    page.get_by_text("删除").first.click()
    page.get_by_role("button", name="确 定").click()

    # 断言：验证删除模板成功提示可见
    expect(page.get_by_text("删除模板成功")).to_be_visible()
    # 截图：删除成功 toast 提示
    page.screenshot(path=os.path.join(sd, "t06_delete_result.png"))

def test_send_constant_sms(browser_context, env_config):
    page = browser_context
    page.goto(f"{env_config['constant_send_url']}")
    # 截图：首页
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "c1_home.png"))
    page.get_by_role("link", name="短信发送", exact=True).click()
    page.get_by_role("button", name="短信群发").click()
    page.get_by_role("button", name="手动添加").click()
    page.get_by_role("dialog", name="手动添加").get_by_role("textbox").fill(f"{env_config['phone']}")
    page.get_by_role("button", name="确 定").click()
    # 截图：添加号码后
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "c1_add_number.png"))
    page.locator("#onlinesendForm").get_by_text("选择模板").click()
    page.get_by_role("textbox", name="模板内容 :").click()
    page.get_by_role("textbox", name="模板内容 :").fill(f"{env_config['constant_template']}")
    page.get_by_role("button", name="查 询").click()
    # 使用更精确的选择器，定位到表格中的"选择"按钮
    page.locator("table tbody tr a").filter(has_text="选择").first.click()
    page.get_by_role("button", name="提交短信群发任务").click()
    page.get_by_role("button", name="立即发送").click()
    # 截图：发送成功
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "c1_success.png"))
    # 验证发送成功
    expect(page.locator("html").get_by_role("document").filter(has_text="已经成功提交发送")).to_be_visible()

    # page.wait_for_timeout(120000)
    # page.goto(f"{env_config['send_records_url']}")
    # # 等待页面加载
    # page.wait_for_timeout(3000)
    # # 获取期望的模板内容（带签名的完整内容）
    # expected_content = f"{env_config['assert_constant_template']}"
    # # 断言 1：验证发送内容与模板内容一致
    # # 在表格中查找包含期望内容的单元格
    # page.wait_for_selector(f'text={expected_content[:20]}', timeout=10000)
    # content_cell = page.locator(f'td:has-text("{expected_content}")').first
    # assert content_cell.count() > 0, f"发送记录中未找到期望的内容：{expected_content}"
    # # 断言 2：验证状态码为 DELIVRD
    # # 查找同一行中的状态码（DELIVRD）
    # status_cell = page.locator('td:has-text("DELIVRD")').first
    # assert status_cell.count() > 0, "发送记录中未找到状态码 DELIVRD"
    # page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "c4_assert.png"))
    # print(f"\n[OK] 断言通过：发送内容包含 '{expected_content[:30]}...'，状态码为 DELIVRD")




def test_send_variable_sms(browser_context, env_config):
    page = browser_context
    page.goto(f"{env_config['variable_send_url']}")
    # 截图：首页
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "c2_home.png"))
    page.get_by_role("link", name="变量短信发送", exact=True).click()
    page.get_by_role("button", name="短信群发").click()
    page.locator("#onlinesendForm").get_by_text("选择模板").click()
    page.get_by_role("textbox", name="模板内容 :").click()
    page.get_by_role("textbox", name="模板内容 :").fill(f"{env_config['variable_template']}")
    page.get_by_role("button", name="查 询").click()
    # 使用更精确的选择器，定位到表格中的"选择"按钮
    page.locator("table tbody tr a").filter(has_text="选择").first.click()
    page.get_by_role("button", name="导入变量内容").click()
    # 截图：导入文件对话框
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "c2_import_dialog.png"))
    # 使用 file chooser 来上传本地文件
    # 先点击上传区域触发文件选择器
    with page.expect_file_chooser() as fc_info:
        page.get_by_role("heading", name="点击或将文件拖拽到这里上传").click()
    file_chooser = fc_info.value
    # 设置要上传的本地文件路径（使用绝对路径）
    local_file_path = os.path.abspath("C:\\Users\\15274\\OneDrive\\guoneibianliang.txt")
    print(f"\n[INFO] 上传文件路径：{local_file_path}")
    # 设置文件
    file_chooser.set_files(local_file_path)
    page.get_by_role("button", name="开始上传").click()
    # 截图：上传完成
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "c2_uploaded.png"))
    page.get_by_role("button", name="提交短信群发任务").click()
    page.get_by_role("button", name="立即发送").click()
    # 截图：发送成功
    page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "c2_success.png"))
    # 验证发送成功
    expect(page.locator("html").get_by_role("document").filter(has_text="已经成功提交发送")).to_be_visible()

    # page.wait_for_timeout(120000)
    # page.goto(f"{env_config['send_records_url']}")
    # # 等待页面加载
    # page.wait_for_timeout(3000)
    # # 获取期望的模板内容（带签名的完整内容）
    # expected_content = f"{env_config['assert_variable_template']}"
    # # 断言 1：验证发送内容与模板内容一致
    # # 在表格中查找包含期望内容的单元格
    # page.wait_for_selector(f'text={expected_content[:20]}', timeout=10000)
    # content_cell = page.locator(f'td:has-text("{expected_content}")').first
    # assert content_cell.count() > 0, f"发送记录中未找到期望的内容：{expected_content}"
    # # 断言 2：验证状态码为 DELIVRD
    # # 查找同一行中的状态码（DELIVRD）
    # status_cell = page.locator('td:has-text("DELIVRD")').first
    # assert status_cell.count() > 0, "发送记录中未找到状态码 DELIVRD"
    # page.screenshot(path=os.path.join(TestWeb.SCREENSHOT_DIR, "v5_assert.png"))
    # print(f"\n[OK] 断言通过：发送内容包含 '{expected_content[:30]}...'，状态码为 DELIVRD")



def _load_screenshots(file_list):
    """读取截图列表并转为 base64 字典"""
    result = {}
    for filename, _ in file_list:
        filepath = os.path.join(TestWeb.SCREENSHOT_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                result[filename] = f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return result


def _render_screenshots(screenshots, file_list):
    """生成截图卡片 HTML"""
    html = ""
    for filename, title in file_list:
        if filename in screenshots:
            html += f'''
                <div class="screenshot-card">
                    <h3>{title}</h3>
                    <img src="{screenshots[filename]}" alt="{filename}">
                </div>'''
    return html


def generate_html_report(test_results):
    """生成 HTML 测试报告"""

    os.makedirs(TestWeb.REPORT_DIR, exist_ok=True)

    # 签名+模板用例截图
    sig_tmpl_files = [
        ("s01_signature_page.png",       "步骤01 签名管理页面"),
        ("s02_new_signature_form.png",    "步骤02 新建签名表单"),
        ("s03_fill_name.png",             "步骤03 填写签名名称"),
        ("s04_select_industry.png",       "步骤04 选择行业"),
        ("s05_select_type.png",           "步骤05 选择签名类型"),
        ("s06_select_self_use.png",       "步骤06 选择自用"),
        ("s07_fill_link.png",             "步骤07 填写APP链接"),
        ("s08_select_customer.png",       "步骤08 选择终端客户"),
        ("s09_submit_audit.png",          "步骤09 提交审核"),
        ("s10_submit_success.png",        "步骤10 提交成功弹窗"),
        ("s16_search_rejected.png",       "步骤11 搜索签名"),
        ("s17_delete_confirm_dialog.png", "步骤12 删除确认弹窗"),
        ("s18_delete_result.png",         "步骤13 删除结果"),
        ("t01_template_page.png",         "步骤14 模板管理页面"),
        ("t02_new_template_form.png",     "步骤15 新建模板表单"),
        ("t03_fill_template_form.png",    "步骤16 填写模板"),
        ("t04_before_submit.png",         "步骤17 提交前"),
        ("t05_after_submit.png",          "步骤18 提交后"),
    ]

    # 固定短信截图
    screenshot_files_constant = [
        ("c1_home.png",       "首页"),
        ("c1_add_number.png", "添加手机号"),
        ("c1_success.png",    "发送成功"),
    ]

    # 变量短信截图
    screenshot_files_variable = [
        ("c2_home.png",          "首页"),
        ("c2_import_dialog.png", "导入文件对话框"),
        ("c2_uploaded.png",      "文件上传完成"),
        ("c2_success.png",       "发送成功"),
    ]

    screenshots_sig_tmpl  = _load_screenshots(sig_tmpl_files)
    screenshots_constant  = _load_screenshots(screenshot_files_constant)
    screenshots_variable  = _load_screenshots(screenshot_files_variable)

    overall_cls = 'success' if test_results['passed'] else 'fail'
    pass_color  = '#28a745' if test_results['passed'] else '#dc3545'
    fail_color  = '#dc3545' if not test_results['passed'] else '#28a745'
    overall_txt = '✅ PASSED (通过)' if test_results['passed'] else '❌ FAILED (失败)'
    token_txt   = '✅ 已使用保存的 token' if test_results['use_token'] else '⚠️ 未检测到 token'

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自动化测试报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
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
        .info-table th {{ background: #f8f9fa; color: #333; font-weight: 600; width: 160px; }}
        .case-section {{ margin: 20px; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
        .case-section h2 {{ color: #333; margin-bottom: 15px; }}
        .case-result {{ display: inline-block; padding: 5px 15px; border-radius: 4px; color: #fff; font-weight: bold; }}
        .case-result.pass {{ background: #28a745; }}
        .case-result.fail {{ background: #dc3545; }}
        .screenshots {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 20px; padding: 20px 0; }}
        .screenshot-card {{ background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .screenshot-card h3 {{ padding: 10px 15px; background: #f0f0f0; color: #444; font-size: 13px; border-bottom: 1px solid #ddd; }}
        .screenshot-card img {{ width: 100%; height: auto; display: block; cursor: zoom-in; }}
        .footer {{ padding: 20px; text-align: center; color: #666; border-top: 1px solid #eee; }}
        .status-pass {{ color: #28a745; font-weight: bold; }}
        .status-fail {{ color: #dc3545; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>自动化测试报告</h1>
            <p>签名与模板创建 / 固定短信 / 变量短信 全流程自动化测试</p>
        </div>
        <div class="summary">
            <div class="summary-card {overall_cls}">
                <div class="count">{test_results['total']}</div>
                <div class="label">总测试数</div>
            </div>
            <div class="summary-card success">
                <div class="count" style="color:{pass_color}">{test_results['passed_count']}</div>
                <div class="label">通过</div>
            </div>
            <div class="summary-card {'fail' if test_results['failed_count'] else 'success'}">
                <div class="count" style="color:{fail_color}">{test_results['failed_count']}</div>
                <div class="label">失败</div>
            </div>
        </div>
        <div class="test-info">
            <h2>测试概要</h2>
            <table class="info-table">
                <tr><th>测试时间</th><td>{test_results['timestamp']}</td></tr>
                <tr><th>整体结果</th><td class="{'status-pass' if test_results['passed'] else 'status-fail'}">{overall_txt}</td></tr>
                <tr><th>免登录状态</th><td>{token_txt}</td></tr>
            </table>
        </div>
'''

    def _case_section(title, nodeid, desc, screenshots_dict, file_list):
        r = test_results['cases'].get(nodeid, {})
        p = r.get('passed', False)
        cls = 'pass' if p else 'fail'
        label = 'PASSED' if p else 'FAILED'
        res_cls = 'status-pass' if p else 'status-fail'
        res_txt = '✅ 通过' if p else '❌ 失败'
        imgs = _render_screenshots(screenshots_dict, file_list)
        return f'''
        <div class="case-section">
            <h2>{title} <span class="case-result {cls}">{label}</span></h2>
            <table class="info-table">
                <tr><th>测试说明</th><td>{desc}</td></tr>
                <tr><th>测试结果</th><td class="{res_cls}">{res_txt}</td></tr>
            </table>
            <h3 style="margin-top:16px;color:#333;">测试步骤截图</h3>
            <div class="screenshots">{imgs}</div>
        </div>'''

    html_content += _case_section(
        "用例 1：签名与模板创建",
        "testcases/test_web.py::test_signature_and_template",
        "新建签名 → 提交审核 → 删除签名；新建模板 → 提交审核 → 删除模板",
        screenshots_sig_tmpl, sig_tmpl_files
    )
    html_content += _case_section(
        "用例 2：固定短信发送",
        "testcases/test_web.py::test_send_constant_sms",
        "手动添加手机号，发送固定内容的短信",
        screenshots_constant, screenshot_files_constant
    )
    html_content += _case_section(
        "用例 3：变量短信发送",
        "testcases/test_web.py::test_send_variable_sms",
        "导入文件，发送变量内容的短信",
        screenshots_variable, screenshot_files_variable
    )

    html_content += '''
        <div class="footer">
            <p>Generated by Playwright Automation Test</p>
        </div>
    </div>
</body>
</html>
'''

    report_path = os.path.join(TestWeb.REPORT_DIR, "test_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n[OK] HTML 测试报告已生成：{report_path}")
    return report_path


if __name__ == "__main__":
    import sys

    # 确保截图目录和报告目录存在
    os.makedirs(TestWeb.SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(TestWeb.REPORT_DIR, exist_ok=True)

    # 记录测试开始时间
    start_time = datetime.now()

    # 运行 pytest 测试，生成 JSON 报告
    json_report_path = os.path.join(TestWeb.REPORT_DIR, "report.json")
    exit_code = pytest.main([
        __file__,
        "-v",
        "-s",
        "--tb=short",
        f"--json-report",
        f"--json-report-file={json_report_path}"
    ])

    # 读取配置中的 URL
    import yaml
    with open('C:\\Users\\15274\\PycharmProjects\\playwright_test\\config\\config.yml', 'r', encoding='utf-8') as f:
        _cfg = yaml.safe_load(f)
    _env = os.getenv("prod", "prod")
    _env_cfg = _cfg["environments"][_env]

    # 读取 JSON 报告
    test_results = {
        "total": 2,
        "passed_count": 0,
        "failed_count": 0,
        "passed": exit_code == 0,
        "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "use_token": os.path.exists(TestWeb.TOKEN_FILE),
        "constant_send_url": _env_cfg.get("constant_send_url", ""),
        "variable_send_url": _env_cfg.get("variable_send_url", ""),
        "cases": {}
    }

    if os.path.exists(json_report_path):
        with open(json_report_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)
            for test in report_data.get("tests", []):
                test_name = test.get("nodeid", "")
                status = test.get("outcome", "failed")  # JSON 报告中使用 outcome 字段
                test_results["cases"][test_name] = {"passed": status == "passed"}
                if status == "passed":
                    test_results["passed_count"] += 1
                else:
                    test_results["failed_count"] += 1

    generate_html_report(test_results)

    sys.exit(exit_code)
