import pytest
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import yaml


class TestWeb():
    PROJECT_ROOT = r"C:\Users\15274\PycharmProjects\playwright_test"
    TOKEN_FILE = os.path.join(PROJECT_ROOT, "utils", "token.json")
    SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshot")
    REPORT_DIR = os.path.join(PROJECT_ROOT, "report")

    @staticmethod
    def load_token():
        """从文件加载 token"""
        if os.path.exists(TestWeb.TOKEN_FILE):
            with open(TestWeb.TOKEN_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return None


@pytest.fixture(scope="session")
def browser_context():
    """创建浏览器上下文，支持免登录"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # 关闭无头模式，显示浏览器
            slow_mo=1000,  # 每个操作延迟 500ms，方便观察
            args=['--start-maximized']  # 启动时最大化窗口
        )

        # 尝试加载保存的 token
        token_data = TestWeb.load_token()

        if token_data:
            # 使用保存的 token 创建上下文
            context = browser.new_context(no_viewport=True)  # 禁用固定视口，使用实际窗口大小
            context.add_cookies(token_data.get("cookies", []))
            page = context.new_page()
            print("\n[OK] 使用保存的 token 免登录")
        else:
            # 正常创建上下文（需要登录）
            context = browser.new_context(no_viewport=True)  # 禁用固定视口，使用实际窗口大小
            page = context.new_page()
            print("\n[OK] 未检测到 token，需要登录")

        yield page
        browser.close()

def load_config():
    with open('C:\\Users\\15274\\PycharmProjects\\playwright_test\\config\\config.yml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def env_config():
    #env = os.getenv("sit", "sit")
    env = os.getenv("prod", "prod")
    config = load_config()
    return config["environments"][env]


# 记录测试开始时间和结果
_test_start_time = None
_test_reports = {}


def pytest_sessionstart(session):
    """测试会话开始时记录时间"""
    global _test_start_time
    _test_start_time = datetime.now()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """捕获每个测试的结果"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        nodeid = item.nodeid
        _test_reports[nodeid] = {
            "passed": report.passed,
            "failed": report.failed,
            "outcome": report.outcome
        }


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束后生成 HTML 报告"""
    from testcases.test_web import generate_html_report

    config = load_config()
    env = os.getenv("prod", "prod")
    env_cfg = config["environments"][env]

    # 统计测试结果
    passed_count = sum(1 for r in _test_reports.values() if r["passed"])
    failed_count = sum(1 for r in _test_reports.values() if r["failed"])

    # 构建测试结果数据
    cases = {}
    for nodeid, report_data in _test_reports.items():
        cases[nodeid] = {"passed": report_data["passed"]}

    test_results = {
        "total": len(_test_reports),
        "passed_count": passed_count,
        "failed_count": failed_count,
        "passed": exitstatus == 0,
        "timestamp": _test_start_time.strftime("%Y-%m-%d %H:%M:%S") if _test_start_time else datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "use_token": os.path.exists(TestWeb.TOKEN_FILE),
        "constant_send_url": env_cfg.get("constant_send_url", ""),
        "variable_send_url": env_cfg.get("variable_send_url", ""),
        "cases": cases
    }

    generate_html_report(test_results)
