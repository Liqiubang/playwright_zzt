使用步骤
1.在以下文件中修改环境、URL
conftest.py
save_token.py

2.运行save_token.py保存token

3.运行run_all.py

    # 运行全部用例
    pytest testcases/

    # 运行单个文件
    pytest testcases/test_constant_sms.py

    # 运行指定用例
    pytest testcases/test_signature_template.py::test_signature_and_template
