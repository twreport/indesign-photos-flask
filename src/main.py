import os
import logging
from flask import Flask
from flask import jsonify
from api.utils.database import db
from api.utils.database import ma
from api.routes.users import users_routes
from api.routes.standards import standards_routes
from api.routes.roles import roles_routes
from api.routes.photos import photos_routes
from api.routes.palette import palette_routes
from api.utils.responses import response_with
import api.utils.responses as resp
from api.config.config import DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

# 根据不同环境读取相应配置
app.config.from_object(app_config)

# 避免中文返回ascii码
app.config['JSON_AS_ASCII'] = False

# 初始化数据库和json模块
db.init_app(app)
ma.init_app(app)
with app.app_context():
    db.create_all()

# 注册模块的路由
app.register_blueprint(users_routes, url_prefix='/api/users')
app.register_blueprint(roles_routes, url_prefix='/api/roles')
app.register_blueprint(standards_routes, url_prefix='/api/standards')
app.register_blueprint(photos_routes, url_prefix='/api/photos')
app.register_blueprint(palette_routes, url_prefix='/api/palette')

# START GLOBAL HTTP CONFIGURATIONS
@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)

@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)
