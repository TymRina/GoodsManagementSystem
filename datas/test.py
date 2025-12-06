import datetime
from members import members
from categories import categories
from brands import brands
from goods import goods
from orders import orders


def test_data_relations():
    # 测试1: 所有用户ID是否唯一
    user_ids = [m[0] for m in members]
    assert len(user_ids) == len(set(user_ids)), "用户ID不唯一"

    # 测试2: 所有商品分类ID是否存在于分类数据中
    category_ids = [c[0] for c in categories]
    for product in goods:
        assert product[3] in category_ids, f"商品 {product[0]} 的分类ID {product[3]} 不存在"

    # 测试3: 所有商品品牌ID是否存在于品牌数据中
    brand_ids = [b[0] for b in brands]
    for product in goods:
        assert product[4] in brand_ids, f"商品 {product[0]} 的品牌ID {product[4]} 不存在"

    # 测试4: 所有订单的用户ID是否存在于会员数据中
    member_ids = [m[0] for m in members]
    for order in orders:
        assert order[2] in member_ids, f"订单 {order[0]} 的用户ID {order[2]} 不存在"

    # 测试5: 订单状态与时间逻辑一致性
    for order in orders:
        status = order[3]
        pay_time = order[8]
        ship_time = order[11]
        receive_time = order[12]

        if status >= 1:  # 待支付以上状态
            assert pay_time is not None, f"订单 {order[0]} 状态 {status} 但无支付时间"
        if status >= 2:  # 待发货以上状态
            assert ship_time is not None, f"订单 {order[0]} 状态 {status} 但无发货时间"
        if status >= 3:  # 待收货以上状态
            assert receive_time is not None, f"订单 {order[0]} 状态 {status} 但无收货时间"
            # 收货时间应在发货时间之后
            if ship_time and receive_time:
                ship_date = datetime.datetime.strptime(ship_time, "%Y-%m-%d %H:%M:%S")
                receive_date = datetime.datetime.strptime(receive_time, "%Y-%m-%d %H:%M:%S")
                assert receive_date > ship_date, f"订单 {order[0]} 收货时间早于发货时间"

    # 测试6: 订单金额合理性
    for order in orders:
        total = order[4]
        discount = order[5]
        payment = order[6]
        assert total > 0, f"订单 {order[0]} 总金额为0"
        assert discount >= 0, f"订单 {order[0]} 优惠金额为负"
        assert payment > 0, f"订单 {order[0]} 实付金额为0"
        assert abs((total - discount) - payment) < 0.05, f"订单 {order[0]} 金额计算错误"

    print("所有数据关联性测试通过！")


if __name__ == "__main__":
    test_data_relations()