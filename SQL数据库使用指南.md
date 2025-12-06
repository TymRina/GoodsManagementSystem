# SQL数据库使用指南

## 1. 项目数据库架构概述

本项目采用MySQL数据库进行数据存储，使用PyMySQL库实现Python与MySQL的连接。项目采用分层架构设计：

- **数据库层**：MySQL数据库，存储商品、分类、品牌等核心业务数据
- **数据库管理层**：`DatabaseManager`类，负责数据库连接、SQL执行等基础操作
- **业务逻辑层**：各类Manager类（如`GoodsManager`、`CategoryManager`），封装具体业务逻辑
- **视图层**：UI组件，调用业务逻辑层完成数据展示与交互

## 2. 数据库连接配置

### 2.1 连接信息

数据库连接信息位于`src/modules/database.py`文件中，主要配置包括：

```python
class DatabaseManager:
    def __init__(self):
        self.host = 'localhost'          # 数据库主机地址
        self.port = 3306                 # 数据库端口
        self.user = 'root'               # 数据库用户名
        self.password = '123456'         # 数据库密码
        self.database = 'shukan_advanced' # 数据库名称
        self.charset = 'utf8mb4'         # 字符集
```

### 2.2 修改连接配置

如需修改数据库连接信息，直接编辑`src/modules/database.py`文件中的对应参数即可。

## 3. 数据库初始化

### 3.1 初始化脚本

项目提供了`init_database.py`脚本用于初始化数据库，包括：

1. 创建数据库（如果不存在）
2. 创建表结构
3. 插入初始数据

### 3.2 执行初始化

在项目根目录下执行以下命令完成数据库初始化：

```bash
python init_database.py
```

### 3.3 表结构说明

初始化脚本会创建以下表：

| 表名 | 描述 | 主要字段 |
|------|------|----------|
| categories | 商品分类表 | id, name, parent_id, created_at, updated_at |
| brands | 品牌表 | id, name, image_path, created_at, updated_at |
| goods | 商品表 | id, title, goods_code, category_id, brand_id, sale_price, original_price, stock, status, image_path, create_time, update_time |

## 4. 数据库操作方法

`DatabaseManager`类提供了以下核心方法：

| 方法名 | 描述 | 参数 | 返回值 |
|--------|------|------|--------|
| connect() | 连接数据库 | 无 | 无 |
| close() | 关闭数据库连接 | 无 | 无 |
| execute(sql, params) | 执行SQL语句 | sql: SQL语句, params: 参数列表 | 受影响的行数 |
| commit() | 提交事务 | 无 | 无 |
| fetch_all(sql, params) | 获取所有查询结果 | sql: SQL语句, params: 参数列表 | 结果列表 |
| fetch_one(sql, params) | 获取单个查询结果 | sql: SQL语句, params: 参数列表 | 单个结果 |
| create_tables() | 创建表结构 | 无 | 无 |
| init_data() | 插入初始数据 | 无 | 无 |

## 5. 业务逻辑层使用

### 5.1 核心Manager类

项目中已经实现了以下Manager类：

- **GoodsManager**：商品管理，包括获取商品列表、根据ID获取商品、添加商品、更新商品、删除商品等
- **CategoryManager**：分类管理，包括获取分类列表、根据ID获取分类、获取子分类、获取分类路径等

### 5.2 使用示例

#### 获取所有商品

```python
from src.modules.goods_manager import goods_manager

# 获取所有商品
goods_list = goods_manager.get_all_goods()
```

#### 根据ID获取商品

```python
# 根据ID获取商品
goods = goods_manager.get_goods_by_id(1)
```

#### 添加商品

```python
# 准备商品数据
goods_data = {
    'title': '测试商品',
    'goods_code': 'TEST001',
    'category_id': 1,
    'brand_id': 1,
    'sale_price': 99.99,
    'original_price': 199.99,
    'stock': 100,
    'status': 1,
    'image_path': 'resources/images/goods/test.jpg',
    'create_time': datetime.now(),
    'update_time': datetime.now()
}

# 添加商品
new_goods_id = goods_manager.add_goods(goods_data)
```

