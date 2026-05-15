"""
report_helper.py - HTML 测试报告生成模块

本模块包含报告生成的所有逻辑，供 conftest.py 调用。
"""

import os
import base64

# 项目根目录与路径常量
PROJECT_ROOT = r"C:\Users\15274\PycharmProjects\playwright_test"
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshot")
REPORT_DIR = os.path.join(PROJECT_ROOT, "report")


def generate_html_report(test_results):
    """生成 HTML 格式的测试报告

    Args:
        test_results: 包含以下字段的字典：
            - total: 总用例数
            - passed_count: 通过数
            - failed_count: 失败数
            - passed: 是否全部通过
            - timestamp: 测试时间
            - use_token: 是否使用 token 免登录
            - cases: 各用例结果
    """
    os.makedirs(REPORT_DIR, exist_ok=True)

    # 收集 screenshot 目录下所有实际存在的截图，转为 base64
    all_screenshots = {}
    if os.path.isdir(SCREENSHOT_DIR):
        for fname in sorted(os.listdir(SCREENSHOT_DIR)):
            fpath = os.path.join(SCREENSHOT_DIR, fname)
            if fname.lower().endswith(('.png', '.jpg', '.jpeg')) and os.path.isfile(fpath):
                with open(fpath, "rb") as f:
                    ext = fname.rsplit('.', 1)[-1].lower()
                    mime = 'image/png' if ext == 'png' else 'image/jpeg'
                    all_screenshots[fname] = f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

    # ---- 各用例对应的截图文件列表 ----

    screenshot_signature = [
        ("fill_name.png", "填写签名名称"),
        ("select_customer.png", "选择终端客户"),
        ("upload_auth.png", "上传签名授权书"),
        ("submit_success.png", "签名提交成功"),
    ]

    screenshot_template = [
        ("new_template_form.png", "新建常量模板表单"),
        ("submit_template_success.png", "常量模板提交成功"),
        ("new_var_template_form.png", "新建变量模板表单"),
        ("submit_var_template_success.png", "变量模板提交成功"),
    ]

    screenshot_constant_sms = [
        ("c1_home.png", "首页"),
        ("c1_add_number.png", "添加手机号"),
        ("c1_success.png", "发送成功"),
    ]

    screenshot_variable_sms = [
        ("c2_home.png", "首页"),
        ("c2_import_dialog.png", "导入文件对话框"),
        ("c2_uploaded.png", "文件上传完成"),
        ("c2_success.png", "发送成功"),
    ]

    screenshot_clean_template = [
        ("tmpl_delete_result.png", "删除模板成功"),
    ]

    screenshot_clean_signature = [
        ("tmpl_delete_subport.png", "子端口列表"),
    ]

    # ---- 报告概要信息 ----

    overall_txt = 'PASSED' if test_results['passed'] else 'FAILED'
    token_txt = '已使用保存的 token 免登录' if test_results['use_token'] else '未检测到 token'

    # ---- 构建用例配置 ----

    all_cases = [
        {
            "title": "创建签名",
            "nodeid": "testcases/test_signature.py::test_signature",
            "desc": "新建签名 -> 填写信息 -> 上传授权书 -> 提交审核",
            "files": screenshot_signature,
        },
        {
            "title": "创建模板",
            "nodeid": "testcases/test_template.py::test_template",
            "desc": "新建常量模板 -> 审核通过 -> 新建变量模板 -> 审核通过",
            "files": screenshot_template,
        },
        {
            "title": "固定短信发送",
            "nodeid": "testcases/test_constant_sms.py::test_send_constant_sms",
            "desc": "手动添加手机号，发送固定内容的短信",
            "files": screenshot_constant_sms,
        },
        {
            "title": "变量短信发送",
            "nodeid": "testcases/test_variable_sms.py::test_send_variable_sms",
            "desc": "导入变量文件，发送变量内容的短信",
            "files": screenshot_variable_sms,
        },
        {
            "title": "清理模板",
            "nodeid": "testcases/test_clean_template.py::test_clean_template",
            "desc": "搜索并批量删除测试模板",
            "files": screenshot_clean_template,
        },
        {
            "title": "清理签名",
            "nodeid": "testcases/test_clean_signature.py::test_clean_signature",
            "desc": "智能运营删除签名及子端口",
            "files": screenshot_clean_signature,
        },
    ]

    # 只显示本次运行过的用例
    case_configs = []
    for c in all_cases:
        if c["nodeid"] in test_results["cases"]:
            case_configs.append(c)

    # ---- 生成用例 HTML 片段 ----

    cases_html = ""
    for idx, c in enumerate(case_configs, 1):
        r = test_results['cases'].get(c['nodeid'], {})
        p = r.get('passed', False)
        badge_cls = 'badge-pass' if p else 'badge-fail'
        badge_txt = 'PASSED' if p else 'FAILED'
        result_cls = 'result-pass' if p else 'result-fail'
        result_txt = '通过' if p else '失败'

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

    # ---- 组装完整 HTML ----

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

    report_path = os.path.join(REPORT_DIR, "test_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n[OK] HTML 测试报告已生成：{report_path}")
    return report_path
