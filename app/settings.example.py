"""Tortoise ORM 配置模板。

用法：复制本文件为 app/settings.py，填入自己的数据库账号密码。
app/settings.py 已被 .gitignore 排除，不会提交到仓库。
"""
# ---------------------------------------------------------- 总配置
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "YOUR_DB_PASSWORD",  # 改成自己的密码
                "database": "fastapi",
                "charset": "utf8mb4",
                "minsize": 1,  # 连接池下限
                "maxsize": 5,  # 连接池上限
                "echo": True,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}