#### 更新商品

```python
# 准备更新数据
updated_data = {
    'title': '更新后的商品名称',
    'sale_price': 89.99,
    'update_time': datetime.now()
    # 其他需要更新的字段...
}

# 更新商品
goods_manager.update_goods(goods_id, updated_data)
```

#### 删除商品

```python
# 删除商品
goods_manager.delete_goods(goods_id)
```

## 6. 自定义业务逻辑

### 6.1 创建新的Manager类

如果需要添加新的业务逻辑，可以创建新的Manager类，例如：

```python
from src.modules.database import db_manager

class OrderManager:
    """订单管理类"""
    
    @staticmethod
    def get_orders_by_user(user_id):
        """根据用户ID获取订单"""
        sql = "SELECT * FROM orders WHERE user_id = %s ORDER BY create_time DESC"
        return db_manager.fetch_all(sql, (user_id,))
    
    # 其他方法...

# 全局订单管理器实例
order_manager = OrderManager()
```

### 6.2 执行自定义SQL

如果需要执行复杂的自定义SQL，可以直接使用`db_manager`：

```python
from src.modules.database import db_manager

# 执行自定义查询
sql = "SELECT c.name as category_name, COUNT(g.id) as goods_count " \
      "FROM categories c " \
      "LEFT JOIN goods g ON c.id = g.category_id " \
      "GROUP BY c.id"
result = db_manager.fetch_all(sql)
```

## 7. 最佳实践

### 7.1 连接管理

- 项目已实现自动连接管理，使用时无需手动调用`connect()`方法
- 长时间不使用数据库时，建议调用`close()`方法关闭连接

### 7.2 事务处理

- 执行插入、更新、删除操作后，需要调用`commit()`方法提交事务
- `DatabaseManager`类已实现事务回滚机制，发生异常时会自动回滚

### 7.3 参数化查询

- 始终使用参数化查询，避免SQL注入
- 正确使用`execute(sql, params)`方法，将参数作为元组传递

### 7.4 代码组织

- 业务逻辑应封装在Manager类中，避免直接在视图层执行SQL
- Manager类应提供清晰的接口，便于视图层调用

### 7.5 错误处理

- 捕获并处理数据库操作可能出现的异常
- 记录详细的错误日志，便于调试

## 8. 常见问题及解决方案

### 8.1 数据库连接失败

**问题**：执行脚本时提示"数据库连接失败"

**解决方案**：
1. 检查MySQL服务是否正常运行
2. 检查数据库连接信息是否正确
3. 确保数据库用户具有相应的权限

### 8.2 表创建失败

**问题**：执行初始化脚本时提示"数据库表创建失败"

**解决方案**：
1. 检查SQL语句是否正确
2. 确保数据库用户具有创建表的权限
3. 检查数据库是否已存在同名表

### 8.3 数据插入失败

**问题**：执行初始化脚本时提示"初始数据插入失败"

**解决方案**：
1. 检查数据格式是否正确
2. 确保外键约束条件满足
3. 检查数据库用户具有插入数据的权限

## 9. 扩展建议

### 9.1 添加新表

如需添加新表，建议按照以下步骤进行：

1. 在`DatabaseManager.create_tables()`方法中添加创建表的SQL语句
2. 在初始化数据方法中添加初始数据插入逻辑
3. 创建对应的Manager类封装业务逻辑

### 9.2 优化查询性能

对于大数据量查询，可以考虑：
1. 添加合适的索引
2. 优化SQL查询语句
3. 实现分页查询

### 9.3 数据备份与恢复

定期备份数据库，确保数据安全：

```bash
# 备份数据库
mysqldump -u root -p shukan_advanced > backup.sql

# 恢复数据库
mysql -u root -p shukan_advanced < backup.sql
```

## 10. 总结

本项目提供了完整的SQL数据库使用方案，包括：

- 便捷的数据库连接管理
- 清晰的业务逻辑分层
- 丰富的CRUD操作接口
- 完整的数据库初始化流程

通过遵循本指南，您可以轻松地在项目中使用SQL数据库，实现各种业务需求。