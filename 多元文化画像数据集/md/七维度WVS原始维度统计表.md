# 七维度 WVS 原始维度统计表

> 依据《多元文化画像构建方案V2.md》第二节“七维度变量映射表”枚举的 WVS 原始变量,对 CSV 原始数据(不归一化 / 不 log 变换 / 不做特征工程)计算描述统计,保留 WVS 原始取值。

> 缺失处理:负数(-1/-2/-3/-4/-5)与空值均视为缺失;均值/标准差仅对有效值计算。

> 样本总量: **97,220** 人。


## 维度1 地区/地理


| 子维度 | 变量 | Label(codebook 原文) | 类型 | 有效N | 均值 | 标准差 | 最小值 | 最大值 | 缺失率(%) |
|---|---|---|---|---|---|---|---|---|---|
| 国家(ISO-3) | `B_COUNTRY_ALPHA` | ISO 3166-1 alpha-3 country code | 分类 | 97,220 | 类别数=66; 众数(CAN=4018; IDN=3200; CHN=3036) | — | — | — | 0.00 |
| 国家(数字) | `B_COUNTRY` | ISO 3166-1 numeric country code | 分类 | 97,220 | 类别数=66; 众数(124=4018; 360=3200; 156=3036) | — | — | — | 0.00 |
| 国内区域 ISO | `N_REGION_ISO` | Region ISO 3166-2 | 分类 | 94,729 | 类别数=1303; 众数(360001=1700; 586004=1139; 446001=1023) | — | — | — | 2.56 |
| 国内区域 WVS | `N_REGION_WVS` | Region country specific | 分类 | 89,157 | 类别数=941; 众数(360021=1700; 586010=1139; 446001=1023) | — | — | — | 8.29 |
| NUTS-2 区域 | `N_REGION_NUTS2` | Region NUTS-2 | 分类 | 13,786 | 类别数=122; 众数(6430101=489; 3000001=430; 5280303=413) | — | — | — | 85.82 |
| 城乡 | `H_URBRURAL` | Urban-Rural | 二值 | 97,183 | 1.322 | 0.467 | 1.000 | 2.000 | 0.04 |
| 城镇规模 | `G_TOWNSIZE` | Settlement size_8 groups | 分类 | 95,941 | 类别数=8; 众数(8=24598; 7=16761; 5=11275) | — | — | — | 1.32 |
| 城镇规模(5组) | `G_TOWNSIZE2` | Settlement size_5 groups | 分类 | 95,941 | 类别数=5; 众数(5=24409; 3=20723; 1=19264) | — | — | — | 1.32 |
| 定居点类型 | `H_SETTLEMENT` | Settlement type | 分类 | 97,008 | 类别数=5; 众数(5=25998; 1=19685; 2=18921) | — | — | — | 0.22 |
| 经度 | `O1_LONGITUDE` | Geographical Coordinates - Longitude | 连续/有序 | 52,959 | 64.240 | 37.836 | 0.000 | 156.890 | 45.53 |
| 纬度 | `O2_LATITUDE` | Geographical Coordinates - Latitude | 连续/有序 | 60,085 | 30.257 | 16.253 | 0.000 | 100.350 | 38.20 |

## 维度2 语言


| 子维度 | 变量 | Label(codebook 原文) | 类型 | 有效N | 均值 | 标准差 | 最小值 | 最大值 | 缺失率(%) |
|---|---|---|---|---|---|---|---|---|---|
| 访谈语言 | `S_INTLANGUAGE` | Language in which interview was conducted | 分类 | 97,220 | 类别数=53; 众数(1270=16190; 1240=15250; 170=8407) | — | — | — | 0.00 |
| 访谈语言 ISO | `LNGE_ISO` | Language in which interview was conducted  (ISO 639-1 Alpha 2 digit) | 分类 | 97,220 | 类别数=52; 众数(es=16190; en=15248; ar=8407) | — | — | — | 0.00 |
| 家庭语言 | `Q272` | Language at home | 分类 | 94,500 | 类别数=169; 众数(1270=15659; 1240=12003; 170=6844) | — | — | — | 2.80 |

## 维度3 价值观


