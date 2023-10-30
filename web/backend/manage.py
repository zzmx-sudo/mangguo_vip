import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask_script import Manager
from flask_migrate import MigrateCommand

from web.backend import create_app

# manager监管app
app = create_app()
manager = Manager(app)

# 配置db命令
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()
