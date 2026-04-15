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

    # 步骤3：点击签名名称输入框并填写签名名称（来自配置）
    page.get_by_role("textbox", name="* 签名名称").click()
    page.get_by_role("textbox", name="* 签名名称").fill(f"{env_config['signature']}")
    # 截图：签名名称已填写
    page.screenshot(path=os.path.join(sd, "fill_name.png"))

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

    # 步骤8：点击"终端客户信息"下拉框
    page.get_by_role("combobox", name="* 终端客户信息").click()
    page.get_by_text(f"{env_config['company']}").click()
    # 截图：终端客户已选择
    page.screenshot(path=os.path.join(sd, "select_customer.png"))

    # 步骤8.5：上传签名授权书（"他用"模式必填证明材料）
    auth_file = os.path.join(TestWeb.PROJECT_ROOT, "签名授权书.png")
    with page.expect_file_chooser() as fc_info:
        page.locator(".sms-upload").nth(2).click()
    file_chooser = fc_info.value
    file_chooser.set_files(auth_file)
    page.wait_for_timeout(8000)
    # 截图：上传签名授权书
    page.screenshot(path=os.path.join(sd, "upload_auth.png"))

    # 步骤9：点击"提交审核"按钮，等待后端响应后截图
    page.get_by_role("button", name="提交审核").click()

    # 步骤10：断言成功弹窗出现（弹窗文本包含该关键词即可），点击"我知道了"关闭弹窗
    expect(page.get_by_text("您的签名已提交审核", exact=False)).to_be_visible(timeout=10000)
    # 截图：提交成功弹窗可见
    page.screenshot(path=os.path.join(sd, "submit_success.png"))
    page.get_by_role("button", name="我知道了").click()

    # 步骤15：在搜索框中输入签名名称并点击"搜 索"，等待结果加载后截图
    page.get_by_role("textbox", name="请输入搜索关键词").click()
    page.get_by_role("textbox", name="请输入搜索关键词").fill(f"{env_config['signature']}")
    # 点击搜索按钮，触发列表刷新
    page.get_by_role("button", name="搜 索").click()
    # 等待搜索结果中出现签名名称文本，确认数据已加载
    expect(page.get_by_text(env_config['signature'])).to_be_visible(timeout=10000)

    # 步骤16：点击列表中第一个"删除"链接，弹出确认对话框后确认删除
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(sd, "sig_after_search.png"))
    page.get_by_text("删除").first.click()
    page.get_by_role("button", name="确 定").click()

    # 断言：验证删除签名成功提示可见（toast消失很快，必须立即断言）
    expect(page.get_by_text("删除签名成功")).to_be_visible()
    # 截图：删除成功 toast 提示
    page.screenshot(path=os.path.join(sd, "sig_delete_result.png"))

    # ===== 模板部分 =====

    # 步骤17：导航到模板管理页面
    page.goto(f"{env_config['create_template_url']}")

    # 步骤18：点击"新建模板"按钮，打开新建表单
    page.get_by_role("button", name="新建模板").click()

    # 步骤19：填写模板名称
    page.get_by_role("textbox", name="* 模板名称").click()
    page.get_by_role("textbox", name="* 模板名称").fill("测试模板")
    # 截图：模板名称截图
    page.screenshot(path=os.path.join(sd, "new_template_form.png"))

    # 步骤20：点击关联签名下拉框（通过 id 定位，force=True 绕过 sms-select-selection-item 遮挡）
    page.locator("input#signature").click(force=True)
    # 等待下拉选项渲染完成后选择"创蓝云智"
    page.wait_for_selector(".sms-select-item-option-content", timeout=5000)
    page.locator(".sms-select-item-option-content").filter(has_text="创蓝云智").click()

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

    # 步骤25：点击"提交审核"按钮，等待后端响应后截图
    page.get_by_role("button", name="提交审核").click()
    # 截图：提交成功弹窗可见
    page.screenshot(path=os.path.join(sd, "submit_template_success.png"))
    # 步骤26：点击"我知道了"关闭提交成功弹窗
    page.get_by_role("button", name="我知道了").click()

    # 步骤27：删除模板
    page.get_by_text("标题").click()
    page.get_by_text("内容", exact=True).click()
    page.get_by_role("textbox", name="请输入搜索关键词").click()
    page.get_by_role("textbox", name="请输入搜索关键词").fill(f"{env_config['template']}")
    page.get_by_role("button", name="搜 索").click()

    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(sd, "tmpl_after_search.png"))
    page.get_by_text("删除").first.click()
    page.get_by_role("button", name="确 定").click()

    # 断言：验证删除模板成功提示可见
    expect(page.get_by_text("删除模板成功")).to_be_visible()
    # 截图：删除成功 toast 提示
    page.screenshot(path=os.path.join(sd, "tmpl_delete_result.png"))


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
    sd = TestWeb.SCREENSHOT_DIR

    # 收集 screenshot 目录下所有实际存在的截图
    all_screenshots = {}
    if os.path.isdir(sd):
        for fname in sorted(os.listdir(sd)):
            fpath = os.path.join(sd, fname)
            if fname.lower().endswith(('.png', '.jpg', '.jpeg')) and os.path.isfile(fpath):
                with open(fpath, "rb") as f:
                    ext = fname.rsplit('.', 1)[-1].lower()
                    mime = 'image/png' if ext == 'png' else 'image/jpeg'
                    all_screenshots[fname] = f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

    # 签名+模板用例截图（按测试代码中的实际文件名）
    sig_tmpl_files = [
        ("fill_name.png", "步骤1 填写签名名称"),
        ("select_customer.png", "步骤2 选择终端客户"),
        ("upload_auth.png", "步骤3 上传签名授权书"),
        ("submit_success.png", "步骤4 签名提交成功"),
        ("sig_after_search.png", "步骤5 搜索签名结果"),
        ("sig_delete_result.png", "步骤6 删除签名成功"),
        ("new_template_form.png", "步骤7 新建模板表单"),
        ("submit_template_success.png", "步骤8 模板提交成功"),
        ("tmpl_after_search.png", "步骤9 搜索模板结果"),
        ("tmpl_delete_result.png", "步骤10 删除模板成功"),
    ]

    # 固定短信截图
    screenshot_files_constant = [
        ("c1_home.png", "首页"),
        ("c1_add_number.png", "添加手机号"),
        ("c1_success.png", "发送成功"),
    ]

    # 变量短信截图
    screenshot_files_variable = [
        ("c2_home.png", "首页"),
        ("c2_import_dialog.png", "导入文件对话框"),
        ("c2_uploaded.png", "文件上传完成"),
        ("c2_success.png", "发送成功"),
    ]

    overall_cls = 'success' if test_results['passed'] else 'fail'
    overall_txt = 'PASSED' if test_results['passed'] else 'FAILED'
    token_txt = '已使用保存的 token 免登录' if test_results['use_token'] else '未检测到 token'

    # 构建用例数据
    case_configs = []
    sig_case = {
        "title": "签名与模板创建",
        "nodeid": "testcases/test_web.py::test_signature_and_template",
        "desc": "新建签名 -> 提交审核 -> 搜索签名 -> 删除签名；新建模板 -> 提交审核 -> 搜索模板 -> 删除模板",
        "files": sig_tmpl_files,
    }
    const_case = {
        "title": "固定短信发送",
        "nodeid": "testcases/test_web.py::test_send_constant_sms",
        "desc": "手动添加手机号，发送固定内容的短信",
        "files": screenshot_files_constant,
    }
    var_case = {
        "title": "变量短信发送",
        "nodeid": "testcases/test_web.py::test_send_variable_sms",
        "desc": "导入文件，发送变量内容的短信",
        "files": screenshot_files_variable,
    }

    # 只显示本次运行过的用例
    for c in [sig_case, const_case, var_case]:
        if c["nodeid"] in test_results["cases"]:
            case_configs.append(c)

    # 生成用例 HTML
    cases_html = ""
    for idx, c in enumerate(case_configs, 1):
        r = test_results['cases'].get(c['nodeid'], {})
        p = r.get('passed', False)
        badge_cls = 'badge-pass' if p else 'badge-fail'
        badge_txt = 'PASSED' if p else 'FAILED'
        result_cls = 'result-pass' if p else 'result-fail'
        result_txt = '通过' if p else '失败'

        # 截图卡片
        imgs_html = ""
        for fname, title in c["files"]:
            if fname in all_screenshots:
                imgs_html += f'''
                    <div class="screenshot-card">
                        <div class="card-title">{title}</div>
                        <img src="{all_screenshots[fname]}" alt="{fname}" onclick="openModal(this.src)">
                        <div class="card-filename">{fname}</div>
                    </div>'''

        cases_html += f'''
        <div class="case-section">
            <div class="case-header">
                <span class="case-name">用例 {idx}：{c['title']}</span>
                <span class="badge {badge_cls}">{badge_txt}</span>
            </div>
            <table class="detail-table">
                <tr><th>测试场景</th><td>{c['desc']}</td></tr>
                <tr><th>测试结果</th><td class="{result_cls}">{result_txt}</td></tr>
            </table>
            <div class="screenshots-title">测试步骤截图</div>
            <div class="screenshots-grid">{imgs_html if imgs_html else '<p style="color:#999;padding:12px;">暂无截图</p>'}</div>
        </div>'''

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自动化测试报告</title>
    <style>
        :root {{
            --primary: #4f46e5;
            --primary-light: #818cf8;
            --success: #10b981;
            --danger: #ef4444;
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-300: #d1d5db;
            --gray-500: #6b7280;
            --gray-700: #374151;
            --gray-900: #111827;
            --radius: 12px;
            --shadow: 0 1px 3px rgba(0,0,0,.1), 0 1px 2px rgba(0,0,0,.06);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,.1), 0 4px 6px -2px rgba(0,0,0,.05);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif; background: var(--gray-100); color: var(--gray-900); line-height: 1.6; }}
        .page {{ max-width: 1400px; margin: 0 auto; padding: 24px; }}

        /* Header */
        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, #7c3aed 50%, #a855f7 100%);
            color: #fff; padding: 40px 36px; border-radius: var(--radius) var(--radius) 0 0;
            position: relative; overflow: hidden;
        }}
        .header::after {{
            content: ''; position: absolute; top: -50%; right: -10%; width: 400px; height: 400px;
            background: rgba(255,255,255,.06); border-radius: 50%;
        }}
        .header h1 {{ font-size: 32px; font-weight: 700; margin-bottom: 6px; position: relative; z-index: 1; }}
        .header .subtitle {{ opacity: .85; font-size: 15px; position: relative; z-index: 1; }}

        /* Stats Bar */
        .stats-bar {{
            display: flex; gap: 16px; padding: 24px 36px;
            background: #fff; border-bottom: 1px solid var(--gray-200);
        }}
        .stat-card {{
            flex: 1; padding: 20px; border-radius: 10px; text-align: center;
            background: var(--gray-50); border: 1px solid var(--gray-200); transition: transform .15s;
        }}
        .stat-card:hover {{ transform: translateY(-2px); box-shadow: var(--shadow); }}
        .stat-card .num {{ font-size: 40px; font-weight: 800; line-height: 1.1; }}
        .stat-card .lbl {{ font-size: 13px; color: var(--gray-500); margin-top: 4px; text-transform: uppercase; letter-spacing: .5px; }}
        .stat-card.total .num {{ color: var(--primary); }}
        .stat-card.pass .num {{ color: var(--success); }}
        .stat-card.fail .num {{ color: var(--danger); }}

        /* Summary */
        .summary {{
            padding: 24px 36px; background: #fff; border-bottom: 1px solid var(--gray-200);
        }}
        .summary h2 {{
            font-size: 18px; color: var(--gray-700); margin-bottom: 16px;
            padding-bottom: 10px; border-bottom: 3px solid var(--primary); display: inline-block;
        }}
        .summary-table {{ width: 100%; border-collapse: collapse; }}
        .summary-table th {{ text-align: left; padding: 12px 16px; background: var(--gray-50); color: var(--gray-500); font-weight: 600; width: 140px; font-size: 13px; text-transform: uppercase; letter-spacing: .3px; }}
        .summary-table td {{ padding: 12px 16px; color: var(--gray-700); font-size: 15px; }}
        .summary-table tr {{ border-bottom: 1px solid var(--gray-100); }}
        .result-pass {{ color: var(--success); font-weight: 700; }}
        .result-fail {{ color: var(--danger); font-weight: 700; }}

        /* Case Sections */
        .case-section {{
            padding: 24px 36px; background: var(--gray-50);
            border-bottom: 1px solid var(--gray-200);
        }}
        .case-header {{
            display: flex; align-items: center; gap: 12px; margin-bottom: 16px;
        }}
        .case-name {{ font-size: 20px; font-weight: 700; color: var(--gray-900); }}
        .badge {{
            padding: 4px 14px; border-radius: 20px; font-size: 12px;
            font-weight: 700; letter-spacing: .5px; text-transform: uppercase;
        }}
        .badge-pass {{ background: #d1fae5; color: #065f46; }}
        .badge-fail {{ background: #fee2e2; color: #991b1b; }}
        .detail-table {{ width: 100%; border-collapse: collapse; margin-bottom: 16px; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: var(--shadow); }}
        .detail-table th {{ text-align: left; padding: 10px 16px; background: var(--gray-50); color: var(--gray-500); font-weight: 600; width: 120px; font-size: 13px; }}
        .detail-table td {{ padding: 10px 16px; color: var(--gray-700); }}
        .detail-table tr {{ border-bottom: 1px solid var(--gray-100); }}
        .detail-table tr:last-child {{ border-bottom: none; }}
        .screenshots-title {{ font-size: 15px; font-weight: 600; color: var(--gray-700); margin-bottom: 12px; }}

        /* Screenshots Grid */
        .screenshots-grid {{
            display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 16px;
        }}
        .screenshot-card {{
            background: #fff; border-radius: 10px; overflow: hidden;
            box-shadow: var(--shadow); transition: transform .15s, box-shadow .15s;
        }}
        .screenshot-card:hover {{ transform: translateY(-3px); box-shadow: var(--shadow-lg); }}
        .card-title {{
            padding: 10px 16px; font-size: 13px; font-weight: 600;
            color: var(--gray-700); background: var(--gray-50); border-bottom: 1px solid var(--gray-200);
        }}
        .screenshot-card img {{ width: 100%; height: auto; display: block; cursor: pointer; }}
        .card-filename {{
            padding: 6px 16px; font-size: 12px; color: var(--gray-500);
            background: var(--gray-50); border-top: 1px solid var(--gray-200);
            font-family: 'Consolas', 'Monaco', monospace; text-align: center;
        }}

        /* Modal */
        .modal-overlay {{
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,.85); z-index: 1000; justify-content: center; align-items: center; cursor: zoom-out;
        }}
        .modal-overlay.active {{ display: flex; }}
        .modal-overlay img {{ max-width: 92vw; max-height: 92vh; border-radius: 8px; box-shadow: 0 0 40px rgba(0,0,0,.5); }}

        /* Footer */
        .footer {{
            padding: 20px 36px; text-align: center; color: var(--gray-500);
            font-size: 13px; background: #fff; border-top: 1px solid var(--gray-200);
            border-radius: 0 0 var(--radius) var(--radius);
        }}
    </style>
</head>
<body>
    <div class="page">
        <div class="header">
            <h1>自动化测试报告</h1>
            <div class="subtitle">Playwright E2E Automation Test Report &middot; {test_results['timestamp']}</div>
        </div>
        <div class="stats-bar">
            <div class="stat-card total"><div class="num">{test_results['total']}</div><div class="lbl">Total</div></div>
            <div class="stat-card pass"><div class="num">{test_results['passed_count']}</div><div class="lbl">Passed</div></div>
            <div class="stat-card fail"><div class="num">{test_results['failed_count']}</div><div class="lbl">Failed</div></div>
        </div>
        <div class="summary">
            <h2>测试概要</h2>
            <table class="summary-table">
                <tr><th>测试时间</th><td>{test_results['timestamp']}</td></tr>
                <tr><th>整体结果</th><td class="{'result-pass' if test_results['passed'] else 'result-fail'}">{overall_txt}</td></tr>
                <tr><th>免登录状态</th><td>{token_txt}</td></tr>
            </table>
        </div>
        {cases_html}
        <div class="footer">
            Generated by Playwright Automation Test &middot; {test_results['timestamp']}
        </div>
    </div>

    <!-- 图片放大弹窗 -->
    <div class="modal-overlay" id="imgModal" onclick="closeModal()">
        <img id="modalImg" src="" alt="preview">
    </div>
    <script>
        function openModal(src) {{
            document.getElementById('modalImg').src = src;
            document.getElementById('imgModal').classList.add('active');
        }}
        function closeModal() {{
            document.getElementById('imgModal').classList.remove('active');
        }}
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') closeModal();
        }});
    </script>
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
