import random
from datetime import datetime, timedelta


# 生成评价数据
def generate_comments(num_comments=100, num_orders=2000, num_users=1000):
    """
    生成商品评价数据

    参数:
    num_comments - 要生成的评价数量 (默认: 100)
    num_orders - 订单数量 (默认: 2000)
    num_users - 用户数量 (默认: 1000)

    返回:
    评价数据列表(列表包裹元组)
    """
    comments = []

    # 生成订单数据
    orders = []
    for i in range(1, num_orders + 1):
        # 生成随机时间 (2025年内)
        order_date = datetime(2025, random.randint(1, 12), random.randint(1, 28),
                              random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        order_id = int(order_date.strftime("%Y%m%d%H%M%S") + str(random.randint(1000000, 9999999)))
        user_id = random.randint(1, num_users)  # 随机分配用户ID
        orders.append((order_id, user_id))

    # 生成评价数据
    for i in range(1, num_comments + 1):
        comment_id = i
        rating = random.randint(1, 5)

        # 随机选择评价内容
        comment_text = random.choice([
            "商品质量非常好，超出预期！",
            "物流速度很快，包装完好无损",
            "与描述一致，非常满意",
            "性价比很高，会再次购买",
            "客服态度很好，解决问题及时",
            "使用效果一般，没有想象中好",
            "商品有瑕疵，但客服处理很及时",
            "尺寸不太合适，其他都还好",
            "非常失望，与图片不符",
            "一般般，没有特别惊喜",
            "强烈推荐，物超所值",
            "包装精美，送礼很合适",
            "功能齐全，操作简单",
            "颜色很正，和图片一样",
            "材质很好，手感舒适",
            "安装简单，使用方便",
            "用了几天感觉不错",
            "性价比高，值得购买",
            "发货速度快，服务态度好",
            "有轻微划痕，但不影响使用"
        ])

        # 生成评价图片路径
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        image_path = f"../../images/comments/2025{month:02d}{day:02d}/{random.randint(1, 10)}.png"

        # 随机选择一个订单
        order = random.choice(orders)
        order_id = order[0]
        user_id = order[1]

        # 生成随机时间 (2025年内)
        create_time = datetime(2025, random.randint(1, 12), random.randint(1, 28),
                               random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        update_time = create_time + timedelta(days=random.randint(0, 30))

        # 添加到评价列表(列表包裹元组)
        comments.append((
            comment_id,
            rating,
            comment_text,
            image_path,
            order_id,
            user_id,
            create_time.strftime("%Y-%m-%d %H:%M:%S"),
            update_time.strftime("%Y-%m-%d %H:%M:%S")
        ))

    return comments


def save_comments_to_py(comments, filename='comments.py'):
    """
    将生成的评价数据保存到 Python 文件中

    参数:
    comments - 评价数据列表(列表包裹元组)
    filename - 保存的 Python 文件名 (默认: comments.py)
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("# 自动生成的评价数据\n")
        file.write("comments_data = [\n")

        # 写入每条评价数据
        for comment in comments:
            # 转义字符串中的引号
            escaped_text = comment[2].replace("'", "\\'")
            file.write(
                f"    ({comment[0]}, {comment[1]}, '{escaped_text}', '{comment[3]}', {comment[4]}, {comment[5]}, '{comment[6]}', '{comment[7]}'),\n")

        file.write("]\n")

    print(f"成功将 {len(comments)} 条评价数据保存到 {filename} 文件中")


# 测试生成函数
if __name__ == "__main__":
    # 生成100条评价数据
    comments = generate_comments(100)
    print(f"成功生成 {len(comments)} 条评价数据(列表包裹元组格式)")
    print("数据格式示例:")
    print("comments_data = [")
    for i in range(min(3, len(comments))):
        print(f"    {comments[i]},")
    if len(comments) > 0:
        print("    ...")
    print("]")

    # 保存到 Python 文件
    save_comments_to_py(comments)    