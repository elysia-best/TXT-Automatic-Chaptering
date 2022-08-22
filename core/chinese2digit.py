from decimal import *


def chinese2digit(cn):
    """中文转数字

    :param cn: 中文字符串
    :return: 数字
    >>> chinese2digit('十一')
    11
    >>> chinese2digit('九万八千零七十六点五四三二一')
    Decimal('98076.54321')
    """
    CN_NUM = {
        '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
        '貮': 2, '两': 2
    }
    CN_UNIT = {
        '十': 10, '拾': 10, '百': 100, '佰': 100, '千': 1000, '仟': 1000, '万': 10000, '萬': 10000,
        '亿': 100000000, '億': 100000000, '兆': 1000000000000
    }

    cn = cn.split('点')
    integer = list(cn[0])  # 整数部分
    decimal = list(cn[1]) if len(cn) == 2 else []  # 小数部分
    unit = 0  # 当前单位
    parse = []  # 解析数组
    while integer:
        x = integer.pop()
        if x in CN_UNIT:
            # 当前字符是单位
            unit = CN_UNIT.get(x)
            if unit == 10000:
                parse.append('w')  # 万位
                unit = 1
            elif unit == 100000000:
                parse.append('y')  # 亿位
                unit = 1
            elif unit == 1000000000000:  # 兆位
                parse.append('z')
                unit = 1
            continue
        else:
            # 当前字符是数字
            dig = CN_NUM.get(x)
            if unit:
                dig = dig * unit
                unit = 0
            parse.append(dig)

    if unit == 10:  # 处理10-19的数字
        parse.append(10)

    result = 0
    tmp = 0
    while parse:
        x = parse.pop()
        if x == 'w':
            tmp *= 10000
            result += tmp
            tmp = 0
        elif x == 'y':
            tmp *= 100000000
            result += tmp
            tmp = 0
        elif x == 'z':
            tmp *= 1000000000000
            result += tmp
            tmp = 0
        else:
            tmp += x
    result += tmp

    if decimal:
        unit = 0.1
        getcontext().prec = len(decimal)  # 小数精度
        result = Decimal(float(result))
        tmp = Decimal(0)
        for x in decimal:
            dig = CN_NUM.get(x)
            tmp += Decimal(str(dig)) * Decimal(str(unit))
            unit *= 0.1
        getcontext().prec = len(result.to_eng_string()) + len(decimal)  # 完整精度
        result += tmp
    return result

# ————————————————
# 版权声明：本文为CSDN博主「XerCis」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/lly1122334/article/details/107004681
