import random
import string
import datetime
from categories import categories
from brands import brands

# 商品数据 (2000条)
goods = []
for i in range(1, 2001):
    # 商品标题 (不少于10个字)
    prefixes = ['新款', '旗舰', '高性能', '智能', '专业', '超薄', '大容量', '便携', '高速', '节能']
    types = ['笔记本电脑', '智能手机', '数码相机', '平板电视', '冰箱', '洗衣机', '空调', '耳机',
             '手表', '运动鞋', '外套', '连衣裙', '背包', '厨具', '玩具', '化妆品', '食品', '书籍']
    features = ['高清', '无线', '蓝牙', '防水', '防摔', '长续航', '多功能', '可折叠', '触控', '智能控制']

    title = f"{random.choice(prefixes)}{random.choice(features)}{random.choice(types)} " \
            f"{random.randint(1, 5)}代 {random.choice(['专业版', '旗舰版', '尊享版', '青春版'])}"

    # 商品编码 (15位唯一)
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

    # 分类ID (从分类数据中随机选择)
    category = random.choice(categories)
    category_id = category[0]

    # 品牌ID (从200个品牌中选择)
    brand = random.choice(brands)
    brand_id = brand[0]

    # 价格
    original_price = round(random.uniform(50, 10000), 2)
    sale_price = round(original_price * random.uniform(0.5, 0.95), 2)

    # 库存
    stock = random.randint(100, 10000)

    # 状态
    status = 1 if random.random() > 0.1 else 0

    # 主图URL
    image = f"../../images/goods/{random.randint(1, 100)}.png"

    # 创建时间 (最近1年内)
    create_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
    create_time = create_date.strftime("%Y-%m-%d %H:%M:%S")

    # 修改时间 (在创建时间之后)
    update_date = create_date + datetime.timedelta(days=random.randint(0, 30))
    update_time = update_date.strftime("%Y-%m-%d %H:%M:%S")

    goods.append((
        i,  # 商品ID
        title,  # 商品标题
        code,  # 商品编码
        category_id,  # 分类ID
        brand_id,  # 品牌ID
        sale_price,  # 售价
        original_price,  # 原价
        stock,  # 库存
        status,  # 状态
        image,  # 主图URL
        create_time,  # 创建时间
        update_time  # 修改时间
    ))

# 导出商品数据
with open('goods.py', 'w', encoding='utf-8') as f:
    f.write("goods = [\n")
    for product in goods:
        f.write(f"    {product},\n")
    f.write("]\n")