| 子维度 | 变量 | Label(codebook 原文) | 类型 | 有效N | 均值 | 标准差 | 最小值 | 最大值 | 缺失率(%) |
|---|---|---|---|---|---|---|---|---|---|
| 世俗-传统(主轴) | `SACSECVAL` | SACSECVAL.- Welzel Overall | 连续/有序 | 96,740 | 0.366 | 0.178 | 0.000 | 1.000 | 0.49 |
| 生存-自我表达(主轴) | `RESEMAVAL` | RESEMAVAL.- Welzel | 连续/有序 | 96,472 | 0.436 | 0.182 | 0.000 | 1.000 | 0.77 |
| 权威服从 | `I_AUTHORITY` | AUTHORITY - Welzel | 连续/有序 | 94,496 | 0.288 | 0.374 | 0.000 | 1.000 | 2.80 |
| 民族主义 | `I_NATIONALISM` | NATIONALISM - Welzel | 连续/有序 | 94,132 | 0.181 | 0.248 | 0.000 | 1.000 | 3.18 |
| 虔诚度 | `I_DEVOUT` | DEVOUT- Welzel defiance - 3: | 连续/有序 | 95,544 | 0.215 | 0.246 | 0.000 | 1.000 | 1.72 |
| 自主性(合成) | `AUTONOMY` | AUTONOMY.- Wezel | 连续/有序 | 96,006 | 0.446 | 0.300 | 0.000 | 1.000 | 1.25 |
| 平等观(合成) | `EQUALITY` | Emancipative Values-2: | 连续/有序 | 96,342 | 0.576 | 0.258 | 0.000 | 1.000 | 0.90 |
| 选择自由(合成) | `CHOICE` | CHOICE.- Welzel choice sub- | 连续/有序 | 95,255 | 0.353 | 0.303 | 0.000 | 1.000 | 2.02 |
| 发声倾向(合成) | `VOICE` | VOICE.- Welzel voice sub- | 连续/有序 | 95,206 | 0.368 | 0.285 | 0.000 | 1.000 | 2.07 |
| 认识论怀疑 | `DEFIANCE` | DEFIANCE.- Welzel defiance | 连续/有序 | 96,653 | 0.233 | 0.199 | 0.000 | 1.000 | 0.58 |
| 不信教 | `DISBELIEF` | DISBELIEF.- Welzel disbelief | 连续/有序 | 96,520 | 0.417 | 0.337 | 0.000 | 1.014 | 0.72 |
| 相对主义 | `RELATIVISM` | RELATIVISM.- Welzel | 连续/有序 | 96,257 | 0.388 | 0.404 | 0.000 | 1.000 | 0.99 |
| 怀疑主义 | `SCEPTICISM` | SCEPTICISM.- Welzel | 连续/有序 | 94,837 | 0.429 | 0.255 | 0.000 | 1.000 | 2.45 |
| 信任军队 | `I_TRUSTARMY` | TRUSTARMY- Welzel | 连续/有序 | 92,897 | 0.367 | 0.310 | 0.000 | 1.000 | 4.45 |
| 信任警察 | `I_TRUSTPOLICE` | TRUSTPOLICE- Welzel | 连续/有序 | 94,808 | 0.446 | 0.311 | 0.000 | 1.000 | 2.48 |
| 信任法院 | `I_TRUSTCOURTS` | TRUSTCOURTS- Welzel | 连续/有序 | 93,709 | 0.471 | 0.313 | 0.000 | 1.000 | 3.61 |
| 规范1 | `I_NORM1` | NORM1 - Welzel relativism- 1: | 连续/有序 | 93,681 | 0.484 | 0.500 | 0.000 | 1.000 | 3.64 |
| 规范2 | `I_NORM2` | NORM2 - Welzel relativism- 2: | 连续/有序 | 95,941 | 0.371 | 0.483 | 0.000 | 1.000 | 1.32 |
| 规范3 | `I_NORM3` | NORM3 - Welzel relativism- 3: | 连续/有序 | 96,026 | 0.308 | 0.462 | 0.000 | 1.000 | 1.23 |
| 后物质主义12项 | `Y001` | Post-Materialist index 12-item Y001_1: | 连续/有序 | 91,274 | 2.064 | 1.198 | 0.000 | 5.000 | 6.12 |
| 后物质主义4项 | `Y002` | Post-Materialist index 4-item | 连续/有序 | 93,417 | 1.814 | 0.613 | 1.000 | 3.000 | 3.91 |
| 自主指数 | `Y003` | Autonomy Index | 连续/有序 | 66,552 | 0.727 | 0.702 | 0.000 | 2.000 | 31.55 |

## 维度4 社会规范


