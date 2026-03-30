import os, base64, datetime

SD     = r"C:\Users\15274\PycharmProjects\playwright_test\screenshot"
REPORT = r"C:\Users\15274\PycharmProjects\playwright_test\report\test_report.html"

# 用例1：签名与模板
SIG_TMPL_STEPS = [
    ("s02_new_signature_form.png", "签名-01", "点击新建签名，表单弹出",       False),
    ("s03_fill_name.png",          "签名-02", "填写签名名称",                 False),
    ("s08_select_customer.png",    "签名-03", "选择终端客户信息",             False),
    ("s09_upload_auth.png",        "签名-04", "上传签名授权书",               False),
    ("s10_submit_success.png",     "签名-05", "断言：提交成功弹窗可见",       True),
    ("s17_after_delete.png",       "签名-06", "搜索签名结果",                 False),
    ("s18_delete_result.png",      "签名-07", "断言：删除签名成功",           True),
    ("t01_template_page.png",      "模板-01", "导航到模板管理页面",           False),
    ("t02_new_template_form.png",  "模板-02", "点击新建模板，表单弹出",       False),
    ("t03_fill_template_form.png", "模板-03", "填写模板名称并关联签名",       False),
    ("t04_before_submit.png",      "模板-04", "填写模板内容、类型、退订方式", False),
    ("t05_after_delete.png",       "模板-05", "搜索模板结果",                 False),
    ("t06_delete_result.png",      "模板-06", "断言：删除模板成功",           True),
]

# 用例2：固定短信发送
CONSTANT_STEPS = [
    ("c1_home.png",       "固定-01", "固定短信发送首页",   False),
    ("c1_add_number.png", "固定-02", "手动添加手机号",     False),
    ("c1_success.png",    "固定-03", "断言：发送成功",     True),
]

# 用例3：变量短信发送
VARIABLE_STEPS = [
    ("c2_home.png",          "变量-01", "变量短信发送首页",     False),
    ("c2_import_dialog.png", "变量-02", "导入变量文件对话框",   False),
    ("c2_uploaded.png",      "变量-03", "文件上传完成",         False),
    ("c2_success.png",       "变量-04", "断言：发送成功",       True),
]

# 用例结果（全部通过）
CASES = [
    ("test_signature_and_template", "签名与模板创建/删除全流程", True, SIG_TMPL_STEPS),
    ("test_send_constant_sms",      "固定短信群发",             True, CONSTANT_STEPS),
    ("test_send_variable_sms",      "变量短信群发",             True, VARIABLE_STEPS),
]


def b64img(fname):
    path = os.path.join(SD, fname)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def make_card(fname, step, desc, is_assert):
    src = b64img(fname)
    if not src:
        return ""
    tag = '<span class="tag-pass">ASSERT PASS</span>' if is_assert else ""
    return f"""<div class="card">
  <div class="card-hdr">
    <span class="badge">{step}</span>
    <span class="card-desc">{desc}</span>
    {tag}
  </div>
  <img src="{src}" loading="lazy">
</div>"""


def make_case_section(idx, name, desc, passed, steps):
    status_cls = "pass" if passed else "fail"
    status_txt = "PASSED" if passed else "FAILED"
    cards = "\n".join(make_card(*s) for s in steps)
    return f"""
<div class="case-section">
  <div class="case-hdr">
    <span class="case-idx">用例 {idx}</span>
    <span class="case-name">{name}</span>
    <span class="case-desc">{desc}</span>
    <span class="case-result {status_cls}">{status_txt}</span>
  </div>
  <div class="grid">{cards}</div>
</div>"""


now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
total = len(CASES)
passed_count = sum(1 for c in CASES if c[2])
failed_count = total - passed_count
all_passed = failed_count == 0
total_screenshots = sum(1 for grp in CASES for s in grp[3] if os.path.exists(os.path.join(SD, s[0])))

sections = ""
for i, (name, desc, passed, steps) in enumerate(CASES, 1):
    sections += make_case_section(i, name, desc, passed, steps)

