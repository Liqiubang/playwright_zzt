"""
conftest.py - Pytest 全局配置与 Fixture 定义

本模块负责：
- 创建 Playwright 浏览器上下文（支持 token 免登录）
- 加载环境配置（从 config.yml 读取）
- 收集测试结果并在测试会话结束后生成 HTML 报告
"""

import pytest
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import yaml


class TestWeb:
    """测试项目的全局常量定义"""

    # 项目根目录
    PROJECT_ROOT = r"C:\Users\15274\PycharmProjects\playwright_test"
    # Token 文件路径，用于免登录
    TOKEN_FILE = os.path.join(PROJECT_ROOT, "utils", "token.json")
    # 截图保存目录
    SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshot")
    # 测试报告输出目录
    REPORT_DIR = os.path.join(PROJECT_ROOT, "report")

    @staticmethod
    def load_token():
        """从文件加载 token（支持新格式：按站点分组）

        新格式结构: { "cloudsit": {...}, "smart_operation": {...} }
        旧格式结构: { "cookies": [...] }

        Returns:
            dict: 包含 cookies 列表的字典，或 None（文件不存在时）
        """
        if os.path.exists(TestWeb.TOKEN_FILE):
            with open(TestWeb.TOKEN_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 新格式：合并所有站点的 cookies
                if "cloudsit" in data or "smart_operation" in data:
                    all_cookies = []
                    for site_key in ("cloudsit", "smart_operation"):
                        if site_key in data:
                            all_cookies.extend(data[site_key].get("cookies", []))
                    return {"cookies": all_cookies}
                # 兼容旧格式：直接返回
                return data
        return None


@pytest.fixture(scope="session")
def browser_context():
    """创建浏览器上下文（session 级别，整个测试会话共用）

    - 以有头模式启动 Chromium 浏览器（方便观察执行过程）
    - 若本地存在 token 文件，则自动注入 cookies 实现免登录
    - 每个操作间隔 1000ms，便于调试观察

    Yields:
        Page: Playwright 页面对象
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=1000,
            args=['--start-maximized']
        )

        # 尝试加载保存的 token
        token_data = TestWeb.load_token()

        if token_data:
            # 使用保存的 token 创建上下文
            context = browser.new_context(no_viewport=True)
            context.add_cookies(token_data.get("cookies", []))
            page = context.new_page()
            print("\n[OK] 使用保存的 token 免登录")
        else:
            # 正常创建上下文（需要登录）
            context = browser.new_context(no_viewport=True)
            page = context.new_page()
            print("\n[OK] 未检测到 token，需要登录")

        yield page
        browser.close()


def load_config():
    """加载 YAML 配置文件

    Returns:
        dict: 配置文件内容
    """
    config_path = r"C:\Users\15274\PycharmProjects\playwright_test\config\config.yml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def env_config():
    """获取当前环境配置（session 级别）

    根据环境变量选择对应的配置段，默认使用 prod 环境。

    Returns:
        dict: 当前环境的配置字典
    """
    env = os.getenv("prod", "prod")
    config = load_config()
    return config["environments"][env]


# ==================== 测试结果收集 ====================

# 测试会话开始时间
_test_start_time = None
# 各用例测试结果，key 为 nodeid
_test_reports = {}


def pytest_sessionstart(session):
    """Pytest 钩子：测试会话开始时记录时间"""
    global _test_start_time
    _test_start_time = datetime.now()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest 钩子：捕获每个测试用例的执行结果

    仅在 call 阶段（实际测试执行）记录结果，
    忽略 setup 和 teardown 阶段。
    """
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
    """Pytest 钩子：测试会话结束后生成 HTML 报告

    汇总所有用例的执行结果，调用 test_web 模块中的
    generate_html_report() 生成可视化报告。
    """
    from testcases.test_web import generate_html_report

    config = load_config()
    env = os.getenv("prod", "prod")
    env_cfg = config["environments"][env]

    # 统计通过/失败数量
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
        "timestamp": (
            _test_start_time.strftime("%Y-%m-%d %H:%M:%S")
            if _test_start_time
            else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
        "use_token": os.path.exists(TestWeb.TOKEN_FILE),
        "constant_send_url": env_cfg.get("constant_send_url", ""),
        "variable_send_url": env_cfg.get("variable_send_url", ""),
        "cases": cases
    }

    generate_html_report(test_results)
