def meihuaByNumber(number: str):

    if not number.isdigit():
        raise ValueError("参数 number 必须为数字")

    # 计算上卦、下卦和动爻
    if len(number) == 2:
        # 两位：第一位为上卦，第二位为下卦，两位之余 6 则为动爻
        upper = int(number[0])
        lower = int(number[1])
        moving_line = int(number) % 6
    elif len(number) == 3:
        # 三位：第一位为上卦，第二位为下卦，第三位为动爻
        upper = int(number[0])
        lower = int(number[1])
        moving_line = int(number[2])
    else:
        # 四位、五位、六位：前一半为上卦，后一半为下卦，所有数之和为动爻
        mid = len(number) // 2
        upper_part = number[:mid]
        lower_part = number[mid:]
        upper = sum(int(number) for d in upper_part)
        lower = sum(int(d) for d in lower_part)
        moving_line = sum(int(d) for d in number)

    # 八卦对应（按先天八卦数：乾 1、兑 2、离 3、震 4、巽 5、坎 6、艮 7、坤 8）
    bagua = {
        1: "乾☰",
        2: "兑☱",
        3: "离☲",
        4: "震☳",
        5: "巽☴",
        6: "坎☵",
        7: "艮☶",
        8: "坤☷"
    }

    # 处理卦数（取模 8，余数为 0 则为 8）
    upper_gua = (upper - 1) % 8 + 1
    lower_gua = (lower - 1) % 8 + 1
    moving_line_gua = (moving_line - 1) % 6 + 1

    upper_name = bagua.get(upper_gua, "未知")
    lower_name = bagua.get(lower_gua, "未知")

    # 提取纯卦名（去掉符号）
    def extract_gua_name(name_with_symbol):
        return name_with_symbol[0]

    upper_pure = extract_gua_name(upper_name)
    lower_pure = extract_gua_name(lower_name)

    # 构建完整的六爻卦象（从初爻到上爻）
    # 先天八卦的爻象表示（1 表示阳爻，0 表示阴爻）
    bagua_yao = {
        1: [1, 1, 1],  # 乾☰
        2: [1, 1, 0],  # 兑☱
        3: [1, 0, 1],  # 离☲
        4: [1, 0, 0],  # 震☳
        5: [0, 1, 1],  # 巽☴
        6: [0, 1, 0],  # 坎☵
        7: [0, 0, 1],  # 艮☶
        8: [0, 0, 0]  # 坤☷
    }

    # 获取上下卦的爻象
    upper_yao = bagua_yao[upper_gua]
    lower_yao = bagua_yao[lower_gua]

    # 完整的六爻卦象（从下到上：初爻、二爻、三爻、四爻、五爻、上爻）
    full_yao = lower_yao + upper_yao

    # 生成本卦
    ben_gua_name = G64(upper_pure, lower_pure)

    # 生成互卦（取本卦的 234 爻为下卦，345 爻为上卦）
    # 注意：full_yao 索引 0=初爻，1=二爻，2=三爻，3=四爻，4=五爻，5=上爻
    hu_lower_yao = [full_yao[1], full_yao[2], full_yao[3]]  # 2、3、4 爻
    hu_upper_yao = [full_yao[2], full_yao[3], full_yao[4]]  # 3、4、5 爻

    # 根据爻象确定互卦的上下卦
    def yao_to_gua(yao):
        """将三爻转换为八卦数字"""
        for gua_num, yao_list in bagua_yao.items():
            if yao_list == yao:
                return gua_num
        return 1  # 默认乾卦

    hu_upper_gua = yao_to_gua(hu_upper_yao)
    hu_lower_gua = yao_to_gua(hu_lower_yao)
    hu_upper_name = bagua.get(hu_upper_gua, "未知")
    hu_lower_name = bagua.get(hu_lower_gua, "未知")
    hu_gua_name = G64(hu_upper_name[0], hu_lower_name[0])

    # 生成变卦（动爻变化）
    # 动爻在第几爻就变化那一爻的阴阳
    # moving_line_gua 范围是 1-6，对应索引 0-5
    yao_index = moving_line_gua - 1
    changed_yao = full_yao.copy()
    changed_yao[yao_index] = 1 - changed_yao[yao_index]  # 阴阳互换：1 变 0，0 变 1

    # 分离变卦的上下卦
    bian_lower_yao = changed_yao[:3]
    bian_upper_yao = changed_yao[3:]

    # 根据爻象确定变卦的上下卦
    bian_upper_gua = yao_to_gua(bian_upper_yao)
    bian_lower_gua = yao_to_gua(bian_lower_yao)
    bian_upper_name = bagua.get(bian_upper_gua, "未知")
    bian_lower_name = bagua.get(bian_lower_gua, "未知")
    bian_gua_name = G64(bian_upper_name[0], bian_lower_name[0])

    # 生成综卦（将本卦倒过来看，旋转 180 度）
    # 初爻变上爻，二爻变五爻，三爻变四爻，四爻变三爻，五爻变二爻，上爻变初爻
    zong_yao = full_yao[::-1]  # 将整个六爻反转
    zong_lower_yao = zong_yao[:3]  # 新的下卦（原上卦的反转）
    zong_upper_yao = zong_yao[3:]  # 新的上卦（原下卦的反转）

    # 根据爻象确定综卦的上下卦
    zong_upper_gua = yao_to_gua(zong_upper_yao)
    zong_lower_gua = yao_to_gua(zong_lower_yao)
    zong_upper_name = bagua.get(zong_upper_gua, "未知")
    zong_lower_name = bagua.get(zong_lower_gua, "未知")
    zong_gua_name = G64(zong_upper_name[0], zong_lower_name[0])

    # 生成错卦（将本卦每个爻阴阳互换）
    cuo_yao = [1 - y for y in full_yao]  # 所有爻阴阳互换
    cuo_lower_yao = cuo_yao[:3]
    cuo_upper_yao = cuo_yao[3:]

    # 根据爻象确定错卦的上下卦
    cuo_upper_gua = yao_to_gua(cuo_upper_yao)
    cuo_lower_gua = yao_to_gua(cuo_lower_yao)
    cuo_upper_name = bagua.get(cuo_upper_gua, "未知")
    cuo_lower_name = bagua.get(cuo_lower_gua, "未知")
    cuo_gua_name = G64(cuo_upper_name[0], cuo_lower_name[0])

    # 确定体用（根据动爻位置）
    # 动爻在 1-3 爻，下卦为用，上卦为体
    # 动爻在 4-6 爻，上卦为用，下卦为体
    ti_label = "体" if moving_line_gua <= 3 else "用"
    yong_label = "用" if moving_line_gua <= 3 else "体"

    result = f"{ti_label} {upper_name} {hu_upper_name} {bian_upper_name} {zong_upper_name} {cuo_upper_name}\n"
    result += f"{yong_label} {lower_name} {hu_lower_name} {bian_lower_name} {zong_lower_name} {cuo_lower_name}\n"
    result += f"动爻：第{moving_line_gua}爻\n"
    result += f"本卦：{ben_gua_name}\n"
    result += f"互卦：{hu_gua_name}\n"
    result += f"变卦：{bian_gua_name}\n"
    result += f"错卦：{cuo_gua_name}\n"
    result += f"综卦：{zong_gua_name}\n"

    return result

