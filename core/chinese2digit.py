"""
This module provides this app with the ability to convert a number from Chinese to digits.
"""
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
from decimal import getcontext, Decimal

cn_num = {
        '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
        '貮': 2, '两': 2
    }
cn_unit = {
        '十': 10, '拾': 10, '百': 100, '佰': 100, '千': 1000, '仟': 1000, '万': 10000, '萬': 10000,
        '亿': 100000000, '億': 100000000, '兆': 1000000000000
    }


def chinese2digit(chinese_number):
    """中文转数字

    :param chinese_number: 中文字符串
    :return: 数字
    """
    chinese_number = chinese_number.split('点')
    integer = list(chinese_number[0])  # 整数部分
    decimal = list(chinese_number[1]) if len(chinese_number) == 2 else []  # 小数部分
    unit = 0  # 当前单位
    parse = []  # 解析数组
    while integer:
        number = integer.pop()
        if number in cn_unit:
            # 当前字符是单位
            unit = cn_unit.get(number)
            if unit == 10000:
                parse.append('w')  # 万位
                unit = 1
            elif unit == 100000000:
                parse.append('y')  # 亿位
                unit = 1
            elif unit == 1000000000000:  # 兆位
                parse.append('z')
                unit = 1

        else:
            # 当前字符是数字
            dig = cn_num.get(number)
            if unit:
                dig = dig * unit
                unit = 0
            parse.append(dig)

    if unit == 10:  # 处理10-19的数字
        parse.append(10)

    result = 0
    tmp = 0
    while parse:
        number = parse.pop()
        if number == 'w':
            tmp *= 10000
            result += tmp
            tmp = 0
        elif number == 'y':
            tmp *= 100000000
            result += tmp
            tmp = 0
        elif number == 'z':
            tmp *= 1000000000000
            result += tmp
            tmp = 0
        else:
            tmp += number
    result += tmp

    if decimal:
        unit = 0.1
        getcontext().prec = len(decimal)  # 小数精度
        result = Decimal(float(result))
        tmp = Decimal(0)
        for each in decimal:
            dig = cn_num.get(each)
            tmp += Decimal(str(dig)) * Decimal(str(unit))
            unit *= 0.1
        getcontext().prec = len(result.to_eng_string()) + len(decimal)  # 完整精度
        result += tmp
    return result

# ————————————————
# 版权声明：本文为CSDN博主「XerCis」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/lly1122334/article/details/107004681
