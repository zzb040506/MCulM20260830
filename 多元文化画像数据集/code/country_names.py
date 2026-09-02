"""国家代码 → 中文名映射(ISO 3166-1 alpha-3)。"""

COUNTRY_CN = {
    'AND': '安道尔', 'ARG': '阿根廷', 'ARM': '亚美尼亚', 'AUS': '澳大利亚',
    'BGD': '孟加拉国', 'BOL': '玻利维亚', 'BRA': '巴西', 'CAN': '加拿大',
    'CHL': '智利', 'CHN': '中国', 'COL': '哥伦比亚', 'CYP': '塞浦路斯',
    'CZE': '捷克', 'DEU': '德国', 'ECU': '厄瓜多尔', 'EGY': '埃及',
    'ETH': '埃塞俄比亚', 'GBR': '英国', 'GRC': '希腊', 'GTM': '危地马拉',
    'HKG': '香港', 'IDN': '印度尼西亚', 'IND': '印度', 'IRN': '伊朗',
    'IRQ': '伊拉克', 'JOR': '约旦', 'JPN': '日本', 'KAZ': '哈萨克斯坦',
    'KEN': '肯尼亚', 'KGZ': '吉尔吉斯斯坦', 'KOR': '韩国', 'LBN': '黎巴嫩',
    'LBY': '利比亚', 'MAC': '澳门', 'MAR': '摩洛哥', 'MDV': '马尔代夫',
    'MEX': '墨西哥', 'MMR': '缅甸', 'MNG': '蒙古', 'MYS': '马来西亚',
    'NGA': '尼日利亚', 'NIC': '尼加拉瓜', 'NIR': '北爱尔兰', 'NLD': '荷兰',
    'NZL': '新西兰', 'PAK': '巴基斯坦', 'PER': '秘鲁', 'PHL': '菲律宾',
    'PRI': '波多黎各', 'ROU': '罗马尼亚', 'RUS': '俄罗斯', 'SGP': '新加坡',
    'SRB': '塞尔维亚', 'SVK': '斯洛伐克', 'THA': '泰国', 'TJK': '塔吉克斯坦',
    'TUN': '突尼斯', 'TUR': '土耳其', 'TWN': '台湾', 'UKR': '乌克兰',
    'URY': '乌拉圭', 'USA': '美国', 'UZB': '乌兹别克斯坦', 'VEN': '委内瑞拉',
    'VNM': '越南', 'ZWE': '津巴布韦',
}


def country_label(code):
    """返回 'CHN(中国)' 格式。"""
    cn = COUNTRY_CN.get(code, code)
    return f'{code}({cn})'


def country_cn(code):
    """返回中文名,未知则返回原代码。"""
    return COUNTRY_CN.get(code, code)
