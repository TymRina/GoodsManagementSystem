# -*- coding: utf-8 -*-

import random
import string
import datetime
import hashlib
import calendar  # 为了移除28天的限制

# 全国省份
provinces = ["北京市", "天津市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省",
             "上海市", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省", "湖北省",
             "湖南省", "广东省", "广西壮族自治区", "海南省", "重庆市", "四川省", "贵州省", "云南省",
             "西藏自治区", "陕西省", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区", "台湾省",
             "香港特别行政区", "澳门特别行政区"]

# 主要城市
cities = {
    "北京市": ["北京市"],
    "天津市": ["天津市"],
    "河北省": ["石家庄市", "唐山市", "秦皇岛市", "邯郸市", "邢台市", "保定市", "张家口市", "承德市", "沧州市", "廊坊市",
               "衡水市"],
    "山西省": ["太原市", "大同市", "阳泉市", "长治市", "晋城市", "朔州市", "晋中市", "运城市", "忻州市", "临汾市",
               "吕梁市"],
}

# 区县数据
districts = {
    "北京市": ["东城区", "西城区", "朝阳区", "丰台区", "石景山区", "海淀区", "门头沟区", "房山区", "通州区", "顺义区",
               "昌平区", "大兴区", "怀柔区", "平谷区", "密云区", "延庆区"],
    "上海市": ["黄浦区", "徐汇区", "长宁区", "静安区", "普陀区", "虹口区", "杨浦区", "闵行区", "宝山区", "嘉定区",
               "浦东新区", "金山区", "松江区", "青浦区", "奉贤区", "崇明区"],
}

streets = [
    "中山路", "解放路", "人民路", "建设路", "创业路", "科技园路", "学院路", "和园路", "长安街", "南京路",
    "淮海路", "王府井大街", "春熙路", "解放碑步行街", "西湖大道", "珠江路", "滨海大道", "天府大道", "中关村大街",
    "五道口", "陆家嘴环路", "外滩", "滨江路", "大学城路", "创新大道", "生态园路", "文化路", "体育路", "健康路",
    "和平路", "和谐路", "光明路", "幸福路", "胜利路", "团结路", "友谊路", "自由路", "民主路", "科学路",
    "发展大道", "振兴路", "希望路", "未来路", "梦想路", "星光大道", "阳光路", "月光路", "星辰路", "银河路",
    "长江路", "黄河路", "珠江路", "泰山路", "华山路", "衡山路", "嵩山路", "恒山路", "武夷路", "黄山路",
    "西湖路", "东湖路", "南湖路", "北湖路", "滨海路", "海岸路", "海洋路", "海岛路", "森林路", "花园路",
    "公园路", "广场路", "中心路", "环城路", "高架路", "立交路", "隧道路", "大桥路", "小桥路", "河滨路",
    "湖畔路", "山景路", "海景路", "林荫大道", "梧桐大道", "樱花路", "枫叶路", "银杏路", "松柏路", "竹林路",
    "梅花路", "兰花路", "菊花路", "荷花路", "牡丹路", "玫瑰路", "百合路", "郁金香路", "紫荆路", "紫薇路"
]


communities = [
    "天府新苑", "阳光花园", "绿城小区", "学府家园", "中央公馆", "锦绣华庭", "碧桂园", "万科城", "恒大御景", "保利国际",
    "龙湖天街", "华润置地", "中海国际", "金地格林", "绿地新城", "远洋天地", "融创壹号", "世茂滨江", "招商雍景湾",
    "雅居乐",
    "星河湾", "汤臣一品", "翠湖天地", "仁恒滨江", "四季雅苑", "湖畔花园", "森林半岛", "海景壹号", "城市之光",
    "金色家园",
    "幸福里", "和谐家园", "温馨家园", "平安小区", "如意家园", "吉祥小区", "富贵花园", "金玉满堂", "紫气东来",
    "福星高照",
    "翰林院", "状元府", "书香门第", "文华苑", "智慧城", "创新园", "科技园", "创业园", "生态园", "环保小区",
    "绿洲家园", "蓝天白云", "碧水蓝天", "青山绿水", "森林氧吧", "湖畔人家", "海滨花园", "江山如画", "山水名城",
    "风景这边",
    "世纪城", "时代广场", "未来城", "梦想家园", "星光天地", "阳光海岸", "月光湖畔", "星辰大海", "银河国际", "宇宙中心",
    "东方明珠", "西方银座", "南方新城", "北方天地", "中南海景", "西湖印象", "东湖国际", "南湖雅居", "北湖公馆",
    "滨海壹号",
    "海岸明珠", "海洋之星", "海岛风情", "森林城堡", "花园洋房", "公园世家", "广场公寓", "中心别墅", "环城国际", "高架雅苑"
]

common_chars = "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞"

