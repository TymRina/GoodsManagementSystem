from src.modules.database import db_manager

class CategoryManager:
    """分类管理类"""
    
    @staticmethod
    def get_all_categories():
        """获取所有分类"""
        sql = "SELECT * FROM categories ORDER BY id"
        return db_manager.fetch_all(sql)
    
    @staticmethod
    def get_category_by_id(category_id):
        """根据ID获取分类"""
        sql = "SELECT * FROM categories WHERE id = %s"
        return db_manager.fetch_one(sql, (category_id,))
    
    @staticmethod
    def get_subcategories(parent_id):
        """获取子分类"""
        sql = "SELECT * FROM categories WHERE parent_id = %s ORDER BY id"
        return db_manager.fetch_all(sql, (parent_id,))
    
    @staticmethod
    def get_category_path(category_id):
        """获取分类路径"""
        category = CategoryManager.get_category_by_id(category_id)
        if not category:
            return "未知分类"
        
        path = [category['name']]
        parent_id = category['parent_id']
        
        # 递归获取父分类
        while parent_id != 0:
            parent = CategoryManager.get_category_by_id(parent_id)
            if not parent:
                break
            path.insert(0, parent['name'])
            parent_id = parent['parent_id']
        
        return '/'.join(path)
    
    @staticmethod
    def get_category_id(level1_id, level2_id, level3_id):
        """根据三级分类ID获取最终分类ID"""
        if level3_id:
            return level3_id
        if level2_id:
            return level2_id
        if level1_id:
            return level1_id
        return 0

class BrandManager:
    """品牌管理类"""
    
    @staticmethod
    def get_all_brands():
        """获取所有品牌"""
        sql = "SELECT * FROM brands ORDER BY id"
        return db_manager.fetch_all(sql)
    
    @staticmethod
    def get_brand_by_id(brand_id):
        """根据ID获取品牌"""
        sql = "SELECT * FROM brands WHERE id = %s"
        return db_manager.fetch_one(sql, (brand_id,))

# 全局管理器实例
category_manager = CategoryManager()
brand_manager = BrandManager()