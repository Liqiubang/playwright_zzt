"""
save_token.py - 登录 Token 获取与保存工具

本模块用于通过浏览器手动登录后，自动获取并保存 cookies 到本地文件。
支持两个网站（创蓝云智客户平台、智能运营后台）的 token 保存，
采用增量更新机制，不会覆盖已有的其他站点 token。

使用方式：直接运行本脚本，按提示选择要保存 token 的网站。
"""

import json
import os
from playwright.sync_api import sync_playwright

# Token 持久化文件路径
TOKEN_FILE = r"C:\Users\15274\PycharmProjects\playwright_test\utils\token.json"

# 支持的站点配置
SITES = {
    "1": {
        "key": "cloudsit",
        "name": "创蓝云智客户平台",
        "login_url": "https://www.chuanglan.com/control/login"
    },
    "2": {
        "key": "smart_operation",
        "name": "智能运营后台",
        "login_url": "https://smart-operation.new253.com/login"
    }
}


def load_existing_tokens():
    """加载已有的 token 文件（支持增量更新）

    Returns:
        dict: 已保存的 token 数据。若文件不存在或为旧格式则返回空字典。
    """
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 兼容旧格式（直接是 cookies 列表的格式），视为无效数据
            if "cookies" in data and "cloudsit" not in data:
                return {}
            return data
    return {}


def save_site_token(site_key, site_name, login_url):
    """登录指定网站并获取 token

    启动浏览器并打开登录页面，等待用户手动登录后自动获取 cookies。

    Args:
        site_key: 站点标识（如 'cloudsit'）
        site_name: 站点显示名称
        login_url: 登录页面 URL

    Returns:
        dict: 包含 cookies 列表和登录 URL 的字典
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # 访问登录页面
        print(f"\n访问 [{site_name}] 登录页面：{login_url}")
        page.goto(login_url)
        page.wait_for_timeout(2000)

        # 等待用户手动登录（20 秒超时）
        print("请在浏览器中手动输入账号密码并登录...")
        print("您有20秒的输入时间，脚本会自动保存 token 并关闭浏览器")
        page.wait_for_timeout(20000)

        # 获取登录后的 cookies
        cookies = context.cookies()
        print(f"获取到 {len(cookies)} 个 cookies")

        browser.close()

    return {
        "cookies": cookies,
        "login_url": login_url
    }


def save_token():
    """交互式选择并保存 token（主入口函数）

    提供命令行菜单，支持单独保存某个站点或同时保存所有站点的 token。
    采用增量更新机制，保留已有的其他站点 token。
    """
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

    # 逐个站点获取并保存 token
    for site_num in sites_to_save:
        site = SITES[site_num]
        site_token = save_site_token(site["key"], site["name"], site["login_url"])
        token_data[site["key"]] = site_token
        print(f"[OK] [{site['name']}] token 已获取")

    # 持久化到文件
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, ensure_ascii=False, indent=2)

    # 打印保存结果摘要
    print(f"\n[OK] Token 已保存到 {TOKEN_FILE}")
    for key in token_data:
        cookie_count = len(token_data[key].get("cookies", []))
        print(f"  - {key}: {cookie_count} 个 cookies")


if __name__ == "__main__":
    save_token()
