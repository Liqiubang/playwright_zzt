"""
database_ck.py - ClickHouse 数据库查询工具

本模块提供 ClickHouse 数据库的查询功能，
用于验证短信发送后的落库数据是否正确。
"""

from sqlalchemy import create_engine, text
from datetime import datetime


def query_from_ck(date_param=None):
    """从 ClickHouse 查询短信发送记录

    查询 mt_msg_merge 表中指定账号、指定日期的最新消息记录，
    并打印短信内容和状态信息。

    Args:
        date_param: 查询日期，格式为 'YYYY-MM-DD'。
                    默认为 None，此时使用当天日期。

    Returns:
        list: 查询结果的所有行数据
    """
    # 默认使用当天日期
    query_date = date_param if date_param else datetime.now().strftime('%Y-%m-%d')

    # 创建 ClickHouse 数据库连接
    engine = create_engine('clickhouse://root:123456@192.168.2.42:8123/mt_sms_sit')

    with engine.connect() as conn:
        # 查询指定账号在指定日期的消息记录，按创建时间倒序排列
        sql = text(
            "SELECT * FROM mt_msg_merge final "
            "WHERE account=:account AND ptt_day=:day "
            "ORDER BY createTime DESC"
        )
        result = conn.execute(sql, {'account': 'M5865357', 'day': query_date})
        data = result.fetchall()

        # 打印最新一条记录的关键信息
        print(f"数据库返回的最新数据：{data[0]}")
        print(f"短信内容：{data[0][36]}，状态：{data[0][40]}")

        return data
