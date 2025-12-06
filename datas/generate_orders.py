import random
import string
import datetime
from members import members
from goods import goods

# 订单数据 (2000条)
orders = []
for i in range(1, 2001):
    # 订单号
    now = datetime.datetime.now()
    order_no = now.strftime("%Y%m%d%H%M%S") + ''.join(random.choices(string.digits, k=10))

    # 用户ID
    member = random.choice(members)
    user_id = member[0]

    # 订单状态
    status_weights = [0.15, 0.15, 0.15, 0.25, 0.2, 0.1]  # 不同状态的概率
    status = random.choices([0, 1, 2, 3, 4, 5], weights=status_weights)[0]

    # 金额 (基于商品价格)
    product_count = random.randint(1, 10)
    total_amount = 0
    for _ in range(product_count):
        product = random.choice(goods)
        total_amount += product[5] * random.randint(1, 5)  # 售价 * 数量

    discount_ratio = random.uniform(0.05, 0.3)
    payment_amount = round(total_amount * (1 - discount_ratio), 2)
    discount = round(total_amount - payment_amount, 2)  # 反推计算保证等式成立

    # 支付方式
    payment_method = random.randint(0, 3)

    # 支付时间（仅依赖状态）
    if status >= 1:
        pay_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
        pay_time = pay_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        pay_time = None

    # 支付流水号（仅依赖状态）
    if status >= 1:
        pay_id = f"{random.randint(100, 999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
    else:
        pay_id = None

    # 物流单号
    logistics_companies = ['SF', 'YT', 'ST', 'ZT', 'YD']  # 顺丰、圆通、申通、中通、韵达
    company = random.choice(logistics_companies)
    logistics_no = f"{company}{random.randint(100000000000, 999999999999)}"

    # 发货时间 (状态2以上)
    if status >= 2:
        if pay_time:
            ship_date = datetime.datetime.strptime(pay_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
                days=random.randint(1, 3))
        else:
            ship_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 15))
        ship_time = ship_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        ship_time = None

    # 收货时间 (状态3以上)
    if status >= 3 and ship_time:
        receive_date = datetime.datetime.strptime(ship_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
            days=random.randint(1, 7))
        receive_time = receive_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        receive_time = None

    # 收货信息 (从会员信息中获取)
    receiver_name = member[6]  # 昵称
    receiver_phone = member[3]  # 手机号
    receiver_address = member[9]  # 收货地址

    orders.append((
        i,  # 订单ID
        order_no,  # 订单号
        user_id,  # 用户ID
        status,  # 订单状态
        total_amount,  # 总金额
        discount,  # 优惠金额
        payment_amount,  # 实付金额
        payment_method,  # 支付方式
        pay_time,  # 支付时间
        pay_id,  # 支付流水号
        logistics_no,  # 物流单号
        ship_time,  # 发货时间
        receive_time,  # 收货时间
        receiver_name,  # 收货人名称
        receiver_phone,  # 收货人电话
        receiver_address  # 收货地址
    ))

# 导出订单数据
with open('orders.py', 'w', encoding='utf-8') as f:
    f.write("orders = [\n")
    for order in orders:
        f.write(f"    {order},\n")
    f.write("]\n")