| 子维度 | 变量 | Label(codebook 原文) | 类型 | 有效N | 均值 | 标准差 | 最小值 | 最大值 | 缺失率(%) |
|---|---|---|---|---|---|---|---|---|---|
| 信任半径-通用信任 | `Q57P` | Most people can be trusted | 连续/有序 | 95,883 | 1.243 | 0.429 | 1.000 | 2.000 | 1.38 |
| 信任半径-信任家人 | `Q58P` | How much you trust: Your family | 连续/有序 | 96,888 | 3.727 | 0.566 | 1.000 | 4.000 | 0.34 |
| 信任半径-信任邻里 | `Q59P` | Trust: Your neighborhood | 连续/有序 | 96,393 | 2.818 | 0.798 | 1.000 | 4.000 | 0.85 |
| 信任半径-信任熟人 | `Q60P` | Trust: People you know personally | 连续/有序 | 96,635 | 2.942 | 0.796 | 1.000 | 4.000 | 0.60 |
| 信任半径-信任陌生人 | `Q61P` | Trust: People you meet for the first time | 连续/有序 | 95,859 | 1.991 | 0.811 | 1.000 | 4.000 | 1.40 |
| 信任半径-信任异教徒 | `Q62P` | Trust: People of another religion | 连续/有序 | 93,144 | 2.315 | 0.868 | 1.000 | 4.000 | 4.19 |
| 信任半径-信任外国人 | `Q63P` | Trust: People of another nationality | 连续/有序 | 93,142 | 2.210 | 0.875 | 1.000 | 4.000 | 4.20 |
| 机构信任-宗教组织 | `Q64P` | Confidence: Churches | 连续/有序 | 95,184 | 2.806 | 1.001 | 1.000 | 4.000 | 2.09 |
| 机构信任-军队 | `Q65P` | Confidence: Armed Forces | 连续/有序 | 92,897 | 2.890 | 0.934 | 1.000 | 4.000 | 4.45 |
| 机构信任-报刊 | `Q66P` | Confidence: The Press | 连续/有序 | 95,010 | 2.292 | 0.872 | 1.000 | 4.000 | 2.27 |
| 机构信任-电视 | `Q67P` | Confidence: Television | 连续/有序 | 95,772 | 2.366 | 0.869 | 1.000 | 4.000 | 1.49 |
| 机构信任-工会 | `Q68P` | Confidence: Labor Unions | 连续/有序 | 89,965 | 2.295 | 0.886 | 1.000 | 4.000 | 7.46 |
| 机构信任-警察 | `Q69P` | Confidence: The Police | 连续/有序 | 94,808 | 2.654 | 0.936 | 1.000 | 4.000 | 2.48 |
| 机构信任-法院 | `Q70P` | Confidence: Justice System/Courts | 连续/有序 | 93,709 | 2.578 | 0.940 | 1.000 | 4.000 | 3.61 |
| 机构信任-政府 | `Q71P` | Confidence: The Government | 连续/有序 | 94,083 | 2.376 | 0.988 | 1.000 | 4.000 | 3.23 |
| 机构信任-政党 | `Q72P` | Confidence: The Political Parties | 连续/有序 | 93,915 | 2.030 | 0.892 | 1.000 | 4.000 | 3.40 |
| 机构信任-议会 | `Q73P` | Confidence: Parliament | 连续/有序 | 93,741 | 2.199 | 0.945 | 1.000 | 4.000 | 3.58 |
| 机构信任-公务员 | `Q74P` | Confidence: The Civil Services | 连续/有序 | 93,883 | 2.435 | 0.887 | 1.000 | 4.000 | 3.43 |
| 机构信任-大学 | `Q75P` | Confidence: Universities | 连续/有序 | 93,295 | 2.852 | 0.845 | 1.000 | 4.000 | 4.04 |
| 机构信任-选举 | `Q76P` | Confidence: Election | 连续/有序 | 93,400 | 2.404 | 0.953 | 1.000 | 4.000 | 3.93 |
| 机构信任-大企业 | `Q77P` | Confidence: Major Companies | 连续/有序 | 91,853 | 2.385 | 0.845 | 1.000 | 4.000 | 5.52 |
| 机构信任-银行 | `Q78P` | Confidence: Banks | 连续/有序 | 94,353 | 2.580 | 0.922 | 1.000 | 4.000 | 2.95 |
| 机构信任-环保运动 | `Q79P` | Confidence: The Environmental Protection Movement | 连续/有序 | 90,776 | 2.622 | 0.880 | 1.000 | 4.000 | 6.63 |
| 机构信任-妇女运动 | `Q80P` | Confidence: The Women´s Movement | 连续/有序 | 88,635 | 2.677 | 0.872 | 1.000 | 4.000 | 8.83 |
| 机构信任-慈善组织 | `Q81P` | Confidence: Charitable or humanitarian organizations | 连续/有序 | 91,480 | 2.705 | 0.884 | 1.000 | 4.000 | 5.90 |
| 机构信任-区域组织 | `Q82P` | Confidence: Major regional organization (combined from country-specific) | 连续/有序 | 75,682 | 2.344 | 0.912 | 1.000 | 4.000 | 22.15 |
| 机构信任-联合国 | `Q83P` | Confidence: The United Nations (UN) | 连续/有序 | 83,399 | 2.428 | 0.938 | 1.000 | 4.000 | 14.22 |
| 机构信任-IMF | `Q84P` | Confidence: International Monetary Found (IMF) | 连续/有序 | 78,457 | 2.295 | 0.911 | 1.000 | 4.000 | 19.30 |
| 机构信任-ICC | `Q85P` | Confidence: International Criminal Court (ICC) | 连续/有序 | 77,597 | 2.385 | 0.915 | 1.000 | 4.000 | 20.18 |
| 机构信任-NATO | `Q86P` | Confidence: North Atlantic Treaty Organization (NATO) | 连续/有序 | 72,041 | 2.255 | 0.912 | 1.000 | 4.000 | 25.90 |
| 机构信任-世界银行 | `Q87P` | Confidence: The World Bank (WB) | 连续/有序 | 77,995 | 2.398 | 0.937 | 1.000 | 4.000 | 19.77 |
| 机构信任-WHO | `Q88P` | Confidence: The World Health Organization (WHO) | 连续/有序 | 81,371 | 2.700 | 0.918 | 1.000 | 4.000 | 16.30 |
| 机构信任-WTO | `Q89P` | Confidence: The World Trade Organization (WTO) | 连续/有序 | 75,977 | 2.426 | 0.901 | 1.000 | 4.000 | 21.85 |
| 伦理弹性-骗福利 | `Q177` | Justifiable: Claiming government benefits to which you are not entitled | 连续/有序 | 95,532 | 2.973 | 2.672 | 1.000 | 10.000 | 1.74 |
| 伦理弹性-逃票 | `Q178` | Justifiable: Avoiding a fare on public transport | 连续/有序 | 93,681 | 2.842 | 2.578 | 1.000 | 10.000 | 3.64 |
| 伦理弹性-偷窃 | `Q179` | Justifiable: Stealing property | 连续/有序 | 96,315 | 1.818 | 1.791 | 1.000 | 10.000 | 0.93 |
| 伦理弹性-逃税 | `Q180` | Justifiable: Cheating on taxes | 连续/有序 | 95,941 | 2.234 | 2.154 | 1.000 | 10.000 | 1.32 |
| 伦理弹性-受贿 | `Q181` | Justifiable: Someone accepting a bribe in the course of their duties | 连续/有序 | 96,026 | 1.966 | 1.917 | 1.000 | 10.000 | 1.23 |
| 伦理弹性-同性恋 | `Q182` | Justifiable: Homosexuality | 连续/有序 | 89,705 | 4.052 | 3.408 | 1.000 | 10.000 | 7.73 |
| 伦理弹性-卖淫 | `Q183` | Justifiable: Prostitution | 连续/有序 | 88,469 | 3.050 | 2.684 | 1.000 | 10.000 | 9.00 |
| 伦理弹性-堕胎 | `Q184` | Justifiable: Abortion | 连续/有序 | 94,945 | 3.554 | 2.989 | 1.000 | 10.000 | 2.34 |
| 伦理弹性-离婚 | `Q185` | Justifiable: Divorce | 连续/有序 | 95,291 | 5.007 | 3.202 | 1.000 | 10.000 | 1.98 |
| 伦理弹性-婚前性 | `Q186` | Justifiable: Sex before marriage | 连续/有序 | 92,406 | 4.655 | 3.435 | 1.000 | 10.000 | 4.95 |
| 伦理弹性-自杀 | `Q187` | Justifiable: Suicide | 连续/有序 | 94,854 | 2.581 | 2.440 | 1.000 | 10.000 | 2.43 |
| 伦理弹性-安乐死 | `Q188` | Justifiable: Euthanasia | 连续/有序 | 93,246 | 3.882 | 3.175 | 1.000 | 10.000 | 4.09 |
| 伦理弹性-家暴 | `Q189` | Justifiable: For a man to beat his wife | 连续/有序 | 93,144 | 1.858 | 1.867 | 1.000 | 10.000 | 4.19 |
| 伦理弹性-体罚孩子 | `Q190` | Justifiable: Parents beating children | 连续/有序 | 96,186 | 2.832 | 2.538 | 1.000 | 10.000 | 1.06 |
| 伦理弹性-暴力 | `Q191` | Justifiable: Violence against other people | 连续/有序 | 96,198 | 1.961 | 1.858 | 1.000 | 10.000 | 1.05 |
| 伦理弹性-恐怖主义 | `Q192` | Justifiable: Terrorism as a political, ideological or religious mean | 连续/有序 | 92,697 | 1.789 | 1.794 | 1.000 | 10.000 | 4.65 |
| 伦理弹性-随便性行为 | `Q193` | Justifiable: Having casual sex | 连续/有序 | 89,470 | 3.556 | 3.041 | 1.000 | 10.000 | 7.97 |
| 伦理弹性-政治暴力 | `Q194` | Justifiable: Political violence | 连续/有序 | 92,427 | 1.987 | 1.920 | 1.000 | 10.000 | 4.93 |
| 伦理弹性-死刑 | `Q195` | Justifiable: Death penalty | 连续/有序 | 94,751 | 4.098 | 3.183 | 1.000 | 10.000 | 2.54 |
| 工作伦理-不工作者变懒 | `Q39P` | People who don´t work turn lazy | 连续/有序 | 96,272 | 3.801 | 1.123 | 1.000 | 5.000 | 0.97 |
| 工作伦理-工作是社会义务 | `Q40P` | Work is a duty towards society | 连续/有序 | 96,368 | 3.828 | 1.032 | 1.000 | 5.000 | 0.88 |
| 工作伦理-工作优先于闲暇 | `Q41P` | Work should  always come first even if it means less spare time | 连续/有序 | 96,430 | 3.465 | 1.189 | 1.000 | 5.000 | 0.81 |
| 工作伦理-收入平等vs激励 | `Q106` | Income equality vs larger income differences | 连续/有序 | 95,851 | 6.282 | 2.987 | 1.000 | 10.000 | 1.41 |
| 工作伦理-私有vs国有 | `Q107` | Private vs state ownership of business | 连续/有序 | 93,776 | 5.647 | 2.828 | 1.000 | 10.000 | 3.54 |
| 工作伦理-政府vs个人责任 | `Q108` | Government´s vs individual´s responsibility | 连续/有序 | 96,042 | 5.028 | 3.009 | 1.000 | 10.000 | 1.21 |
| 工作伦理-竞争观 | `Q109` | Competition good or harmful | 连续/有序 | 95,558 | 4.065 | 2.735 | 1.000 | 10.000 | 1.71 |
| 工作伦理-成功归因 | `Q110` | Success: hard work vs luck | 连续/有序 | 95,779 | 4.462 | 2.935 | 1.000 | 10.000 | 1.48 |
| 工作伦理-环境vs增长 | `Q111` | Protecting environment vs. Economic growth | 连续/有序 | 92,569 | 1.460 | 0.557 | 1.000 | 3.000 | 4.78 |
| 政府权力-公共监控 | `Q196P` | Government has the right: Keep people under video surveillance in public areas | 连续/有序 | 93,834 | 2.731 | 1.096 | 1.000 | 4.000 | 3.48 |
| 政府权力-监控通讯 | `Q197P` | Government has the right: Monitor all e-mails and any other information | 连续/有序 | 92,882 | 2.101 | 1.066 | 1.000 | 4.000 | 4.46 |
| 政府权力-收集信息 | `Q198P` | Government has the right: Collect information about anyone living in this | 连续/有序 | 93,264 | 2.045 | 1.074 | 1.000 | 4.000 | 4.07 |

