import pytest
import json
import os
from playwright.sync_api import sync_playwright
import yaml


class TestWeb():
    TOKEN_FILE = "utils/token.json"
    SCREENSHOT_DIR = "screenshot"
    REPORT_DIR = "report"

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
            slow_mo=1000  # 每个操作延迟 500ms，方便观察
        )

        # 尝试加载保存的 token
        token_data = TestWeb.load_token()

        if token_data:
            # 使用保存的 token 创建上下文
            context = browser.new_context()
            context.add_cookies(token_data.get("cookies", []))
            page = context.new_page()
            print("\n[OK] 使用保存的 token 免登录")
        else:
            # 正常创建上下文（需要登录）
            context = browser.new_context()
            page = context.new_page()
            print("\n[OK] 未检测到 token，需要登录")

        page.set_viewport_size({"width": 1920, "height": 1080})
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