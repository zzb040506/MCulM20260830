# -*- coding: utf-8 -*-
"""66国元数据：ISO3 → {中文名, 英文名, 文化圈zone}。
文化圈遵循 Inglehart-Welzel 标准分类（近似分组）。"""

# 8 文化圈
ZONES = ["北美", "西欧", "拉美", "伊斯兰", "南亚", "儒教东亚", "撒哈拉以南非洲", "正教"]
ZONE_EN = {
    "北美": "North America",
    "西欧": "Western Europe",
    "拉美": "Latin America",
    "伊斯兰": "Islamic",
    "南亚": "South Asia",
    "儒教东亚": "Confucian/East Asia",
    "撒哈拉以南非洲": "Sub-Saharan Africa",
    "正教": "Orthodox",
}
ZONE_COLOR = {
    "北美": "#2E5C8A", "西欧": "#4F8A5B", "拉美": "#D98A2B", "伊斯兰": "#C0504D",
    "南亚": "#7F6BAF", "儒教东亚": "#3A8FB7", "撒哈拉以南非洲": "#8B5A2B", "正教": "#9C6BA0",
}

# ISO3 -> (中文名, 英文名, 文化圈)
COUNTRIES = {
    "AND":("安道尔","Andorra","西欧"), "ARG":("阿根廷","Argentina","拉美"),
    "ARM":("亚美尼亚","Armenia","正教"), "AUS":("澳大利亚","Australia","西欧"),
    "BGD":("孟加拉国","Bangladesh","伊斯兰"), "BOL":("玻利维亚","Bolivia","拉美"),
    "BRA":("巴西","Brazil","拉美"), "CAN":("加拿大","Canada","北美"),
    "CHL":("智利","Chile","拉美"), "CHN":("中国","China","儒教东亚"),
    "COL":("哥伦比亚","Colombia","拉美"), "CYP":("塞浦路斯","Cyprus","正教"),
    "CZE":("捷克","Czechia","西欧"), "DEU":("德国","Germany","西欧"),
    "ECU":("厄瓜多尔","Ecuador","拉美"), "EGY":("埃及","Egypt","伊斯兰"),
    "ETH":("埃塞俄比亚","Ethiopia","撒哈拉以南非洲"), "GBR":("英国","United Kingdom","西欧"),
    "GRC":("希腊","Greece","正教"), "GTM":("危地马拉","Guatemala","拉美"),
    "HKG":("中国香港","Hong Kong","儒教东亚"), "IDN":("印度尼西亚","Indonesia","伊斯兰"),
    "IND":("印度","India","南亚"), "IRN":("伊朗","Iran","伊斯兰"),
    "IRQ":("伊拉克","Iraq","伊斯兰"), "JOR":("约旦","Jordan","伊斯兰"),
    "JPN":("日本","Japan","儒教东亚"), "KAZ":("哈萨克斯坦","Kazakhstan","伊斯兰"),
    "KEN":("肯尼亚","Kenya","撒哈拉以南非洲"), "KGZ":("吉尔吉斯斯坦","Kyrgyzstan","伊斯兰"),
    "KOR":("韩国","South Korea","儒教东亚"), "LBN":("黎巴嫩","Lebanon","伊斯兰"),
    "LBY":("利比亚","Libya","伊斯兰"), "MAC":("中国澳门","Macao","儒教东亚"),
    "MAR":("摩洛哥","Morocco","伊斯兰"), "MDV":("马尔代夫","Maldives","伊斯兰"),
    "MEX":("墨西哥","Mexico","拉美"), "MMR":("缅甸","Myanmar","儒教东亚"),
    "MNG":("蒙古","Mongolia","儒教东亚"), "MYS":("马来西亚","Malaysia","伊斯兰"),
    "NGA":("尼日利亚","Nigeria","撒哈拉以南非洲"), "NIC":("尼加拉瓜","Nicaragua","拉美"),
    "NIR":("北爱尔兰","Northern Ireland","西欧"), "NLD":("荷兰","Netherlands","西欧"),
    "NZL":("新西兰","New Zealand","西欧"), "PAK":("巴基斯坦","Pakistan","伊斯兰"),
    "PER":("秘鲁","Peru","拉美"), "PHL":("菲律宾","Philippines","儒教东亚"),
    "PRI":("波多黎各","Puerto Rico","拉美"), "ROU":("罗马尼亚","Romania","正教"),
    "RUS":("俄罗斯","Russia","正教"), "SGP":("新加坡","Singapore","儒教东亚"),
    "SRB":("塞尔维亚","Serbia","正教"), "SVK":("斯洛伐克","Slovakia","西欧"),
    "THA":("泰国","Thailand","儒教东亚"), "TJK":("塔吉克斯坦","Tajikistan","伊斯兰"),
    "TUN":("突尼斯","Tunisia","伊斯兰"), "TUR":("土耳其","Turkey","伊斯兰"),
    "TWN":("中国台湾","Taiwan","儒教东亚"), "UKR":("乌克兰","Ukraine","正教"),
    "URY":("乌拉圭","Uruguay","拉美"), "USA":("美国","USA","北美"),
    "UZB":("乌兹别克斯坦","Uzbekistan","伊斯兰"), "VEN":("委内瑞拉","Venezuela","拉美"),
    "VNM":("越南","Vietnam","儒教东亚"), "ZWE":("津巴布韦","Zimbabwe","撒哈拉以南非洲"),
}

def zone_of(iso3):
    return COUNTRIES.get(iso3, (iso3, iso3, "其他"))[2]

def name_zh(iso3):
    return COUNTRIES.get(iso3, (iso3, iso3, "其他"))[0]

def name_en(iso3):
    return COUNTRIES.get(iso3, (iso3, iso3, "其他"))[1]
