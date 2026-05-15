"""
run_all.py - 测试用例执行入口

功能：
- 一次运行全部用例
- 可自定义用例执行顺序
- 支持通过命令行参数选择运行哪些用例

用法：
    python run_all.py          # 运行全部用例（按默认顺序）
    python run_all.py --only 1 3  # 只运行第1、3个用例
"""

import sys
import os
import pytest

# 切换工作目录到项目根目录，确保 pytest 能正确找到用例文件
PROJECT_ROOT = r"C:\Users\15274\PycharmProjects\playwright_test"
os.chdir(PROJECT_ROOT)

# ============================================================
# 用例执行顺序配置（修改此列表即可调整顺序）
# ============================================================

TEST_ORDER = [
    "testcases/test_signature.py::test_signature",                          # 1. 签名
    "testcases/test_template.py::test_template",                            # 2. 模板
    "testcases/test_constant_sms.py::test_send_constant_sms",               # 3. 固定短信
    "testcases/test_variable_sms.py::test_send_variable_sms",               # 4. 变量短信
    "testcases/test_clean_template.py::test_clean_template",                 # 5. 清理模板
    "testcases/test_clean_signature.py::test_clean_signature",              # 6. 清理签名

]


def main():
    # 解析 --only 参数，选择运行哪些用例
    tests_to_run = TEST_ORDER

    if "--only" in sys.argv:
        idx = sys.argv.index("--only")
        indices = [int(x) for x in sys.argv[idx + 1:] if x.isdigit()]
        tests_to_run = [TEST_ORDER[i - 1] for i in indices if 1 <= i <= len(TEST_ORDER)]
        if not tests_to_run:
            print("[ERROR] 无效的用例编号，可选范围：1 ~", len(TEST_ORDER))
            sys.exit(1)

    print("=" * 60)
    print("  即将执行的用例（按顺序）：")
    print("=" * 60)
    for i, t in enumerate(tests_to_run, 1):
        name = t.split("::")[-1]
        print(f"  {i}. {name}")
    print("=" * 60)

    exit_code = pytest.main([
        *tests_to_run,
        "-v",
        "-s",
        "--tb=short",
        "-p", "no:randomly",  # 禁用随机排序插件（如果安装了的话）
    ])

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
