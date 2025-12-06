from src.modules.database import db_manager

class GoodsManager:
    """商品管理类"""
    
    @staticmethod
    def get_all_goods():
        """获取所有商品"""
        sql = "SELECT * FROM goods ORDER BY id DESC"
        return db_manager.fetch_all(sql)
    
    @staticmethod
    def get_goods_by_id(goods_id):
        """根据ID获取商品"""
        sql = "SELECT * FROM goods WHERE id = %s"
        return db_manager.fetch_one(sql, (goods_id,))
    
    @staticmethod
    def add_goods(goods_data):
        """添加商品"""
        sql = """
        INSERT INTO goods (
            title, goods_code, category_id, brand_id, 
            sale_price, original_price, stock, status, 
            image_path, create_time, update_time
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        params = (
            goods_data['title'],
            goods_data.get('goods_code', ''),
            goods_data['category_id'],
            goods_data['brand_id'],
            goods_data['sale_price'],
            goods_data['original_price'],
            goods_data['stock'],
            goods_data['status'],
            goods_data.get('image_path', ''),
            goods_data['create_time'],
            goods_data['update_time']
        )
        
        db_manager.execute(sql, params)
        db_manager.commit()
        return db_manager.cursor.lastrowid
    
    @staticmethod
    def update_goods(goods_id, goods_data):
        """更新商品"""
        sql = """
        UPDATE goods SET 
            title = %s, category_id = %s, brand_id = %s, 
            sale_price = %s, original_price = %s, stock = %s, 
            status = %s, image_path = %s, update_time = %s
        WHERE id = %s
        """
        
        params = (
            goods_data['title'],
            goods_data['category_id'],
            goods_data['brand_id'],
            goods_data['sale_price'],
            goods_data['original_price'],
            goods_data['stock'],
            goods_data['status'],
            goods_data.get('image_path', ''),
            goods_data['update_time'],
            goods_id
        )
        
        db_manager.execute(sql, params)
        db_manager.commit()
        return db_manager.cursor.rowcount
    
    @staticmethod
    def delete_goods(goods_id):
        """删除商品"""
        sql = "DELETE FROM goods WHERE id = %s"
        db_manager.execute(sql, (goods_id,))
        db_manager.commit()
        return db_manager.cursor.rowcount
    
    @staticmethod
    def get_goods_count():
        """获取商品总数"""
        sql = "SELECT COUNT(*) as count FROM goods"
        result = db_manager.fetch_one(sql)
        return result['count'] if result else 0
    
    @staticmethod
    def get_goods_by_page(page, per_page):
        """分页获取商品"""
        offset = (page - 1) * per_page
        sql = "SELECT * FROM goods ORDER BY id DESC LIMIT %s OFFSET %s"
        return db_manager.fetch_all(sql, (per_page, offset))

# 全局商品管理器实例
goods_manager = GoodsManager()