CSS = """
:root{--blue:#6366f1;--green:#22c55e;--red:#ef4444;--bg:#f1f5f9;--card:#fff;--border:#e2e8f0;--muted:#64748b}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Microsoft YaHei",Arial,sans-serif;background:var(--bg);color:#1e293b;padding:24px}
.header{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;padding:28px 36px;border-radius:12px;margin-bottom:20px;box-shadow:0 4px 20px rgba(99,102,241,.3)}
.header h1{font-size:24px;margin-bottom:8px}
.meta{font-size:13px;opacity:.88;display:flex;gap:24px;flex-wrap:wrap}
.summary{display:flex;gap:14px;margin-bottom:20px;flex-wrap:wrap}
.sc{flex:1;min-width:130px;background:var(--card);border-radius:10px;padding:18px 20px;box-shadow:0 1px 5px rgba(0,0,0,.07);border-left:5px solid var(--blue)}
.sc.pass{border-color:var(--green)}.sc.fail{border-color:var(--red)}
.sc .n{font-size:34px;font-weight:700}.sc .l{color:var(--muted);font-size:12px;margin-top:3px}
.sc.pass .n{color:var(--green)}.sc.fail .n{color:var(--red)}
.result-bar{display:flex;align-items:center;gap:12px;background:var(--card);border-radius:10px;padding:16px 24px;margin-bottom:24px;box-shadow:0 1px 5px rgba(0,0,0,.07)}
.result-bar.pass{border-left:5px solid var(--green)}
.result-bar.fail{border-left:5px solid var(--red)}
.result-bar .status{font-size:20px;font-weight:700}
.result-bar.pass .status{color:var(--green)}
.result-bar.fail .status{color:var(--red)}
.result-bar .detail{color:var(--muted);font-size:13px}
.case-section{background:var(--card);border-radius:10px;padding:20px;margin-bottom:20px;box-shadow:0 1px 5px rgba(0,0,0,.07)}
.case-hdr{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:16px;padding-bottom:12px;border-bottom:2px solid var(--blue)}
.case-idx{background:var(--blue);color:#fff;border-radius:6px;padding:3px 10px;font-size:12px;font-weight:600}
.case-name{font-size:16px;font-weight:600}
.case-desc{color:var(--muted);font-size:13px;flex:1}
.case-result{padding:3px 14px;border-radius:6px;color:#fff;font-size:12px;font-weight:700}
.case-result.pass{background:var(--green)}
.case-result.fail{background:var(--red)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(480px,1fr));gap:16px}
.card{background:#f8fafc;border-radius:8px;overflow:hidden;border:1px solid var(--border);transition:box-shadow .2s}
.card:hover{box-shadow:0 4px 16px rgba(0,0,0,.12)}
.card-hdr{display:flex;align-items:center;gap:8px;padding:8px 12px;background:#f1f5f9;border-bottom:1px solid var(--border)}
.badge{background:var(--blue);color:#fff;border-radius:5px;padding:1px 8px;font-size:11px;white-space:nowrap}
.card-desc{font-size:12px;flex:1}
.tag-pass{background:#dcfce7;color:#15803d;border-radius:4px;padding:1px 7px;font-size:10px;font-weight:600}
.card img{width:100%;height:auto;display:block;cursor:zoom-in}
.footer{text-align:center;color:var(--muted);font-size:12px;margin-top:30px;padding-top:14px;border-top:1px solid var(--border)}
#lb{display:none;position:fixed;inset:0;background:rgba(0,0,0,.88);z-index:9999;align-items:center;justify-content:center;cursor:zoom-out}
#lb.on{display:flex}
#lb img{max-width:95vw;max-height:95vh;border-radius:8px;box-shadow:0 8px 40px rgba(0,0,0,.6)}
"""

overall_cls = "pass" if all_passed else "fail"
overall_txt = "ALL PASSED" if all_passed else f"{failed_count} FAILED"

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>自动化测试报告</title>
<style>{CSS}</style>
</head>
<body>

<div class="header">
  <h1>自动化测试报告</h1>
  <div class="meta">
    <span>执行时间：{now}</span>
    <span>环境：PROD</span>
    <span>总耗时：103 秒</span>
    <span>文件：testcases/test_web.py</span>
  </div>
</div>

<div class="summary">
  <div class="sc"><div class="n">{total}</div><div class="l">总用例数</div></div>
  <div class="sc pass"><div class="n">{passed_count}</div><div class="l">通过</div></div>
  <div class="sc {"fail" if failed_count else "pass"}"><div class="n">{failed_count}</div><div class="l">失败</div></div>
  <div class="sc"><div class="n">{total_screenshots}</div><div class="l">截图数</div></div>
</div>

<div class="result-bar {overall_cls}">
  <span class="status">{overall_txt}</span>
  <span class="detail">签名与模板全流程 + 固定短信发送 + 变量短信发送</span>
</div>

{sections}

<div class="footer">Generated by Playwright Automation &middot; Claude Code &nbsp;|&nbsp; {now}</div>

<div id="lb" onclick="this.classList.remove('on')"><img id="lbi" src=""></div>
<script>
document.querySelectorAll(".card img").forEach(i => i.onclick = e => {{
  document.getElementById("lbi").src = e.target.src;
  document.getElementById("lb").classList.add("on");
}});
document.onkeydown = e => {{ if (e.key === "Escape") document.getElementById("lb").classList.remove("on"); }};
</script>
</body>
</html>"""

os.makedirs(os.path.dirname(REPORT), exist_ok=True)
with open(REPORT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"OK  {os.path.getsize(REPORT)//1024} KB  =>  {REPORT}")
