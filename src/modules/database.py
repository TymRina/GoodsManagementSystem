import pymysql
from pymysql.cursors import DictCursor

class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self):
        self.host = 'localhost'  # 数据库主机地址
        self.port = 3306  # 数据库端口
        self.user = 'your_username'  # 替换为您的数据库用户名
        self.password = 'your_password'  # 替换为您的数据库密码
        self.database = 'your_database_name'  # 替换为您的数据库名称
        self.charset = 'utf8mb4'
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                cursorclass=DictCursor
            )
            self.cursor = self.connection.cursor()
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {str(e)}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute(self, sql, params=None):
        """执行SQL语句"""
        try:
            if not self.connection:
                self.connect()
            return self.cursor.execute(sql, params)
        except Exception as e:
            print(f"SQL执行失败: {str(e)}")
            if self.connection:
                self.connection.rollback()
            raise
    
    def commit(self):
        """提交事务"""
        try:
            self.connection.commit()
        except Exception as e:
            print(f"事务提交失败: {str(e)}")
            if self.connection:
                self.connection.rollback()
            raise
    
    def fetch_all(self, sql, params=None):
        """获取所有查询结果"""
        self.execute(sql, params)
        return self.cursor.fetchall()
    
    def fetch_one(self, sql, params=None):
        """获取单个查询结果"""
        self.execute(sql, params)
        return self.cursor.fetchone()
    
    def create_tables(self):
        """创建数据库表"""
        # 创建分类表
        categories_sql = """
        CREATE TABLE IF NOT EXISTS categories (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            parent_id INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        
        # 创建品牌表
        brands_sql = """
        CREATE TABLE IF NOT EXISTS brands (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            image_path VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        
        # 创建商品表
        goods_sql = """
        CREATE TABLE IF NOT EXISTS goods (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            goods_code VARCHAR(50) DEFAULT '',
            category_id INT NOT NULL,
            brand_id INT NOT NULL,
            sale_price DECIMAL(10, 2) NOT NULL,
            original_price DECIMAL(10, 2) NOT NULL,
            stock INT NOT NULL DEFAULT 0,
            status TINYINT NOT NULL DEFAULT 1,
            image_path VARCHAR(255),
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (brand_id) REFERENCES brands(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        
        try:
            self.execute(categories_sql)
            self.execute(brands_sql)
            self.execute(goods_sql)
            self.commit()
            print("数据库表创建成功")
        except Exception as e:
            print(f"数据库表创建失败: {str(e)}")
            if self.connection:
                self.connection.rollback()
            raise
    
    def init_data(self):
        """初始化数据"""
        from datas.categories import categories as categories_data
        from datas.brands import brands as brands_data
        from datas.goods import goods as goods_data
        
        try:
            # 插入分类数据
            for category in categories_data:
                self.execute(
                    "INSERT INTO categories (id, name, parent_id) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name), parent_id=VALUES(parent_id)",
                    category
                )
            
            # 插入品牌数据
            for brand in brands_data:
                self.execute(
                    "INSERT INTO brands (id, name, image_path) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name), image_path=VALUES(image_path)",
                    brand
                )
            
            # 插入商品数据
            for goods in goods_data:
                self.execute(
                    "INSERT INTO goods (id, title, goods_code, category_id, brand_id, sale_price, original_price, stock, status, image_path, create_time, update_time) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                    "ON DUPLICATE KEY UPDATE title=VALUES(title), goods_code=VALUES(goods_code), category_id=VALUES(category_id), brand_id=VALUES(brand_id), "
                    "sale_price=VALUES(sale_price), original_price=VALUES(original_price), stock=VALUES(stock), status=VALUES(status), "
                    "image_path=VALUES(image_path), create_time=VALUES(create_time), update_time=VALUES(update_time)",
                    goods
                )
            
            self.commit()
            print("初始数据插入成功")
        except Exception as e:
            print(f"初始数据插入失败: {str(e)}")
            if self.connection:
                self.connection.rollback()
            raise

# 全局数据库管理器实例
db_manager = DatabaseManager()