## 维度5 关系结构


| 子维度 | 变量 | Label(codebook 原文) | 类型 | 有效N | 均值 | 标准差 | 最小值 | 最大值 | 缺失率(%) |
|---|---|---|---|---|---|---|---|---|---|
| 家庭结构-婚姻状况 | `Q273` | Marital status | 连续/有序 | 96,631 | 2.665 | 2.147 | 1.000 | 6.000 | 0.61 |
| 家庭结构-子女数 | `Q274` | How many children do you have | 连续/有序 | 92,364 | 1.772 | 1.720 | 0.000 | 24.000 | 5.00 |
| 家庭结构-家庭规模 | `Q270` | Number of people in household | 连续/有序 | 96,235 | 4.025 | 2.569 | 1.000 | 63.000 | 1.01 |
| 家庭结构-与父母同住 | `Q271` | Do you live with your parents | 二值 | 94,956 | 1.353 | 0.600 | 1.000 | 4.000 | 2.33 |
| 家庭结构-家庭重要性 | `Q1P` | Important in life: Family | 连续/有序 | 97,065 | 3.887 | 0.365 | 1.000 | 4.000 | 0.16 |
| 家庭结构-朋友重要性 | `Q2P` | Important in life: Friends | 连续/有序 | 96,908 | 3.291 | 0.744 | 1.000 | 4.000 | 0.32 |
| 家庭结构-闲暇重要性 | `Q3P` | Important in life: Leisure time | 连续/有序 | 96,685 | 3.215 | 0.787 | 1.000 | 4.000 | 0.55 |
| 移民背景-本人移民 | `Q263` | Respondent immigrant | 二值 | 96,836 | 1.058 | 0.235 | 1.000 | 2.000 | 0.40 |
| 移民背景-母亲移民 | `Q264` | Mother immigrant | 二值 | 92,539 | 1.097 | 0.296 | 1.000 | 2.000 | 4.82 |
| 移民背景-父亲移民 | `Q265` | Father immigrant | 二值 | 92,341 | 1.100 | 0.300 | 1.000 | 2.000 | 5.02 |
| 移民背景-本人出生国 | `Q266` | Country of birth: Respondent | 分类 | 93,829 | 类别数=154; 众数(124=3329; 360=3256; 826=3052) | — | — | — | 3.49 |
| 移民背景-母亲出生国 | `Q267` | Country of birth: Mother of the respondent | 分类 | 89,761 | 类别数=159; 众数(360=3304; 124=2832; 792=2734) | — | — | — | 7.67 |
| 移民背景-父亲出生国 | `Q268` | Country of birth: Father of the respondent | 分类 | 89,637 | 类别数=154; 众数(360=3289; 792=2766; 124=2763) | — | — | — | 7.80 |
| 移民背景-公民身份 | `Q269` | Respondent citizen | 二值 | 92,016 | 1.022 | 0.148 | 1.000 | 2.000 | 5.35 |
| 组织参与-宗教组织 | `Q94R` | Membership: church or religious organization | 连续/有序 | 96,126 | 0.367 | 0.482 | 0.000 | 1.000 | 1.12 |
| 组织参与-体育组织 | `Q95R` | Membership: sport or recreational org | 连续/有序 | 96,082 | 0.253 | 0.435 | 0.000 | 1.000 | 1.17 |
| 组织参与-文化教育组织 | `Q96R` | Membership: art, music, educational org | 连续/有序 | 96,006 | 0.208 | 0.406 | 0.000 | 1.000 | 1.25 |
| 组织参与-工会 | `Q97R` | Membership: labor union | 连续/有序 | 95,829 | 0.164 | 0.371 | 0.000 | 1.000 | 1.43 |
| 组织参与-政党 | `Q98R` | Membership: political party | 连续/有序 | 95,876 | 0.149 | 0.356 | 0.000 | 1.000 | 1.38 |
| 组织参与-环保组织 | `Q99R` | Membership: environmental organization | 连续/有序 | 95,794 | 0.137 | 0.344 | 0.000 | 1.000 | 1.47 |
| 组织参与-专业组织 | `Q100R` | Membership: professional organization | 连续/有序 | 95,623 | 0.171 | 0.376 | 0.000 | 1.000 | 1.64 |
| 组织参与-慈善组织 | `Q101R` | Membership: charitable/humanitarian organization | 连续/有序 | 95,817 | 0.184 | 0.388 | 0.000 | 1.000 | 1.44 |
| 组织参与-消费者组织 | `Q102R` | Membership: consumer organization | 连续/有序 | 95,505 | 0.113 | 0.317 | 0.000 | 1.000 | 1.76 |
| 组织参与-自助组织 | `Q103R` | Membership: self-help group, mutual aid group | 连续/有序 | 95,618 | 0.150 | 0.357 | 0.000 | 1.000 | 1.65 |
| 组织参与-妇女组织 | `Q104R` | Active/Inactive membership: women’s group (R) | 连续/有序 | 94,179 | 0.130 | 0.336 | 0.000 | 1.000 | 3.13 |
| 组织参与-其他组织 | `Q105R` | Membership: other organization | 连续/有序 | 90,832 | 0.126 | 0.332 | 0.000 | 1.000 | 6.57 |
| 地域认同-人权感知 | `Q253P` | Respect for individual human rights nowadays | 连续/有序 | 95,120 | 2.701 | 0.861 | 1.000 | 4.000 | 2.16 |
| 地域认同-国家自豪 | `Q254P` | National pride | 连续/有序 | 95,844 | 3.480 | 0.769 | 1.000 | 5.000 | 1.42 |
| 地域认同-认同村镇 | `Q255P` | Feel close to your village, town or city | 连续/有序 | 94,313 | 3.387 | 0.737 | 1.000 | 4.000 | 2.99 |
| 地域认同-认同地区 | `Q256P` | Feel close to your district, region | 连续/有序 | 91,980 | 3.223 | 0.809 | 1.000 | 4.000 | 5.39 |
| 地域认同-认同国家 | `Q257P` | Feel close to your country | 连续/有序 | 96,041 | 3.270 | 0.798 | 1.000 | 4.000 | 1.21 |
| 地域认同-认同大洲 | `Q258P` | Feel close to your continent | 连续/有序 | 94,318 | 2.582 | 0.964 | 1.000 | 4.000 | 2.98 |
| 地域认同-认同世界 | `Q259P` | Feel close to the world | 连续/有序 | 92,128 | 2.519 | 0.995 | 1.000 | 4.000 | 5.24 |
| 儿童品质-礼貌 | `Q7P` | Important child qualities: Good manners | 连续/有序 | 96,823 | 0.775 | 0.418 | 0.000 | 1.000 | 0.41 |
| 儿童品质-独立 | `Q8P` | Important child qualities: Independence | 连续/有序 | 96,182 | 0.432 | 0.495 | 0.000 | 1.000 | 1.07 |
| 儿童品质-勤奋 | `Q9P` | Important child qualities: Hard work | 连续/有序 | 96,528 | 0.534 | 0.499 | 0.000 | 1.000 | 0.71 |
| 儿童品质-责任感 | `Q10P` | Important child qualities: Feeling of responsibility | 连续/有序 | 96,667 | 0.650 | 0.477 | 0.000 | 1.000 | 0.57 |
| 儿童品质-想象力 | `Q11P` | Important child qualities: Imagination | 连续/有序 | 96,017 | 0.216 | 0.411 | 0.000 | 1.000 | 1.24 |
| 儿童品质-宽容 | `Q12P` | Important child qualities: Tolerance and respect for other people | 连续/有序 | 96,577 | 0.630 | 0.483 | 0.000 | 1.000 | 0.66 |
| 儿童品质-节俭 | `Q13P` | Important child qualities: Thrift saving money and things | 连续/有序 | 96,104 | 0.302 | 0.459 | 0.000 | 1.000 | 1.15 |
| 儿童品质-毅力 | `Q14P` | Important child qualities: Determination perseverance | 连续/有序 | 96,089 | 0.335 | 0.472 | 0.000 | 1.000 | 1.16 |
| 儿童品质-宗教信仰 | `Q15P` | Important child qualities: Religious faith | 连续/有序 | 96,109 | 0.345 | 0.476 | 0.000 | 1.000 | 1.14 |
| 儿童品质-无私 | `Q16P` | Important child qualities: Unselfishness | 连续/有序 | 96,096 | 0.283 | 0.450 | 0.000 | 1.000 | 1.16 |
| 儿童品质-服从 | `Q17P` | Important child qualities: Obedience | 连续/有序 | 96,028 | 0.311 | 0.463 | 0.000 | 1.000 | 1.23 |
| 邻里排斥-吸毒者 | `Q18P` | Neighbors: Drug addicts | 连续/有序 | 96,291 | 0.837 | 0.369 | 0.000 | 1.000 | 0.96 |
| 邻里排斥-异族 | `Q19P` | Neighbors: People of a different race | 连续/有序 | 96,064 | 0.162 | 0.368 | 0.000 | 1.000 | 1.19 |
| 邻里排斥-艾滋病人 | `Q20P` | Neighbors: People who have AIDS | 连续/有序 | 95,759 | 0.399 | 0.490 | 0.000 | 1.000 | 1.50 |
| 邻里排斥-移民 | `Q21P` | Neighbors: Immigrants/foreign workers | 连续/有序 | 95,914 | 0.217 | 0.412 | 0.000 | 1.000 | 1.34 |
| 邻里排斥-同性恋 | `Q22P` | Neighbors: Homosexuals | 连续/有序 | 93,083 | 0.436 | 0.496 | 0.000 | 1.000 | 4.25 |
| 邻里排斥-异教徒 | `Q23P` | Neighbors: People of a different religion | 连续/有序 | 96,027 | 0.178 | 0.383 | 0.000 | 1.000 | 1.23 |
| 邻里排斥-酗酒者 | `Q24P` | Neighbors: Heavy drinkers | 连续/有序 | 96,213 | 0.686 | 0.464 | 0.000 | 1.000 | 1.04 |
| 邻里排斥-未婚同居者 | `Q25P` | Neighbors: Unmarried couples living together | 连续/有序 | 94,777 | 0.242 | 0.428 | 0.000 | 1.000 | 2.51 |
| 邻里排斥-异语者 | `Q26P` | Neighbors: People who speak a different language | 连续/有序 | 96,030 | 0.153 | 0.360 | 0.000 | 1.000 | 1.22 |

