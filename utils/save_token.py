"""
获取并保存登录后的 token 到本地文件
运行此脚本会打开浏览器，由用户手动输入登录信息
"""

import json
from playwright.sync_api import sync_playwright


def save_token():
    """登录并保存 token 到文件"""

    login_url = "https://www.chuanglan.com/control/login"
    # login_url = "https://cloudsit.cm253.com/control/login"
    token_file = "C:\\Users\\15274\\PycharmProjects\\playwright_test\\utils\\token.json"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 访问登录页面
        print(f"访问登录页面：{login_url}")
        page.goto(login_url)
        page.wait_for_timeout(2000)

        print("\n请在浏览器中手动输入账号密码并登录...")
        print("登录成功后等待 30 秒，脚本会自动保存 token 并关闭浏览器\n")

        # 等待用户手动完成登录
        page.wait_for_timeout(30000)

        # 获取 cookies
        cookies = context.cookies()
        print(f"获取到 {len(cookies)} 个 cookies")

        # 保存 token 信息
        token_data = {
            "cookies": cookies,
            "login_url": login_url
        }

        with open(token_file, "w", encoding="utf-8") as f:
            json.dump(token_data, f, ensure_ascii=False, indent=2)

        print(f"\n[OK] Token 已保存到 {token_file}")

        browser.close()

    return token_file


if __name__ == "__main__":
    save_token()