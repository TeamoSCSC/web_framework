import pymysql

import secret
import config
from models.base_model import SQLModel
from models.comment import Comment
from models.session import Session
from models.user_role import UserRole
from models.user import User
# from models.weibo import Weibo
# from models.comment import Comment
from models.weibo import Weibo
from utils import log


def recreate_table(cursor):
    # cursor.execute(Test.sql_create)
    cursor.execute(User.sql_create)
    cursor.execute(Session.sql_create)
    cursor.execute(Weibo.sql_create)
    cursor.execute(Comment.sql_create)


def recreate_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=secret.mysql_password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'DROP DATABASE IF EXISTS `{}`'.format(
                    config.db_name
                )
            )
            cursor.execute(
                'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
                    config.db_name
                )
            )
            cursor.execute('USE `{}`'.format(config.db_name))

            recreate_table(cursor)

        connection.commit()
    finally:
        connection.close()


def test_data():
    SQLModel.init_db()

    # Test.new({})

    # form = dict(
    #     username='scsc,
    #     password='123',
    #     role=UserRole.normal,
    # )
    # log('@@@lenform', len(form))
    # User.new(form)
    # u = User.all()
    # log('@@@u', u)
    # Session.add(u.id)

    # form = dict(
    #     content='scsc',
    #     user_id=2,
    #     weibo_id=3,
    # )
    # Comment.new(form)
    # u = Comment(form)
    # log('@@@u', u.user())

    # form = dict(
    #     id = 2,
    #     content='change weibo',
    # )
    # Weibo.weibo_update(form)
    # w = Weibo.one(id=2)
    # cs = w.comments()
    # log('@@@cs', cs)

    # form = dict(
    #     content='test comment',
    #     weibo_id=w.id,
    # )
    # Weibo.comment_add(form, u.id)

    # SQLModel.connection.close()


if __name__ == '__main__':
    recreate_database()
    test_data()
