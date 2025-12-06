import csv
import os
import sys

# 确保能导入项目模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 直接导入DatabaseManager类
try:
    from src.modules.database import DatabaseManager
except ImportError:
    print("无法导入DatabaseManager类，请检查src/modules/database.py文件是否存在")
    sys.exit(1)

def import_goods_from_csv(csv_file_path):
    """
    从CSV文件导入商品数据到数据库
    
    参数:
    csv_file_path: str - CSV文件的绝对路径
    
    返回:
    bool - 导入是否成功
    """
    # 检查CSV文件是否存在
    if not os.path.exists(csv_file_path):
        print(f"错误: CSV文件不存在 - {csv_file_path}")
        return False
    
    try:
        # 创建数据库管理器实例
        db_manager = DatabaseManager()
        db_manager.connect()
        
        # 创建表（如果不存在）
        db_manager.create_tables()
        
        # 读取CSV文件
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # 跳过表头
            
            # 准备插入数据
            goods_data = []
            for row in reader:
                if len(row) < 12:
                    print(f"警告: 行数据不完整 - {row}")
                    continue
                    
                # 转换数据类型
                try:
                    goods_id = int(row[0])
                    name = row[1]
                    code = row[2]
                    category_id = int(row[3])
                    brand_id = int(row[4])
                    cost_price = float(row[5])
                    retail_price = float(row[6])
                    stock = int(row[7])
                    status = int(row[8])
                    image = row[9]
                    created_at = row[10]
                    updated_at = row[11]
                    
                    goods_data.append((
                        goods_id, name, code, category_id, brand_id, 
                        cost_price, retail_price, stock, status, image, 
                        created_at, updated_at
                    ))
                except ValueError as e:
                    print(f"警告: 数据类型转换错误 - {row} - {e}")
                    continue
            
            # 插入数据到数据库
            if goods_data:
                db_manager.cursor.executemany(
                    '''INSERT INTO goods (
                        id, name, code, category_id, brand_id, 
                        cost_price, retail_price, stock, status, image, 
                        created_at, updated_at
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )''', goods_data
                )
                
                # 提交事务
                db_manager.conn.commit()
                print(f"成功导入 {len(goods_data)} 条商品数据")
                return True
            else:
                print("没有可导入的数据")
                return False
                
    except Exception as e:
        print(f"导入过程中发生错误: {e}")
        return False
    finally:
        if 'db_manager' in locals():
            db_manager.close()

if __name__ == "__main__":
    # 示例用法：python import_data_from_csv.py "path/to/your/goods.csv"
    if len(sys.argv) != 2:
        print("用法: python import_data_from_csv.py 'csv_file_path'")
        print("请提供CSV文件的绝对路径")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    success = import_goods_from_csv(csv_path)
    
    if success:
        print("数据导入完成！")
    else:
        print("数据导入失败，请检查错误信息")
