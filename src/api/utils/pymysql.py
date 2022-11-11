import pymysql
import pandas as pd

class mysqlDB:
    pd_dict = {
        "color_rgb": ['id', 'red', 'green', 'blue', 'standard_id']
    }
    def __init__(self):
        db = 'color'
        host = 'localhost'
        user = 'admin'
        passwd = 'tw7311'

        self.connect = pymysql.connect(
            db=db,
            host=host,
            user=user,
            passwd=passwd,
            charset='utf8',
            use_unicode=True
        )
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def read_db_with_table_name_and_row_id(self, table_name, row_id):
        read_sql = "SELECT * FROM %s WHERE id=%s" % (table_name, row_id)
        self.cursor.execute(read_sql)
        result = self.cursor.fetchall()
        pd_result = pd.DataFrame(list(result), columns=self.get_col(table_name))
        self.close_spider()
        return pd_result

    def close_spider(self):
        self.cursor.close()
        self.connect.close()

    def get_col(self, table_name):
        return self.pd_dict[table_name]