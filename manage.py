# 命令行文件

from flask_script import Manager
from flas_migrate import Migrate, MigrateCommand
from zingqa import app
from exts import db
# 还需要将创建好的模型导入进来

manager = Manager(app)

# 使用 Migrate 绑定 app 和 db
migrate = Migrate(app, db)

# 添加迁移脚本命令到 manager 中
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()