# 商品管理系统 (Goods Management System)

一个基于PyQt5开发的商品管理系统，集成了人脸识别登录功能，提供商品、品牌、订单、会员和系统管理等完整功能模块。
这边只做了登录和商品管理模块。

## 技术栈

- **开发语言**：Python 3.x
- **GUI框架**：PyQt5
- **人脸识别**：华为云人脸识别服务
- **图像处理**：OpenCV
- **数据处理**：NumPy
- **网络请求**：Requests

## 功能特性

### 📦 商品管理
- 商品列表展示与管理
- 商品发布功能
- 商品评价管理
- 商品类别管理

### 🏷️ 品牌管理
- 品牌列表展示与管理

### 📋 订单管理
- 订单列表展示与管理

### 👥 会员管理
- 会员列表展示与管理

### ⚙️ 系统管理
- 角色管理
- 权限管理
- 日志管理
- 数据备份

### 🔒 安全登录
- 传统账号密码登录
- 华为云人脸识别登录

## 项目结构

```
GoodsManagementSystem/
├── config/                # 配置文件目录
│   ├── menu_config.py     # 菜单配置
│   └── menu_config_all.py # 完整菜单配置
├── datas/                 # 数据相关文件
├── resources/             # 资源文件目录
│   ├── icons/             # 图标文件
│   ├── images/            # 图片文件
│   │   ├── faces/         # 人脸图片（需替换）
│   │   ├── goods/         # 商品图片
│   │   └── login/         # 登录界面图片
│   ├── styles/            # 样式文件
│   └── uploads/           # 上传文件目录
├── src/                   # 源代码目录
│   ├── controllers/       # 控制器
│   ├── models/            # 模型
│   ├── modules/           # 模块
│   └── views/             # 视图
├── ui/                    # UI文件目录
├── main.py                # 主程序入口
├── init_database.py       # 数据库初始化
├── requirements.txt       # 依赖文件
└── README.md              # 项目说明
```

## 安装与运行

### 1. 环境要求
- Python 3.7+
- pip 20.0+

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置华为云API（重要）

由于项目使用了华为云人脸识别服务，需要配置华为云API密钥：

1. 登录华为云控制台，创建人脸识别服务实例
2. 获取API密钥（Access Key ID和Secret Access Key）
3. 在项目中配置API密钥（具体见「隐私信息处理」部分）

### 4. 初始化数据库

```bash
python init_database.py
```

### 5. 运行项目

```bash
python main.py
```

## 隐私信息处理

### 1. 华为云API密钥

项目中使用了华为云人脸识别服务，包含实际的API密钥信息。在上传GitHub前，请执行以下操作：

- **文件位置**：`src/modules/face_compare.py`
- **处理方法**：将实际的API密钥替换为占位符，例如：
  ```python
  # 华为云API配置
  AK = "your_access_key_here"  # 替换为您的Access Key
  SK = "your_secret_key_here"  # 替换为您的Secret Key
  PROJECT_ID = "your_project_id_here"  # 替换为您的项目ID
  REGION = "your_region_here"  # 替换为您的区域
  ```
- **说明**：这些密钥用于华为云人脸识别服务，需要您在华为云控制台自行申请

### 2. admin.jpg人脸图片

项目中包含管理员人脸图片，用于人脸识别登录功能。在上传GitHub前，请执行以下操作：

- **文件位置**：`resources/images/faces/admin.jpg`
- **处理方法**：删除该文件或替换为您自己的人脸图片
- **说明**：如果删除该文件，人脸识别登录功能将无法使用，您可以使用账号密码登录

### 3. 其他隐私信息

- **数据库配置**：`src/modules/database.py`中包含数据库连接信息（用户名、密码等），建议使用环境变量或配置文件管理
- **credentials.csv**：根目录下的该文件包含华为云API密钥的CSV格式备份，在上传GitHub前请删除或替换为占位符内容
  ```csv
  User Name,Access Key Id,Secret Access Key
  your_user_name,your_access_key,your_secret_key
  ```

## 使用说明

### 登录系统

1. **账号密码登录**：输入用户名和密码登录
2. **人脸识别登录**：点击人脸识别按钮，系统将自动识别并登录

### 数据导入

如果您下载项目后数据库中没有商品数据，可以使用我们提供的CSV导入脚本快速导入数据。

#### 商品数据CSV格式

商品数据CSV文件需要包含以下字段（顺序不能改变）：

| 字段名       | 数据类型 | 说明               |
|-------------|---------|-------------------|
| id          | int     | 商品ID             |
| name        | string  | 商品名称           |
| code        | string  | 商品编码           |
| category_id | int     | 分类ID             |
| brand_id    | int     | 品牌ID             |
| cost_price  | float   | 成本价格           |
| retail_price| float   | 零售价格           |
| stock       | int     | 库存数量           |
| status      | int     | 状态（1-正常，0-下架） |
| image       | string  | 商品图片路径       |
| created_at  | string  | 创建时间           |
| updated_at  | string  | 更新时间           |

#### 使用导入脚本

1. 准备好符合上述格式的CSV文件
2. 运行导入脚本：

```bash
python import_data_from_csv.py "path/to/your/goods.csv"
```

请将 `"path/to/your/goods.csv"` 替换为您的CSV文件的绝对路径。

#### 示例数据

我们在项目根目录提供了一个示例CSV文件 `example_goods.csv`，您可以参考其格式创建自己的数据文件。

### 功能操作

1. **商品管理**：在左侧菜单选择「商品管理」，可以进行商品的查看、发布、编辑和删除操作
2. **品牌管理**：在左侧菜单选择「品牌管理」，可以进行品牌的查看、添加、编辑和删除操作
3. **订单管理**：在左侧菜单选择「订单管理」，可以查看和管理订单信息
4. **会员管理**：在左侧菜单选择「会员管理」，可以查看和管理会员信息
5. **系统管理**：在左侧菜单选择「系统管理」，可以进行角色、权限、日志和数据备份管理

## 注意事项

1. **华为云服务费用**：使用华为云人脸识别服务可能产生费用，请参考华为云官方定价
2. **人脸图片要求**：用于识别的人脸图片请确保清晰，正面拍摄
3. **数据库备份**：定期备份数据库，避免数据丢失
4. **系统安全**：请妥善保管管理员账号和API密钥信息
5. **隐私保护**：请遵守相关法律法规，保护用户隐私信息

## 开发说明

### 添加新功能

1. 在`ui/`目录下创建新的UI文件
2. 在`src/controllers/`目录下创建对应的控制器
3. 在`src/models/`目录下创建对应的模型
4. 在`config/menu_config.py`中添加菜单配置

### 调试与测试

- 使用PyQt5 Designer设计UI界面
- 使用Python的调试工具进行代码调试
- 测试人脸识别功能时，请确保网络连接正常

## 许可证

本项目仅供学习和参考使用。

## 更新日志

- v1.0.0：初始版本，包含基本的商品管理功能
- v1.1.0：添加品牌管理、订单管理和会员管理功能
- v1.2.0：添加系统管理功能
- v1.3.0：集成华为云人脸识别登录功能

## 联系方式

如有问题或建议，欢迎联系项目维护者。