# 常用英文单词
english_words = ["Sunny", "Rainbow", "Moon", "Star", "Sky", "Ocean", "River", "Mountain", "Forest", "Flower",
                 "Dream", "Hope", "Joy", "Peace", "Love", "Happy", "Smart", "Brave", "Kind", "Gentle",
                 "Creative", "Adventure", "Explore", "Journey", "Travel", "Freedom", "Wisdom", "Knowledge",
                 "Book", "Music", "Art", "Dance", "Smile", "Laugh", "Friend", "Family", "Home", "City",
                 "Nature", "Green", "Blue", "Red", "Yellow", "Purple", "Orange", "Pink", "White", "Black",
                 "Gold", "Silver", "Diamond", "Crystal", "Angel", "Hero", "Champion", "Winner", "Genius",
                 "Legend", "Myth", "Fantasy", "Magic", "Sparkle", "Twinkle", "Shine", "Glow", "Bright",
                 "Clear", "Fresh", "Cool", "Warm", "Sweet", "Sour", "Bitter", "Spicy", "Delicious", "Tasty",
                 "Fast", "Quick", "Slow", "Calm", "Quiet", "Loud", "Strong", "Weak", "Big", "Small", "Tall",
                 "Short", "Long", "New", "Old", "Young", "Modern", "Classic", "Vintage", "Digital", "Analog"]

# 会员信息 (2000条)
members = []
for i in range(1, 2001):
    # 用户名 (添加shukan_前缀)
    username = f"shukan_{''.join(random.choices(string.ascii_lowercase, k=8))}"

    # 密码 (随机md5)
    password = hashlib.md5(f"pass{i}{random.randint(1000, 9999)}".encode()).hexdigest()

    # 手机号 (唯一)
    phone = f"1{random.randint(50, 89)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"

    # 邮箱
    email = f"{username}@example.com"

    # 会员等级 (淘宝等级)
    levels = ['心1', '心2', '心3', '心4', '心5', '钻1', '钻2', '钻3', '钻4', '钻5', '冠1', '冠2', '冠3']
    level = random.choice(levels)

    # 昵称 (3-8位，汉字+英文组合)
    nickname_type = random.choice(["chinese", "english", "mix"])
    if nickname_type == "chinese":
        # 纯汉字昵称
        nickname = ''.join(random.choices(common_chars, k=random.randint(3, 8)))
    elif nickname_type == "english":
        # 纯英文昵称
        nickname = ''.join(random.choices(english_words, k=random.randint(1, 2)))
    else:
        # 混合昵称
        chinese_part = ''.join(random.choices(common_chars, k=random.randint(2, 4)))
        english_part = random.choice(english_words)
        nickname = f"{chinese_part}{english_part}"

    # 性别
    gender = random.randint(0, 1)

    # 出生日期 (1950-2010)
    # birth_year = random.randint(1950, 2010)
    # birth_month = random.randint(1, 12)
    # birth_day = random.randint(1, 28)  # 为了方便最多取到28
    # birthday = f"{birth_year}{birth_month:02d}{birth_day:02d}"
    # 自己做的优化,需要引入模块import calendar,去除最大28天的限制
    birth_year = random.randint(1950, 2010)
    birth_month = random.randint(1, 12)
    # 获取当月最大天数（自动处理闰年二月）
    max_day = calendar.monthrange(birth_year, birth_month)[1]
    birth_day = random.randint(1, max_day)
    birthday = f"{birth_year}{birth_month:02d}{birth_day:02d}"

    # 头像URL
    avatar = f"../../images/avatar/avatar.png"

    # 收货地址
    province = random.choice(provinces)
    city = random.choice(cities.get(province, ["未知市"]))
    district = random.choice(districts.get(city, ["未知区"]))
    street = random.choice(streets)
    community = random.choice(communities)
    building = random.randint(1, 30)
    unit = random.randint(1, 5)
    room = random.randint(101, 1500)
    address = f"{province}{city}{district}{street}{community}{building}栋{unit}单元{room}"

    # 账号状态
    status = 0 if random.random() > 0.05 else (1 if random.random() > 0.5 else 2)

    # 注册时间 (最近1年内)
    reg_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
    reg_time = reg_date.strftime("%Y-%m-%d %H:%M:%S")

    # 最后登录时间 (在注册时间之后)
    login_date = reg_date + datetime.timedelta(days=random.randint(0, 30),
                                               hours=random.randint(1, 24))
    login_time = login_date.strftime("%Y-%m-%d %H:%M:%S")

    members.append((
        i,  # 用户ID
        username,  # 用户名
        password,  # 密码
        phone,  # 手机号
        email,  # 邮箱
        level,  # 会员等级
        nickname,  # 昵称
        gender,  # 性别
        birthday,  # 出生日期
        avatar,  # 头像URL
        address,  # 收货地址
        status,  # 账号状态
        reg_time,  # 注册时间
        login_time  # 最后登录时间
    ))

# 导出会员数据
with open('members.py', 'w', encoding='utf-8') as f:
    f.write("members = [\n")
    for member in members:
        f.write(f"    {member},\n")
    f.write("]\n")
