from api.utils.database import db
from api.model.users import ColorUser
from api.model.users import ColorUserSchema

class Users:
    def get_all_users(self):
        fetched = ColorUser.query.all()
        users_schema = ColorUserSchema(many=True)
        users = users_schema.dump(fetched)
        return users

    def get_user_by_id(self, user_id):
        fetched = ColorUser.query.get_or_404(user_id)
        users_schema = ColorUserSchema()
        user = users_schema.dump(fetched)
        return user

    def add_user(self, data):
        # 将json转换为dict
        color_user_schema = ColorUserSchema()
        user_schema = color_user_schema.load(data)
        # 实例化模型类
        color_user = ColorUser(user_schema['name'], user_schema['email'], user_schema['password'],
                               user_schema['openid'], user_schema['status'])
        # 通过create()将对象添加到数据库
        result = color_user_schema.dump(color_user.create())
        return result

    def delete_user_by_id(self, user_id):
        fetched = ColorUser.query.get_or_404(user_id)
        db.session.delete(fetched)
        db.session.commit()
        return user_id

    def update_user_by_id(self, user_id, data):
        fetched = ColorUser.query.get_or_404(user_id)
        fetched.name = data['name']
        fetched.email = data['email']
        fetched.password = data['password']
        fetched.openid = data['openid']
        fetched.status = data['status']
        db.session.add(fetched)
        db.session.commit()
        users_schema = ColorUserSchema()
        user = users_schema.dump(fetched)
        return user

    def get_user_with_role_by_id(self, user_id):
        fetched = ColorUser.query.get_or_404(user_id)
        users_schema = ColorUserSchema()
        user = users_schema.dump(fetched)
        return user
