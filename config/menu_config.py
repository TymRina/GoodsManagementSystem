MENU_CONFIGS = [
    {
        'title': '商品管理',
        'items': [
            {'name': '商品列表', 'icon': 'fa5s.list', 'page': 1, 'ui_path': 'ui/goods/goods_list.ui'},
            {'name': '商品发布', 'icon': 'fa5.paper-plane', 'page': 2, 'ui_path': 'ui/goods/goods_publish.ui'},
            {'name': '商品评价', 'icon': 'fa5s.comment-dots', 'page': 3, 'ui_path': 'ui/goods/comment_list.ui'},
            {'name': '商品类别', 'icon': 'mdi6.apps', 'page': 4, 'ui_path': 'ui/goods/category_list.ui'},
        ]
    },
    {
        'title': '品牌管理',
        "items": [
            {'name': '品牌列表', 'icon': 'fa5s.list', 'page': 5, 'ui_path': 'ui/brands/brand_list.ui'}
        ]
    },
    {
        'title': '订单管理',
        "items": [
            {'name': '订单列表', 'icon': 'fa5s.list', 'page': 6, 'ui_path': 'ui/orders/order_list.ui'},
        ]
    },
    {
        'title': '会员管理',
        'items': [
            {'name': '会员列表', 'icon': 'fa5s.user-friends', 'page': 16, 'ui_path': 'ui/members/members_list.ui'},
        ]
    },
    {
        'title': '系统管理',
        'items': [
            {'name': '角色管理', 'icon': 'ph.user-thin', 'page': 20, 'ui_path': 'ui/system/roles_list.ui'},
            {'name': '权限管理', 'icon': 'ri.key-2-line', 'page': 21, 'ui_path': 'ui/system/permissions_list.ui'},
            {'name': '日志管理', 'icon': 'ri.file-list-3-fill', 'page': 23, 'ui_path': 'ui/system/backup_list.ui'},
            {'name': '数据备份', 'icon': 'fa5s.database', 'page': 24, 'ui_path': 'ui/system/logs_list.ui'},
        ]
    },
]