## 维度6 宗教/传统


| 子维度 | 变量 | Label(codebook 原文) | 类型 | 有效N | 均值 | 标准差 | 最小值 | 最大值 | 缺失率(%) |
|---|---|---|---|---|---|---|---|---|---|
| 上帝重要性 | `Q164` | Importance of God | 连续/有序 | 94,967 | 7.360 | 3.233 | 1.000 | 10.000 | 2.32 |
| 信上帝 | `Q165P` | Believe in: God | 二值 | 92,529 | 0.804 | 0.397 | 0.000 | 1.000 | 4.83 |
| 信来世 | `Q166P` | Believe in: life after death | 二值 | 89,625 | 0.643 | 0.479 | 0.000 | 1.000 | 7.81 |
| 信地狱 | `Q167P` | Believe in: hell | 二值 | 90,076 | 0.586 | 0.492 | 0.000 | 1.000 | 7.35 |
| 信天堂 | `Q168P` | Believe in: heaven | 二值 | 90,249 | 0.678 | 0.467 | 0.000 | 1.000 | 7.17 |
| 科学宗教冲突时宗教对 | `Q169P` | Whenever science and religion conflict,  religion is always right | 连续/有序 | 91,627 | 2.540 | 1.060 | 1.000 | 4.000 | 5.75 |
| 宗教派别 | `Q289` | Religious denominations - major groups | 分类 | 95,857 | 类别数=10; 众数(5=25398; 0=23460; 1=19038) | — | — | — | 1.40 |
| 宗教服务频率 | `Q171P` | How often do you attend religious services | 连续/有序 | 96,008 | 3.802 | 2.196 | 1.000 | 7.000 | 1.25 |
| 宗教组织信任 | `Q64P` | Confidence: Churches | 连续/有序 | 95,184 | 2.806 | 1.001 | 1.000 | 4.000 | 2.09 |
| 宗教重要性(指数) | `I_RELIGIMP` | RELIGIMP - Welzel disbelief- | 连续/有序 | 96,294 | 0.328 | 0.364 | 0.000 | 1.000 | 0.95 |
| 宗教信仰(指数) | `I_RELIGBEL` | RELIGBEL - Welzel disbelief- | 连续/有序 | 94,568 | 0.384 | 0.486 | 0.000 | 1.000 | 2.73 |
| 宗教实践(指数) | `I_RELIGPRAC` | RELIGPRAC - Welzel | 连续/有序 | 96,008 | 0.533 | 0.366 | 0.000 | 1.000 | 1.25 |
| 让父母骄傲 | `Q27P` | One of main goals in life has been to make my parents proud | 连续/有序 | 95,544 | 3.348 | 0.745 | 1.000 | 4.000 | 1.72 |

