import pymysql
from src.modules.database import db_manager

# 首先创建数据库
def create_database():
    """创建数据库"""
    try:
        # 不指定数据库连接
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS shukan_advanced CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("数据库创建成功")
        
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"数据库创建失败: {str(e)}")
        raise

if __name__ == "__main__":
    # 创建数据库
    create_database()
    
    # 连接数据库并创建表
    db_manager.connect()
    
    # 创建表结构
    db_manager.create_tables()
    
    # 插入初始数据
    db_manager.init_data()
    
    # 关闭连接
    db_manager.close()
    
    print("数据库初始化完成")