# x为上，y为下
def G64(x, y):
    # 乾卦
    if x == '乾' and y == '乾':
        return '乾为天'
    elif x == '乾' and y == '兑':
        return '天泽履'
    elif x == '乾' and y == '离':
        return '天火同人'
    elif x == '乾' and y == '震':
        return '天雷无妄'
    elif x == '乾' and y == '巽':
        return '天风姤'
    elif x == '乾' and y == '坎':
        return '天水讼'
    elif x == '乾' and y == '艮':
        return '天山遁'
    elif x == '乾' and y == '坤':
        return '天地否'

    # 兑卦
    elif x == '兑' and y == '乾':
        return '泽天夬'
    elif x == '兑' and y == '兑':
        return '兑为泽'
    elif x == '兑' and y == '离':
        return '泽火革'
    elif x == '兑' and y == '震':
        return '泽雷随'
    elif x == '兑' and y == '巽':
        return '泽风大过'
    elif x == '兑' and y == '坎':
        return '泽水困'
    elif x == '兑' and y == '艮':
        return '泽山咸'
    elif x == '兑' and y == '坤':
        return '泽地萃'

    # 离卦
    elif x == '离' and y == '乾':
        return '火天大有'
    elif x == '离' and y == '兑':
        return '火泽睽'
    elif x == '离' and y == '离':
        return '离为火'
    elif x == '离' and y == '震':
        return '火雷噬嗑'
    elif x == '离' and y == '巽':
        return '火风鼎'
    elif x == '离' and y == '坎':
        return '火水未济'
    elif x == '离' and y == '艮':
        return '火山旅'
    elif x == '离' and y == '坤':
        return '火地晋'

    # 震卦
    elif x == '震' and y == '乾':
        return '雷天大壮'
    elif x == '震' and y == '兑':
        return '雷泽归妹'
    elif x == '震' and y == '离':
        return '雷火丰'
    elif x == '震' and y == '震':
        return '震为雷'
    elif x == '震' and y == '巽':
        return '雷风恒'
    elif x == '震' and y == '坎':
        return '雷水解'
    elif x == '震' and y == '艮':
        return '雷山小过'
    elif x == '震' and y == '坤':
        return '雷地豫'

    # 巽卦
    elif x == '巽' and y == '乾':
        return '风天小畜'
    elif x == '巽' and y == '兑':
        return '风泽中孚'
    elif x == '巽' and y == '离':
        return '风火家人'
    elif x == '巽' and y == '震':
        return '风雷益'
    elif x == '巽' and y == '巽':
        return '巽为风'
    elif x == '巽' and y == '坎':
        return '风水涣'
    elif x == '巽' and y == '艮':
        return '风山渐'
    elif x == '巽' and y == '坤':
        return '风地观'

    # 坎卦
    elif x == '坎' and y == '乾':
        return '水天需'
    elif x == '坎' and y == '兑':
        return '水泽节'
    elif x == '坎' and y == '离':
        return '水火既济'
    elif x == '坎' and y == '震':
        return '水雷屯'
    elif x == '坎' and y == '巽':
        return '水风井'
    elif x == '坎' and y == '坎':
        return '坎为水'
    elif x == '坎' and y == '艮':
        return '水山蹇'
    elif x == '坎' and y == '坤':
        return '水地比'

    # 艮卦
    elif x == '艮' and y == '乾':
        return '山天大畜'
    elif x == '艮' and y == '兑':
        return '山泽损'
    elif x == '艮' and y == '离':
        return '山火贲'
    elif x == '艮' and y == '震':
        return '山雷颐'
    elif x == '艮' and y == '巽':
        return '山风蛊'
    elif x == '艮' and y == '坎':
        return '山水蒙'
    elif x == '艮' and y == '艮':
        return '艮为山'
    elif x == '艮' and y == '坤':
        return '山地剥'

    # 坤卦
    elif x == '坤' and y == '乾':
        return '地天泰'
    elif x == '坤' and y == '兑':
        return '地泽临'
    elif x == '坤' and y == '离':
        return '地火明夷'
    elif x == '坤' and y == '震':
        return '地雷复'
    elif x == '坤' and y == '巽':
        return '地风升'
    elif x == '坤' and y == '坎':
        return '地水师'
    elif x == '坤' and y == '艮':
        return '地山谦'
    else:
        return '坤为地'