## 维度7 社会经济背景


| 子维度 | 变量 | Label(codebook 原文) | 类型 | 有效N | 均值 | 标准差 | 最小值 | 最大值 | 缺失率(%) |
|---|---|---|---|---|---|---|---|---|---|
| 性别 | `Q260` | Sex | 二值 | 97,125 | 1.526 | 0.499 | 1.000 | 2.000 | 0.10 |
| 出生年 | `Q261` | Year of birth | 连续/有序 | 95,636 | 1975.636 | 16.668 | 1916.000 | 2007.000 | 1.63 |
| 年龄 | `Q262` | Age | 连续/有序 | 96,709 | 43.178 | 16.583 | 16.000 | 103.000 | 0.53 |
| 年龄(6段) | `X003R` | Age recoded (6 intervals) | 连续/有序 | 96,709 | 3.331 | 1.602 | 1.000 | 6.000 | 0.53 |
| 年龄(3段) | `X003R2` | Age recoded (3 intervals) | 连续/有序 | 96,709 | 2.099 | 0.771 | 1.000 | 3.000 | 0.53 |
| 教育(ISCED) | `Q275` | Highest educational level: Respondent [ISCED 2011] | 连续/有序 | 96,149 | 3.565 | 2.022 | 0.000 | 8.000 | 1.10 |
| 教育(国别版) | `Q275A` | Highest educational level: Respondent (country specific) | 分类 | 54,197 | 类别数=404; 众数(360014=1067; 792015=843; 360012=840) | — | — | — | 44.25 |
| 教育(3组) | `Q275R` | Highest educational level: Respondent (recoded into 3 groups) | 连续/有序 | 96,149 | 2.017 | 0.807 | 1.000 | 3.000 | 1.10 |
| 配偶教育 | `Q276` | Highest educational level: Respondent´s Spouse [ISCED 2011] | 连续/有序 | 61,732 | 3.280 | 2.028 | 0.000 | 9.000 | 36.50 |
| 配偶教育(3组) | `Q276R` | Highest educational level: Respondent´s Spouse (recoded into 3 groups) | 连续/有序 | 61,701 | 1.904 | 0.801 | 1.000 | 3.000 | 36.53 |
| 父亲教育 | `Q278` | Highest educational level: Respondent´s Father [ISCED 2011] | 连续/有序 | 83,575 | 2.260 | 1.995 | 0.000 | 9.000 | 14.04 |
| 父亲教育(3组) | `Q278R` | Highest educational level: Respondent´s Father (recoded into 3 groups) | 连续/有序 | 83,524 | 1.541 | 0.735 | 1.000 | 3.000 | 14.09 |
| 就业状态 | `Q279` | Employment status | 连续/有序 | 95,987 | 3.121 | 2.061 | 1.000 | 8.000 | 1.27 |
| 配偶就业 | `Q280` | Employment status - Respondent´s Spouse | 连续/有序 | 59,382 | 2.830 | 1.943 | 1.000 | 9.000 | 38.92 |
| 职业大类 | `Q281` | Respondent - Occupational group | 分类 | 90,655 | 类别数=12; 众数(1=15111; 0=13042; 4=10993) | — | — | — | 6.75 |
| 配偶职业 | `Q282` | Respondent´s Spouse - Occupational group | 分类 | 59,085 | 类别数=12; 众数(0=9239; 1=8083; 6=6336) | — | — | — | 39.23 |
| 父亲职业 | `Q283` | Respondent´s Father - Occupational group (when respondent was 14 years old) | 分类 | 84,148 | 类别数=12; 众数(9=12915; 6=12072; 7=10904) | — | — | — | 13.45 |
| 就业部门 | `Q284` | Sector of employment | 分类 | 73,434 | 类别数=3; 众数(2=48025; 1=19376; 3=6033) | — | — | — | 24.47 |
| 主要收入来源 | `Q285` | Are you the chief wage earner in your house | 二值 | 94,513 | 1.534 | 0.499 | 1.000 | 2.000 | 2.78 |
| 家庭储蓄 | `Q286` | Family savings during past year | 连续/有序 | 94,280 | 2.033 | 0.902 | 1.000 | 4.000 | 3.02 |
| 社会阶层 | `Q287P` | Social class (subjective) | 连续/有序 | 91,673 | 2.758 | 0.978 | 1.000 | 5.000 | 5.71 |
| 收入等级 | `Q288` | Scale of incomes | 连续/有序 | 94,259 | 4.910 | 2.090 | 1.000 | 10.000 | 3.05 |
| 收入(重编码) | `Q288R` | Income level (recoded) | 连续/有序 | 94,259 | 1.855 | 0.574 | 1.000 | 3.000 | 3.05 |
| 种族归属 | `Q290` | Racial belonging/ ethnic group | 分类 | 87,619 | 类别数=432; 众数(124001=3195; 156001=3036; 826100=2148) | — | — | — | 9.88 |
| 国家GDP(现价PPP) | `GDPpercap1` | GDP per capita, PPP (current international $) [World | 国家级(连续) | 96,773 | 26034.996 | 24150.872 | 0.000 | 129103.010 | 0.46 |
| 国家GDP(不变价PPP) | `GDPpercap2` | GDP per capita, PPP (constant 2017 international $) | 国家级(连续) | 96,773 | 24973.223 | 23153.838 | 0.000 | 123965.290 | 0.46 |
| 国家Gini | `giniWB` |  | 国家级(连续) | 79,976 | 37.128 | 6.133 | 24.900 | 53.900 | 17.74 |
| 国家HDI | `hdi` |  | 国家级(连续) | 93,400 | 0.776 | 0.115 | 0.470 | 0.939 | 3.93 |
| 互联网普及率 | `internetusers` | Internet users, total (% of population) [ITU, 2017- | 国家级(连续) | 93,400 | 63.647 | 23.484 | 15.000 | 95.900 | 3.93 |

---

*统计表生成于 2026-08-24,基于 WVS Wave 7 v6.0 原始 CSV 数据。*