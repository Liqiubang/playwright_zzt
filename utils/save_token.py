"""
获取并保存登录后的 token 到本地文件
支持两个网站的 token 保存到同一个文件，实现增量更新
"""

import json
import os
from playwright.sync_api import sync_playwright

TOKEN_FILE = r"C:\Users\15274\PycharmProjects\playwright_test\utils\token.json"

SITES = {
    "1": {
        "key": "cloudsit",
        "name": "创蓝云智客户平台",
        "login_url": "https://cloudsit.cm253.com/control/login"
        # "login_url": "https://www.chuanglan.com/control/login"
    },
    "2": {
        "key": "smart_operation",
        "name": "智能运营后台",
        "login_url": "http://smart-operation-sit.cm253.com/login"
        # "login_url": "https://smart-operation.new253.com/login"
    }
}


def load_existing_tokens():
    """加载已有的 token 文件"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 兼容旧格式（直接是 cookies 列表的格式）
            if "cookies" in data and "cloudsit" not in data:
                return {}
            return data
    return {}


def save_site_token(site_key, site_name, login_url):
    """登录指定网站并保存 token"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        print(f"\n访问 [{site_name}] 登录页面：{login_url}")
        page.goto(login_url)
        page.wait_for_timeout(2000)

        print("请在浏览器中手动输入账号密码并登录...")
        print("您有20秒的输入时间，脚本会自动保存 token 并关闭浏览器")

        page.wait_for_timeout(20000)

        cookies = context.cookies()
        print(f"获取到 {len(cookies)} 个 cookies")

        browser.close()

    return {
        "cookies": cookies,
        "login_url": login_url
    }


def save_token():
    """交互式选择并保存 token"""
    print("=" * 50)
    print("请选择要保存 token 的网站：")
    print("  1 - 创蓝云智客户平台")
    print("  2 - 智能运营后台")
    print("  3 - 两个都保存")
    print("=" * 50)

    choice = input("请输入选项 (1/2/3): ").strip()

    if choice not in ("1", "2", "3"):
        print("无效选项，退出")
        return

    # 加载已有 token（增量更新）
    token_data = load_existing_tokens()

    if choice == "3":
        sites_to_save = ["1", "2"]
    else:
        sites_to_save = [choice]

    for site_num in sites_to_save:
        site = SITES[site_num]
        site_token = save_site_token(site["key"], site["name"], site["login_url"])
        token_data[site["key"]] = site_token
        print(f"[OK] [{site['name']}] token 已获取")

    # 保存到文件
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Token 已保存到 {TOKEN_FILE}")
    for key in token_data:
        cookie_count = len(token_data[key].get("cookies", []))
        print(f"  - {key}: {cookie_count} 个 cookies")


if __name__ == "__main__":
    save_token()
