# WVS Wave 7 字段分析报告(CSV Codebook)

> 基于 `F00011055-WVS7_Codebook_Variables_report_V6.0.pdf`(404 页)与 CSV 611 个变量交叉解析生成。

---

## 一、概述

| 项目 | 数值 |
|---|---|
| CSV 变量总数 | 611 |
| Codebook 总页数 | 404 |
| Codebook 识别变量数 | 1,241(含子项/变体) |
| CSV 变量有 label 匹配 | 579(94.8%) |
| 未匹配变量 | 32(主要为国家级小写指标与部分政党字段) |
| 数据版本 | 6-0-0(2024-04-30) |
| 调查年份 | 2017–2023 |
| 覆盖国家/地区 | 66 |
| 样本量 | 97,220 |

### 变量命名约定

| 后缀/前缀 | 含义 |
|---|---|
| `Q1`–`Q290` | 核心问卷题(原始编码) |
| `QxxP` | 该题的 **0–1 标准化版本**(P = Proportion/标准化) |
| `Qxx_3` | 该题的三分版本 |
| `Q82_XXX` | Q82 的子项(各国际组织) |
| `Q291G1`/`Q291P1` | 政治信任模块的细分子项(G=政府,P=议会) |
| `X003R`/`X003R2` | 年龄重新编码版本 |
| `I_*` | Inglehart-Welzel 价值观子维度指数(0–1) |
| `Y001`–`Y003` | Schwartz/后物质主义指数 |
| `v2x_*`/`v2*` | V-Dem 民主治理指数 |
| `fh*`/`prf*`/`clf*` | Freedom House 评级 |
| `bti*` | Bertelsmann 转型指数 |
| `td_*` | 世界银行 WGI 治理指标 |
| `GPS_*`/`WVS_*` | 政党与选民位置(来自 Global Party Survey) |

---

## 二、编码约定

### 缺失值编码(WVS 标准)

| 代码 | 含义 |
|---|---|
| `-1` | Don´t know(不知道) |
| `-2` | No answer(无回答) |
| `-3` | 不适用(部分变量) |
| `-4` | Not asked in this country(该国未问此题) |
| `-5` | Missing; Not available(缺失/不可用) |

> 分析前需用 `df = df[df[col] >= 0]` 过滤负值。`QxxP` 标准化版本中负值已被处理或保留为缺失。

### 量表类型

| 量表 | 典型题项 | 范围 |
|---|---|---|
| 4 级重要性 | Q1–Q6(生活重要事项) | 1=非常重要 … 4=完全不重要 |
| 5 级品质 | Q7–Q34(儿童品质) | 1=重要 … 5=不重要 |
| 10 级量表 | Q48–Q56(满意度)、Q164(上帝重要性)、Q176–Q198(伦理可接受度) | 1=最低 … 10=最高 |
| 0–1 标准化 | `QxxP`、`I_*`、`SACSECVAL` 等 | 0–1(已标准化) |
| 二值 | Q165–Q168(信仰是/否) | 1=是,2=否 |
| 连续 | Q261(出生年)、Q262(年龄/教育年限)、Q264(子女数) | 数值 |
| ISO/分类 | B_COUNTRY、Q266(ISCO 职业)、Q164(宗教派别) | 编码 |

### 权重变量

| 变量 | 用途 |
|---|---|
| `W_WEIGHT` | 设计权重(抽样设计校正) |
| `S018` | 等权国家权重(每个国家等权,跨国比较用) |
| `PWGHT` | 人口权重 |
| `S025` | 其他权重 |
| `SECVALWGT`/`RESEMAVALWGT` | 价值观指数专用权重 |

---

## 三、字段章节详解

### 技术变量 (Technical)(33 个)

数据文件元信息:版本、DOI、调查波次/年份、国家编码、访谈元数据(方式/时长/语言)、地区编码、权重。跨国比较必用 W_WEIGHT 与 S018。

| 变量名 | Label | 备注 |
|---|---|---|
| `version` | Version of Data File |  |
| `doi` | Digital Object Identifier |  |
| `A_WAVE` | Wave |  |
| `A_YEAR` | Year of survey |  |
| `A_STUDY` | Study |  |
| `B_COUNTRY` | ISO 3166-1 numeric country code |  |
| `B_COUNTRY_ALPHA` | ISO 3166-1 alpha-3 country code |  |
| `C_COW_NUM` | CoW country code numeric |  |
| `C_COW_ALPHA` | CoW country code alpha |  |
| `D_INTERVIEW` | Interview ID |  |
| `S007` | _(未匹配)_ |  |
| `J_INTDATE` | Date of interview |  |
| `FW_START` | Year/month of start-fieldwork |  |
| `FW_END` | Year/month of end-fieldwork |  |
| `K_TIME_START` | Start time of the interview [HH.MM] |  |
| `K_TIME_END` | End time of the interview [HH.MM] |  |
| `K_DURATION` | Total length of interview [minutes] |  |
| `Q_MODE` | Mode of data collection |  |
| `N_REGION_ISO` | Region ISO 3166-2 |  |
| `N_REGION_WVS` | Region country specific |  |
| `N_REGION_NUTS2` | Region NUTS-2 |  |
| `N_REGION_NUTS1` | _(未匹配)_ |  |
| `N_TOWN` | Settlement name |  |
| `O1_LONGITUDE` | Geographical Coordinates - Longitude |  |
| `O2_LATITUDE` | Geographical Coordinates - Latitude |  |
| `L_INTERVIEWER_NUMBER` | _(未匹配)_ |  |
| `S_INTLANGUAGE` | Language in which interview was conducted |  |
| `LNGE_ISO` | Language in which interview was conducted  (ISO 639-1 Alpha 2 digit) |  |
| `F_INTPRIVACY` | Interview privacy |  |
| `W_WEIGHT` | Weight |  |
| `S018` | Equilibrated weight-1000 |  |
| `PWGHT` | _(未匹配)_ |  |
| `S025` | Country – year |  |

---

### 社会价值观、规范与刻板印象 (Q1-Q45)(48 个)

生活中重要事项(家庭/朋友/闲暇/政治/工作/宗教)、儿童品质期望(礼貌/独立/勤奋/想象/节俭等)、近邻信任、可接受行为边界。刻画社会规范与价值排序。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q1P` | Important in life: Family | [0-1 标准化] |
| `Q2P` | Important in life: Friends | [0-1 标准化] |
| `Q3P` | Important in life: Leisure time | [0-1 标准化] |
| `Q4P` | Important in life: Politics | [0-1 标准化] |
| `Q5P` | Important in life: Work | [0-1 标准化] |
| `Q6P` | Important in life: Religion | [0-1 标准化] |
| `Q7P` | Important child qualities: Good manners | [0-1 标准化] |
| `Q8P` | Important child qualities: Independence | [0-1 标准化] |
| `Q9P` | Important child qualities: Hard work | [0-1 标准化] |
| `Q10P` | Important child qualities: Feeling of responsibility | [0-1 标准化] |
| `Q11P` | Important child qualities: Imagination | [0-1 标准化] |
| `Q12P` | Important child qualities: Tolerance and respect for other people | [0-1 标准化] |
| `Q13P` | Important child qualities: Thrift saving money and things | [0-1 标准化] |
| `Q14P` | Important child qualities: Determination perseverance | [0-1 标准化] |
| `Q15P` | Important child qualities: Religious faith | [0-1 标准化] |
| `Q16P` | Important child qualities: Unselfishness | [0-1 标准化] |
| `Q17P` | Important child qualities: Obedience | [0-1 标准化] |
| `Q18P` | Neighbors: Drug addicts | [0-1 标准化] |
| `Q19P` | Neighbors: People of a different race | [0-1 标准化] |
| `Q20P` | Neighbors: People who have AIDS | [0-1 标准化] |
| `Q21P` | Neighbors: Immigrants/foreign workers | [0-1 标准化] |
| `Q22P` | Neighbors: Homosexuals | [0-1 标准化] |
| `Q23P` | Neighbors: People of a different religion | [0-1 标准化] |
| `Q24P` | Neighbors: Heavy drinkers | [0-1 标准化] |
| `Q25P` | Neighbors: Unmarried couples living together | [0-1 标准化] |
| `Q26P` | Neighbors: People who speak a different language | [0-1 标准化] |
| `Q27P` | One of main goals in life has been to make my parents proud | [0-1 标准化] |
| `Q28P` | Pre-school child suffers with working mother | [0-1 标准化] |
| `Q29P` | Men make better political leaders than women do | [0-1 标准化] |
| `Q30P` | University is more important for a boy than for a girl | [0-1 标准化] |
| `Q31P` | Men make better business executives than women do | [0-1 标准化] |
| `Q32P` | Being a housewife just as fulfilling | [0-1 标准化] |
| `Q33_3` | Jobs scarce: Men should have more right to a job than women |  |
| `Q33P` | Jobs scarce: Men should have more right to a job than women | [0-1 标准化] |
| `Q34_3` | Jobs scarce: Employers should give priority to (nation) people than immigrants |  |
| `Q34P` | Jobs scarce: Employers should give priority to (nation) people than immigrants | [0-1 标准化] |
| `Q35_3` | Problem if women have more income than husband |  |
| `Q35P` | Problem if women have more income than husband | [0-1 标准化] |
| `Q36P` | Homosexual couples are as good parents as other couples | [0-1 标准化] |
| `Q37P` | Duty towards society to have children | [0-1 标准化] |
| `Q38P` | It is children duty to take care of ill parent | [0-1 标准化] |
| `Q39P` | People who don´t work turn lazy | [0-1 标准化] |
| `Q40P` | Work is a duty towards society | [0-1 标准化] |
| `Q41P` | Work should  always come first even if it means less spare time | [0-1 标准化] |
| `Q42` | Basic kinds of attitudes concerning society |  |
| `Q43P` | Future changes: Less importance placed on work | [0-1 标准化] |
| `Q44P` | Future changes: More emphasis on technology | [0-1 标准化] |
| `Q45P` | Future changes: Greater respect for authority | [0-1 标准化] |

---

### 幸福与福祉 (Q46-Q56)(11 个)

生活自由感、生活满意度、财务满意度、幸福感、健康自评、国家经济评价。主观福祉核心指标。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q46P` | Feeling of happiness | [0-1 标准化] |
| `Q47P` | State of health (subjective) | [0-1 标准化] |
| `Q48` | How much freedom of choice and control |  |
| `Q49` | Satisfaction with your life |  |
| `Q50` | Satisfaction with financial situation of household |  |
| `Q51P` | Frequency you/family (last 12 month): Gone without enough food to eat | [0-1 标准化] |
| `Q52P` | Frequency you/family (last 12 month): Felt unsafe from crime in your own home | [0-1 标准化] |
| `Q53P` | Frequency you/family (last 12 month): Gone without needed medicine or treatment | [0-1 标准化] |
| `Q54P` | Frequency you/family (last 12 month): Gone without a cash income | [0-1 标准化] |
| `Q55P` | In the last 12 month, how often have you or your family: Gone without a safe shelter | [0-1 标准化] |
| `Q56P` | Standard of living comparing with your parents | [0-1 标准化] |

---

### 社会资本、信任与组织成员 (Q57-Q105)(78 个)

对各类机构(政府/议会/政党/军队/警察/法院/媒体/联合国等)的信任、组织成员身份(教会/工会/政党/NGO 等)、人际信任、安全感受。社会资本与信任网络。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q57P` | Most people can be trusted | [0-1 标准化] |
| `Q58P` | How much you trust: Your family | [0-1 标准化] |
| `Q59P` | Trust: Your neighborhood | [0-1 标准化] |
| `Q60P` | Trust: People you know personally | [0-1 标准化] |
| `Q61P` | Trust: People you meet for the first time | [0-1 标准化] |
| `Q62P` | Trust: People of another religion | [0-1 标准化] |
| `Q63P` | Trust: People of another nationality | [0-1 标准化] |
| `Q64P` | Confidence: Churches | [0-1 标准化] |
| `Q65P` | Confidence: Armed Forces | [0-1 标准化] |
| `Q66P` | Confidence: The Press | [0-1 标准化] |
| `Q67P` | Confidence: Television | [0-1 标准化] |
| `Q68P` | Confidence: Labor Unions | [0-1 标准化] |
| `Q69P` | Confidence: The Police | [0-1 标准化] |
| `Q70P` | Confidence: Justice System/Courts | [0-1 标准化] |
| `Q71P` | Confidence: The Government | [0-1 标准化] |
| `Q72P` | Confidence: The Political Parties | [0-1 标准化] |
| `Q73P` | Confidence: Parliament | [0-1 标准化] |
| `Q74P` | Confidence: The Civil Services | [0-1 标准化] |
| `Q75P` | Confidence: Universities | [0-1 标准化] |
| `Q76P` | Confidence: Election | [0-1 标准化] |
| `Q77P` | Confidence: Major Companies | [0-1 标准化] |
| `Q78P` | Confidence: Banks | [0-1 标准化] |
| `Q79P` | Confidence: The Environmental Protection Movement | [0-1 标准化] |
| `Q80P` | Confidence: The Women´s Movement | [0-1 标准化] |
| `Q81P` | Confidence: Charitable or humanitarian organizations | [0-1 标准化] |
| `Q82P` | Confidence: Major regional organization (combined from country-specific) | [0-1 标准化] |
| `Q82_AFRICANUNIONP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_APECP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_ARABLEAGUEP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_ASEANP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_CISP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_CUSMAP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_ECOP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_EUP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_GULFCOOPP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_ISLCOOPP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_MERCOSURP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_NAFTAP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_OASP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_SAARCP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_SCOP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_TLCP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q82_UNDPP` | Confidence: Major regional organization (combined from country-specific) | [子项] |
| `Q83P` | Confidence: The United Nations (UN) | [0-1 标准化] |
| `Q84P` | Confidence: International Monetary Found (IMF) | [0-1 标准化] |
| `Q85P` | Confidence: International Criminal Court (ICC) | [0-1 标准化] |
| `Q86P` | Confidence: North Atlantic Treaty Organization (NATO) | [0-1 标准化] |
| `Q87P` | Confidence: The World Bank (WB) | [0-1 标准化] |
| `Q88P` | Confidence: The World Health Organization (WHO) | [0-1 标准化] |
| `Q89P` | Confidence: The World Trade Organization (WTO) | [0-1 标准化] |
| `Q90` | International organizations: being effective vs being democratic |  |
| `Q91` | Countries with the permanent seats on the UN Security Council |  |
| `Q92` | Where are the headquarters of the International Monetary Fund (IMF) located? |  |
| `Q93` | Which of the following problems does the organization Amnesty International |  |
| `Q94` | Active/Inactive membership: Church or religious organization |  |
| `Q94R` | Membership: church or religious organization |  |
| `Q95` | Active/Inactive membership: sport or recreational org |  |
| `Q95R` | Membership: sport or recreational org |  |
| `Q96` | Active/Inactive membership: art, music, educational organization |  |
| `Q96R` | Membership: art, music, educational org |  |
| `Q97` | Active/Inactive membership: Labor union |  |
| `Q97R` | Membership: labor union |  |
| `Q98` | Active/Inactive membership: Political party |  |
| `Q98R` | Membership: political party |  |
| `Q99` | Active/Inactive membership: Environmental organization |  |
| `Q99R` | Membership: environmental organization |  |
| `Q100` | Active/Inactive membership: professional organization |  |
| `Q100R` | Membership: professional organization |  |
| `Q101` | Active/Inactive membership: charitable/humanitarian organization |  |
| `Q101R` | Membership: charitable/humanitarian organization |  |
| `Q102` | Active/Inactive membership: consumer organization |  |
| `Q102R` | Membership: consumer organization |  |
| `Q103` | Active/Inactive membership: Self-help group, mutual aid group |  |
| `Q103R` | Membership: self-help group, mutual aid group |  |
| `Q104` | Active/Inactive membership: women’s group |  |
| `Q104R` | Active/Inactive membership: women’s group (R) |  |
| `Q105` | Active/Inactive membership: other organization |  |
| `Q105R` | Membership: other organization |  |

---

### 经济价值观 (Q106-Q111)(6 个)

收入平等 vs 激励、私有 vs 国有、政府 vs 个人责任、竞争观、成功归因(努力 vs 运气)、环境 vs 增长。经济意识形态。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q106` | Income equality vs larger income differences |  |
| `Q107` | Private vs state ownership of business |  |
| `Q108` | Government´s vs individual´s responsibility |  |
| `Q109` | Competition good or harmful |  |
| `Q110` | Success: hard work vs luck |  |
| `Q111` | Protecting environment vs. Economic growth |  |

---

### 腐败感知 (Q112-Q120)(9 个)

各类机构涉腐程度、行贿频率、问责风险。治理质量主观感知。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q112` | Perceptions of corruption in the country |  |
| `Q113` | Involved in corruption: State authorities |  |
| `Q114` | Involved in corruption: Business executives |  |
| `Q115` | Involved in corruption: Local authorities |  |
| `Q116` | Involved in corruption: Civil service providers |  |
| `Q117` | Involved in corruption: Journalists and media |  |
| `Q118` | Frequency ordinary people pay a bribe, give a gift or do a favor to local |  |
| `Q119P` | Degree of agreement: On the whole, women are less corrupt than men | [0-1 标准化] |
| `Q120` | Risk to be held accountable for giving or receiving a bribe |  |

---

### 移民感知 (Q121-Q130)(10 个)

移民对经济/文化/犯罪/恐怖主义/失业/社会冲突的影响评价。移民态度多维量表。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q121` | Impact of immigrants on the development of the country |  |
| `Q122` | Immigration in your country: Fills useful jobs in the workforce |  |
| `Q123` | Immigration in your country: Strengthens cultural diversity |  |
| `Q124` | Immigration in your country: Increases the crime rate |  |
| `Q125` | Immigration in your country: Gives asylum to political refugees |  |
| `Q126` | Immigration in your country: Increases the risks of terrorism |  |
| `Q127` | Immigration in your country: Helps poor people establish new lives |  |
| `Q128` | Immigration in your country: Increases unemployment |  |
| `Q129` | Immigration in your country: Leads to social conflict |  |
| `Q130P` | Immigration policy preference | [0-1 标准化] |

---

### 安全感知 (Q131-Q151)(21 个)

各类犯罪/战争/恐怖主义发生频率感知、个人安全感受、国家安全感。安全环境主观评估。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q131P` | Secure in neighborhood | [0-1 标准化] |
| `Q132P` | Frequency in your neighborhood: Robberies | [0-1 标准化] |
| `Q133P` | Frequency in your neighborhood: Alcohol consumed in the streets | [0-1 标准化] |
| `Q134P` | Frequency in your neighborhood: Police or military interfere with people’s private | [0-1 标准化] |
| `Q135P` | Frequency in your neighborhood: Racist behavior | [0-1 标准化] |
| `Q136P` | Frequency in your neighborhood: Drug sale in streets | [0-1 标准化] |
| `Q137P` | Frequency in your neighborhood: Street violence and fights | [0-1 标准化] |
| `Q138P` | Frequency in your neighborhood: Sexual harassment | [0-1 标准化] |
| `Q139P` | Things done for reasons of security: Didn’t carry much money | [0-1 标准化] |
| `Q140P` | Things done for reasons of security: Preferred not to go out at night | [0-1 标准化] |
| `Q141P` | Things done for reasons of security: Carried a knife, gun or other weapon | [0-1 标准化] |
| `Q142P` | Worries: Losing my job or not finding a job | [0-1 标准化] |
| `Q143P` | Worries: Not being able to give one´s children a good education | [0-1 标准化] |
| `Q144P` | Respondent was victim of a crime during the past year | [0-1 标准化] |
| `Q145P` | Respondent´s family was victim of a crime during last year | [0-1 标准化] |
| `Q146P` | Worries: A war involving my country | [0-1 标准化] |
| `Q147P` | Worries: A terrorist attack | [0-1 标准化] |
| `Q148P` | Worries: A civil war | [0-1 标准化] |
| `Q149` | Freedom and Equality - Which more important |  |
| `Q150` | Freedom and security - Which more important |  |
| `Q151P` | Willingness to fight for country | [0-1 标准化] |

---

### 后物质主义指数 (Q152-Q157)(6 个)

国家目标与个人目标排序(Inglehart 物质主义 vs 后物质主义)。后物质主义核心测量。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q152` | Aims of country: first choice |  |
| `Q153` | Aims of country: second choice |  |
| `Q154` | Aims of respondent: first choice |  |
| `Q155` | Aims of respondent: second choice |  |
| `Q156` | Most important: first choice |  |
| `Q157` | Most important: second choice |  |

---

### 科技感知 (Q158-Q163)(6 个)

科技对生活/机会/信仰的影响、科技认知需求、科技整体评价。科技态度量表。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q158` | Science and technology are making our lives healthier, easier, and more |  |
| `Q159` | Because of science and technology, there will be more opportunities for the next |  |
| `Q160` | We depend too much on science and not enough on faith |  |
| `Q161` | One of the bad effects of science is that it breaks down people’s ideas of right and |  |
| `Q162` | It is not important for me to know about science in my daily life |  |
| `Q163` | The world is better off, or worse off, because of science and technology |  |

---

### 宗教价值观 (Q164-Q175)(13 个)

上帝重要性、信仰内容(上帝/来世/地狱/天堂/灵魂)、宗教派别、宗教服务频率、宗教组织信任、宗教与非宗教人群关系。宗教信仰与实践。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q164` | Importance of God |  |
| `Q165P` | Believe in: God | [0-1 标准化] |
| `Q166P` | Believe in: life after death | [0-1 标准化] |
| `Q167P` | Believe in: hell | [0-1 标准化] |
| `Q168P` | Believe in: heaven | [0-1 标准化] |
| `Q169P` | Whenever science and religion conflict,  religion is always right | [0-1 标准化] |
| `Q170P` | The only acceptable religion  is my religion | [0-1 标准化] |
| `Q171P` | How often do you attend religious services | [0-1 标准化] |
| `Q172P` | How often to you pray | [0-1 标准化] |
| `Q172R` | How often do you pray (Constructed) |  |
| `Q173P` | Religious person | [0-1 标准化] |
| `Q174` | Meaning of religion: To follow religious norms and ceremonies vs To do good to |  |
| `Q175` | Meaning of religion: To make sense of life after death vs To make sense of life in |  |

---

### 伦理价值观 (Q176-Q198)(23 个)

各类行为可接受度(骗福利/逃票/偷窃/逃税/受贿/同性恋/卖淫/堕胎/离婚/安乐死/自杀等)。道德弹性多维量表。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q176P` | Degree of agreement: Nowadays one often has trouble deciding which moral rules | [0-1 标准化] |
| `Q177` | Justifiable: Claiming government benefits to which you are not entitled |  |
| `Q178` | Justifiable: Avoiding a fare on public transport |  |
| `Q179` | Justifiable: Stealing property |  |
| `Q180` | Justifiable: Cheating on taxes |  |
| `Q181` | Justifiable: Someone accepting a bribe in the course of their duties |  |
| `Q182` | Justifiable: Homosexuality |  |
| `Q183` | Justifiable: Prostitution |  |
| `Q184` | Justifiable: Abortion |  |
| `Q185` | Justifiable: Divorce |  |
| `Q186` | Justifiable: Sex before marriage |  |
| `Q187` | Justifiable: Suicide |  |
| `Q188` | Justifiable: Euthanasia |  |
| `Q189` | Justifiable: For a man to beat his wife |  |
| `Q190` | Justifiable: Parents beating children |  |
| `Q191` | Justifiable: Violence against other people |  |
| `Q192` | Justifiable: Terrorism as a political, ideological or religious mean |  |
| `Q193` | Justifiable: Having casual sex |  |
| `Q194` | Justifiable: Political violence |  |
| `Q195` | Justifiable: Death penalty |  |
| `Q196P` | Government has the right: Keep people under video surveillance in public areas | [0-1 标准化] |
| `Q197P` | Government has the right: Monitor all e-mails and any other information | [0-1 标准化] |
| `Q198P` | Government has the right: Collect information about anyone living in this | [0-1 标准化] |

---

### 政治兴趣与政治参与 (Q199-Q234)(39 个)

政治兴趣、讨论频率、投票行为、政治行动(请愿/抵制/示威/罢工/网络参与)、政党亲近度。政治参与行为量表。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q199P` | Interest in politics | [0-1 标准化] |
| `Q200P` | How often discusses political matters with friends | [0-1 标准化] |
| `Q201P` | Information source: Daily newspaper | [0-1 标准化] |
| `Q202P` | Information source: TV news | [0-1 标准化] |
| `Q203P` | Information source: Radio news | [0-1 标准化] |
| `Q204P` | Information source: Mobile phone | [0-1 标准化] |
| `Q205P` | Information source: Email | [0-1 标准化] |
| `Q206P` | Information source: Internet | [0-1 标准化] |
| `Q207P` | Information source: Social media (Facebook, Twitter, etc.) | [0-1 标准化] |
| `Q208P` | Information source: Talk with friends or colleagues | [0-1 标准化] |
| `Q209P` | Political action: Signing a petition | [0-1 标准化] |
| `Q210P` | Political action: joining in boycotts | [0-1 标准化] |
| `Q211P` | Political action: attending lawful/peaceful demonstrations | [0-1 标准化] |
| `Q212P` | Political action: joining unofficial strikes | [0-1 标准化] |
| `Q213P` | Social activism: Donating to a group or campaign | [0-1 标准化] |
| `Q214P` | Social activism: Contacting a government official | [0-1 标准化] |
| `Q215P` | Social activism: Encouraging others to take action about political issues | [0-1 标准化] |
| `Q216P` | Social activism: Encouraging others to vote | [0-1 标准化] |
| `Q217P` | Political actions online: Searching information about politics and political events | [0-1 标准化] |
| `Q218P` | Political actions online: Signing an electronic petition | [0-1 标准化] |
| `Q219P` | Political actions online: Encouraging other people to take any form of political | [0-1 标准化] |
| `Q220P` | Political actions online: Organizing political activities, events, protests | [0-1 标准化] |
| `Q221P` | Vote in elections: local level | [0-1 标准化] |
| `Q222P` | Vote in elections: National level | [0-1 标准化] |
| `Q223` | Which party would you vote for if there were a national election tomorrow |  |
| `Q223_ABREV` | Party preference Abbreviation |  |
| `Q223_LOCAL` | Party preference Local name |  |
| `Q224P` | How often in country´s elections: Votes are counted fairly | [0-1 标准化] |
| `Q225P` | How often in country´s elections: Opposition candidates are prevented from | [0-1 标准化] |
| `Q226P` | How often in country´s elections: TV news favors the governing party | [0-1 标准化] |
| `Q227P` | How often in country´s elections: Voters are bribed | [0-1 标准化] |
| `Q228P` | How often in country´s elections: Journalists provide fair coverage of elections | [0-1 标准化] |
| `Q229P` | How often in country´s elections: Election officials are fair | [0-1 标准化] |
| `Q230P` | How often in country´s elections: Rich people buy elections | [0-1 标准化] |
| `Q231P` | How often in country´s elections: Voters are threatened with  violence at the polls | [0-1 标准化] |
| `Q232P` | How often in country´s elections: Voters are offered a genuine choice in the | [0-1 标准化] |
| `Q233P` | How often in country´s elections: Women have equal opportunities to run the office | [0-1 标准化] |
| `Q234AP` | _(未匹配)_ |  |
| `Q234P` | Some people think that having honest elections makes a lot of difference in their | [0-1 标准化] |

---

### 政治文化与政治体制 (Q235-Q259)(25 个)

左右政治量表、民主定义要素、政体评价、国家自豪感、国家目标。政治文化与体制偏好。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q235P` | Political system: Having a strong leader who does not have to bother with | [0-1 标准化] |
| `Q236P` | Political system: Having experts, not government, make decisions according to | [0-1 标准化] |
| `Q237P` | Political system: Having the army rule | [0-1 标准化] |
| `Q238P` | Political system: Having a democratic political system | [0-1 标准化] |
| `Q239P` | Political system: Having a system governed by religious law in which there are no | [0-1 标准化] |
| `Q240` | Left-right political scale |  |
| `Q241` | Democracy: Governments tax the rich and subsidize the poor |  |
| `Q242` | Democracy: Religious authorities interpret the laws |  |
| `Q243` | Democracy: People choose their leaders in free elections |  |
| `Q244` | Democracy: People receive state aid for unemployment |  |
| `Q245` | Democracy: The army takes over when government is incompetent |  |
| `Q246` | Democracy: Civil rights protect people’s liberty against oppression |  |
| `Q247` | Democracy: The state makes people´s incomes equal |  |
| `Q248` | Democracy: People obey their rulers |  |
| `Q249` | Democracy: Women have the same rights as men |  |
| `Q250` | Importance of democracy |  |
| `Q251` | How democratically is this country being governed today |  |
| `Q252` | Satisfaction with the political system performance |  |
| `Q253P` | Respect for individual human rights nowadays | [0-1 标准化] |
| `Q254P` | National pride | [0-1 标准化] |
| `Q255P` | Feel close to your village, town or city | [0-1 标准化] |
| `Q256P` | Feel close to your district, region | [0-1 标准化] |
| `Q257P` | Feel close to your country | [0-1 标准化] |
| `Q258P` | Feel close to your continent | [0-1 标准化] |
| `Q259P` | Feel close to the world | [0-1 标准化] |

---

### 人口与社会经济 (Q260-Q290)(41 个)

性别、出生年/年龄、教育、婚姻状况、子女数、家庭规模、移民背景(本人/父母/祖父母出生国)、就业、职业(ISCO)、社会阶层自评、收入等级、种族归属。人口学背景变量。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q260` | Sex |  |
| `Q261` | Year of birth |  |
| `Q262` | Age |  |
| `Q263` | Respondent immigrant |  |
| `Q264` | Mother immigrant |  |
| `Q265` | Father immigrant |  |
| `Q266` | Country of birth: Respondent |  |
| `Q267` | Country of birth: Mother of the respondent |  |
| `Q268` | Country of birth: Father of the respondent |  |
| `Q269` | Respondent citizen |  |
| `Q270` | Number of people in household |  |
| `Q271` | Do you live with your parents |  |
| `Q272` | Language at home |  |
| `Q273` | Marital status |  |
| `Q274` | How many children do you have |  |
| `Q275` | Highest educational level: Respondent [ISCED 2011] |  |
| `Q275A` | Highest educational level: Respondent (country specific) |  |
| `Q275R` | Highest educational level: Respondent (recoded into 3 groups) |  |
| `Q276` | Highest educational level: Respondent´s Spouse [ISCED 2011] |  |
| `Q276A` | Highest educational level: Respondent´s Spouse (country specific) |  |
| `Q276R` | Highest educational level: Respondent´s Spouse (recoded into 3 groups) |  |
| `Q277` | Highest educational level: Respondent´s Mother [ISCED 2011] |  |
| `Q277A` | Highest educational level: Respondent´s Mother (country specific) |  |
| `Q277R` | Highest educational level: Respondent´s Mother (recoded into 3 groups) |  |
| `Q278` | Highest educational level: Respondent´s Father [ISCED 2011] |  |
| `Q278A` | Highest educational level: Respondent´s Father (country specific) |  |
| `Q278R` | Highest educational level: Respondent´s Father (recoded into 3 groups) |  |
| `Q279` | Employment status |  |
| `Q280` | Employment status - Respondent´s Spouse |  |
| `Q281` | Respondent - Occupational group |  |
| `Q282` | Respondent´s Spouse - Occupational group |  |
| `Q283` | Respondent´s Father - Occupational group (when respondent was 14 years old) |  |
| `Q284` | Sector of employment |  |
| `Q285` | Are you the chief wage earner in your house |  |
| `Q286` | Family savings during past year |  |
| `Q287P` | Social class (subjective) | [0-1 标准化] |
| `Q288` | Scale of incomes |  |
| `Q288R` | Income level (recoded) |  |
| `Q289` | Religious denominations - major groups |  |
| `Q289CS9` | _(未匹配)_ |  |
| `Q290` | Racial belonging/ ethnic group |  |

---

### 政治信任模块 (Q291-Q294)(36 个)

对政府/议会/政党/公务员/法院/警察的细粒度评价(能力/效率/腐败/透明度等)。扩展政治信任量表(部分国家)。

| 变量名 | Label | 备注 |
|---|---|---|
| `Q291G1` | Government: Overall, the government is competent and efficient |  |
| `Q291G2` | Government: The government usually carries out its duties poorly |  |
| `Q291G3` | Government: The government usually acts in its own interests |  |
| `Q291G4` | Government: The government wants to do its best to serve the country |  |
| `Q291G5` | Government: The government is generally free of corruption |  |
| `Q291G6` | Government: The government’s work is open and transparent |  |
| `Q291P1` | Parliament: Overall, parliament is competent and efficient |  |
| `Q291P2` | Parliament: Parliament usually carries out its duties poorly |  |
| `Q291P3` | Parliament: Parliament  usually acts in its own interests |  |
| `Q291P4` | Parliament: Parliament wants to do its best to serve the country |  |
| `Q291P5` | Parliament: Parliament is generally free of corruption |  |
| `Q291P6` | Parliament: Parliament’s work is open and transparent |  |
| `Q291UN1` | United Nations: Overall, the UN is competent and efficient |  |
| `Q291UN2` | United Nations: The UN usually carries out its duties poorly |  |
| `Q291UN3` | United Nations: The UN usually acts in its own interests |  |
| `Q291UN4` | United Nations: The UN wants to do its best to serve the world |  |
| `Q291UN5` | United Nations: The UN is generally free of corruption |  |
| `Q291UN6` | United Nations: The UN’s work is open and transparent |  |
| `Q292A` | I am unsure whether to believe most politicians |  |
| `Q292B` | I am usually cautious about trusting politicians |  |
| `Q292C` | In general, politicians are open about their decisions |  |
| `Q292D` | In general, the government usually does the right thing |  |
| `Q292E` | Information provided by the government is generally unreliable |  |
| `Q292F` | It is best to be cautious about trusting the government |  |
| `Q292G` | Most politicians are honest and truthful |  |
| `Q292H` | People in the government often show poor judgement |  |
| `Q292I` | Politicians are often incompetent and ineffective |  |
| `Q292J` | Politicians don’t respect people like me |  |
| `Q292K` | Politicians often put country above their personal interests |  |
| `Q292L` | Politicians usually ignore my community |  |
| `Q292M` | The government acts unfairly towards people like me |  |
| `Q292N` | The government understands the needs of my community |  |
| `Q292O` | The government usually has good intentions |  |
| `Q293` | How much you trust the Head of State in this country? |  |
| `Q294A` | How many world leaders from this list you generally trust (Group A) |  |
| `Q294B` | How many world leaders from this list you generally trust (Group B) |  |

---

### 性别模块(5 个)

性别角色态度(职业/教育/政治/家庭),G/H 前缀变量。

| 变量名 | Label | 备注 |
|---|---|---|
| `G_TOWNSIZE` | Settlement size_8 groups |  |
| `G_TOWNSIZE2` | Settlement size_5 groups |  |
| `H_SETTLEMENT` | Settlement type |  |
| `H_URBRURAL` | Urban-Rural |  |
| `I_PSU` | Primary Sampling Unit ID |  |

---

### WVS 指数(39 个)

Inglehart-Welzel 价值观指数(世俗-传统、生存-自我表达)及子维度(权威/民族主义/虔诚/自主/平等/选择/发声等),Schwartz 后物质主义指数。已 0-1 标准化,可直接用于建模。

| 变量名 | Label | 备注 |
|---|---|---|
| `Y001` | Post-Materialist index 12-item Y001_1: |  |
| `Y002` | Post-Materialist index 4-item |  |
| `Y003` | Autonomy Index |  |
| `SACSECVAL` | SACSECVAL.- Welzel Overall |  |
| `RESEMAVAL` | RESEMAVAL.- Welzel |  |
| `I_AUTHORITY` | AUTHORITY - Welzel |  |
| `I_NATIONALISM` | NATIONALISM - Welzel |  |
| `I_DEVOUT` | DEVOUT- Welzel defiance - 3: |  |
| `DEFIANCE` | DEFIANCE.- Welzel defiance |  |
| `I_RELIGIMP` | RELIGIMP - Welzel disbelief- |  |
| `I_RELIGBEL` | RELIGBEL - Welzel disbelief- |  |
| `I_RELIGPRAC` | RELIGPRAC - Welzel |  |
| `DISBELIEF` | DISBELIEF.- Welzel disbelief |  |
| `I_NORM1` | NORM1 - Welzel relativism- 1: |  |
| `I_NORM2` | NORM2 - Welzel relativism- 2: |  |
| `I_NORM3` | NORM3 - Welzel relativism- 3: |  |
| `RELATIVISM` | RELATIVISM.- Welzel |  |
| `I_TRUSTARMY` | TRUSTARMY- Welzel |  |
| `I_TRUSTPOLICE` | TRUSTPOLICE- Welzel |  |
| `I_TRUSTCOURTS` | TRUSTCOURTS- Welzel |  |
| `SCEPTICISM` | SCEPTICISM.- Welzel |  |
| `I_INDEP` | INDEP- Welzel autonomy-1: |  |
| `I_IMAGIN` | IMAGIN- Welzel autonomy-2: |  |
| `I_NONOBED` | Emancipative Values-1: |  |
| `AUTONOMY` | AUTONOMY.- Wezel |  |
| `I_WOMJOB` | WOMJOB- Welzel equality-1: |  |
| `I_WOMPOL` | WOMPOL- Welzel equality-2: |  |
| `I_WOMEDU` | WOMEDU- Welzel equality-3: |  |
| `EQUALITY` | Emancipative Values-2: |  |
| `I_HOMOLIB` | HOMOLIB- Welzel choice-1: |  |
| `I_ABORTLIB` | ABORTLIB- Welzel choice-2: |  |
| `I_DIVORLIB` | DIVORLIB- Welzel choice-3: |  |
| `CHOICE` | CHOICE.- Welzel choice sub- |  |
| `I_VOICE1` | VOICE1- Welzel voice-1 |  |
| `I_VOICE2` | VOICE2- Welzel voice-2 |  |
| `I_VOI2_00` | VOI2_00- Welzel voice-3 |  |
| `VOICE` | VOICE.- Welzel voice sub- |  |
| `SECVALWGT` | Weight for overall secular |  |
| `RESEMAVALWGT` | Weight for Emancipative |  |

---

### 上下文/国家级指标(126 个)

外部合并的国家级指标:Freedom House(自由度)、Polity(民主-独裁)、V-Dem(民主治理多维)、BTI(转型指数)、世界银行 WGI(治理)、UN/世行宏观社会经济(GDP/Gini/HDI/教育/健康/互联网/人口/CO₂ 等)。个体内为常数,用于层级分析。

| 变量名 | Label | 备注 |
|---|---|---|
| `fhregion` | Region (6 groups) [Freedom House, 2019] |  |
| `polregfh` | Type of political regime (3=Free, 2=Partly Free, |  |
| `freestfh` | Global Freedom Status (0-min to 100-max) [Freedom |  |
| `prfhrat` | Political rights rating (1=high to 7=low) [Freedom |  |
| `prfhscore` | Political rights points (1 min to 40 max) [Freedom |  |
| `clfhrat` | Civil Liberties rating (1=high to 7=low) [Freedom |  |
| `clfhscore` | Civil Liberties points (1 min to 60 max) [Freedom |  |
| `democ` | Institutionalized Democracy (0=min to 10=max) |  |
| `autoc` | Institutionalized Autocracy  (0=min to 10=max) |  |
| `polity` | Polity combined score for autocracy-democracy  (- |  |
| `durable` | Regime Durability (the number of years since the |  |
| `regtype` | Regime type (1=autocracy; 2=closed anocracy; |  |
| `ruleoflaw` | Rule of Law Index (0=min to 1=max) [World Justice |  |
| `corrupttransp` | Corruption perception index (0=highly corrupt to |  |
| `electintegr` | Index of Perceptions of Electoral Integrity, (0-100), |  |
| `btiregion` | BTI Region (7 categories) [Bertelsmann Stiftung, |  |
| `btistatus` | BTI Status Index (1=min to 10=max) [Bertelsmann |  |
| `btidemstatus` | BTI Democracy Status  (1=min to |  |
| `btistate` | BTI Stateness score  (1=min to |  |
| `btipolpart` | BTI Political Participation score  (1=min to |  |
| `btiruleoflaw` | BTI Rule of law score  (1=min to |  |
| `btistability` | BTI Stability of democratic institutions score  (1=min |  |
| `btiintegration` | BTI Political & social integration score  (1=min to |  |
| `btimarket` | BTI Market Economy Status  (1=min to |  |
| `btigovindex` | BTI Governance Index  (1=min to |  |
| `btigoveperform` | BTI Governance Performance (1=min to |  |
| `btiregime` | BTI regime type (5 groups) [Bertelsmann Stiftung, |  |
| `regionWB` | _(未匹配)_ |  |
| `incomeWB` | _(未匹配)_ |  |
| `landWB` | _(未匹配)_ |  |
| `GDPpercap1` | GDP per capita, PPP (current international $) [World |  |
| `GDPpercap2` | GDP per capita, PPP (constant 2017 international $) |  |
| `giniWB` | _(未匹配)_ |  |
| `incrichest10p` | Income share held by richest 10 % [World Bank, |  |
| `popWB1990` | Population total (1990) [World Bank, 2019] |  |
| `popWB2000` | Population total (2000) [World Bank, 2019] |  |
| `popWB2019` | Population total (2019) [World Bank, 2019] |  |
| `lifeexpect` | Life expectancy at birth, total (years) [World Bank, |  |
| `popgrowth` | Population growth (annual %)  [World Bank, 2019] |  |
| `urbanpop` | Urban population (% of total population) [World |  |
| `laborforce` | Labor force, total  [World Bank, 2019] |  |
| `deathrate` | Death rate, crude (per 1,000 people) [World Bank, |  |
| `unemployfem` | Unemployment, female (% of female labor force) |  |
| `unemploymale` | Unemployment, male (% of male labor force) |  |
| `unemploytotal` | Unemployment, total (% of total labor force) |  |
| `accessclfuel` | Access to clean fuels and technologies for cooking (% |  |
| `accesselectr` | Access to electricity (% of population) [World Bank, |  |
| `renewelectr` | Renewable electricity output (% of total electricity |  |
| `co2emis` | CO2 emissions (kt) [World Bank, 2016] |  |
| `co2percap` | CO2 emissions (metric tons per capita)  [World Bank, |  |
| `easeofbusiness` | Ease of doing business index (1=most business- |  |
| `militaryexp` | Military expenditure (% of GDP)  [World Bank, |  |
| `Trade` | _(未匹配)_ |  |
| `healthexp` | Health expenditure (% of GDP)  [World Bank, 2017] |  |
| `educationexp` | Government expenditure on education (% of GDP) |  |
| `medageun` | Median age (years) [UNDESA, 2020] |  |
| `meanschooling` | Mean years of schooling (years) [UNESCO, 2018] |  |
| `educationHDI` | _(未匹配)_ |  |
| `GII` | Gender Inequality Index (GII) (0 to 1) [UNDP, 2018] |  |
| `DGI` | Gender Development Index (0 to 1) (GDI) [UNDP, |  |
| `womenparl` | Proportion of seats held by women in national |  |
| `hdi` | _(未匹配)_ |  |
| `incomeindexHDI` | _(未匹配)_ |  |
| `humanineqiality` | Coefficient of human inequality [UNDP, 2016-2018] |  |
| `lifeexpectHDI` | _(未匹配)_ |  |
| `homiciderate` | Homicide rate (per 100,000 people) [UNDP, 2012- |  |
| `Refugeesorigin` | _(未匹配)_ |  |
| `internetusers` | Internet users, total (% of population) [ITU, 2017- |  |
| `mobphone` | Mobile phone subscriptions (per 100 people) [ITU, |  |
| `migrationrate` | Net migration rate (per 1,000 people) [UNDESA, |  |
| `schoolgpi` | School enrollment, primary and secondary (gross), |  |
| `femchoutsch` | Children out of school, female (% of female primary |  |
| `choutsch` | Children out of school (% of primary school age) |  |
| `v2x_polyarchy` | Electoral democracy index  0 to 1 index  [V-Dem, |  |
| `v2x_libdem` | Liberal democracy index  0 to 1 index  [V-Dem, |  |
| `v2x_partipdem` | Participatory democracy index  0 to 1 index  [V-Dem, |  |
| `v2x_delibdem` | Deliberative democracy index  0 to 1 index  [V-Dem, |  |
| `v2x_egaldem` | Egalitarian democracy index 0 to 1 index  [V-Dem, |  |
| `v2x_freexp_altinf` | Freedom of Expression and Alternative Sources of |  |
| `v2x_frassoc_thick` | Freedom of association thick index 0 to 1 index  [V- |  |
| `v2xel_frefair` | Clean elections index 0 to 1 index  [V-Dem, 2019] |  |
| `v2xcl_rol` | Equality before the law and individual liberty index 0 |  |
| `v2x_cspart` | Civil society participation index 0 to 1 index  [V- |  |
| `v2xeg_eqdr` | Equal distribution of resources index 0 to 1 index  [V- |  |
| `v2excrptps` | Public sector corrupt exchanges [V-Dem, 2019] |  |
| `v2exthftps` | Public sector theft [V-Dem, 2019] |  |
| `v2juaccnt` | Judicial accountability [V-Dem, 2019] |  |
| `v2cltrnslw` | Transparent laws with predictable enforcement [V- |  |
| `v2clacjust` | Social class equality in respect for civil liberty [V- |  |
| `v2clsocgrp` | Social group equality in respect for civil liberties [V- |  |
| `v2clacfree` | Freedom of academic and cultural expression [V- |  |
| `v2clrelig` | Freedom of religion [V-Dem, 2019] |  |
| `v2csrlgrep` | Religious organization repression [V-Dem, 2019] |  |
| `v2mecenefm` | Government censorship effort --- Media [V-Dem, |  |
| `v2mecenefi` | Internet censorship effort [V-Dem, 2019] |  |
| `v2mebias` | Media bias [V-Dem, 2019] |  |
| `v2pepwrses` | Power distributed by socioeconomic position [V- |  |
| `v2pepwrgen` | Power distributed by gender [V-Dem, 2019] |  |
| `v2peedueq` | Educational equality [V-Dem, 2019] |  |
| `v2pehealth` | Health equality [V-Dem, 2019] |  |
| `v2peapsecon` | Access to public services distributed by socio- |  |
| `v2peasjsoecon` | Access to state jobs by socio-economic position [V- |  |
| `v2clgencl` | Gender equality in respect for civil liberties [V-Dem, |  |
| `v2peasjgen` | Access to state jobs by gender [V-Dem, 2019] |  |
| `v2peasbgen` | Access to state business opportunities by gender [V- |  |
| `v2cafres` | Freedom to research and teach [V-Dem, 2019] |  |
| `v2cafexch` | Freedom of academic exchange and dissemination [V- |  |
| `v2x_corr` | Political corruption index 0 to 1 index  [V-Dem, 2019] |  |
| `v2x_gender` | Women political empowerment index 0 to 1 index  [V- |  |
| `v2x_gencl` | Women civil liberties index 0 to 1 index  [V-Dem, |  |
| `v2x_genpp` | Women political participation index 0 to 1 index  [V- |  |
| `v2x_rule` | Rule of law index 0 to 1 index  [V-Dem, 2019] |  |
| `v2xcl_acjst` | Access to justice [V-Dem, 2019] |  |
| `td_voiacc` | _(未匹配)_ |  |
| `td_polstab` | _(未匹配)_ |  |
| `td_goveff` | _(未匹配)_ |  |
| `td_regqual` | _(未匹配)_ |  |
| `td_rulelaw` | _(未匹配)_ |  |
| `td_ctrlcorr` | _(未匹配)_ |  |
| `v2psbars` | Barriers to parties [V-Dem, 2018] |  |
| `v2psorgs` | Party organizations [V-Dem, 2018] |  |
| `v2psprbrch` | Party branches [V-Dem, 2018] |  |
| `v2psprlnks` | Party linkages [V-Dem, 2018] |  |
| `v2psplats` | Distinct party platforms [V-Dem, 2018] |  |
| `v2xnp_client` | Clientelism Index [V-Dem, 2018] |  |
| `v2xps_party` | Party institutionalization index [V-Dem, 2018] |  |

---

### 政党与选民模块(28 个)

政党属性(Global Party Survey):政党 ID、名称、左右、民粹类型、规模、选民分布(GPS 维度、WVS 衍生的选民位置)。缺失率约 96%,仅适用于投票子样本。

| 变量名 | Label | 备注 |
|---|---|---|
| `ID_GPS` | Party ID [Global Party Survey, 2018] |  |
| `ID_PartyFacts` | Party ID Party Facts |  |
| `Partyname` | _(未匹配)_ |  |
| `Partyabb` | _(未匹配)_ |  |
| `CPARTY` | ISO country + full party name (string text) [Global |  |
| `CPARTYABB` | ISO + party abbreviation [Global Party Survey, 2018] |  |
| `Type_Values` | The Party Values typology combines the categories of |  |
| `Type_Populism` | Type of Pluralist or Populist party by their rhetoric |  |
| `Type_Populist_Values` | _(未匹配)_ |  |
| `Type_Partysize_vote` | _(未匹配)_ |  |
| `Type_Partysize_seat` | _(未匹配)_ |  |
| `GPS_V4_Scale` | The party is leftwing (0) or rightwing (10) in their |  |
| `GPS_V6_Scale` | The party is liberal (0) or conservative (10) in their |  |
| `GPS_V8_Scale` | The party favors pluralist (0) or populist (10) rhetoric |  |
| `GPS_V9` | Salient is populist rhetoric for the party: No |  |
| `GPS_V10` | Issues: Party favors liberal (0) or restrictive (10) |  |
| `GPS_V11` | Issues: Party favors increased public spending (0) or |  |
| `GPS_V12` | Issues: Party favors (0) or opposes (10) environmental |  |
| `GPS_V13` | Issues: Party favors nationalism (0) or multilateralism |  |
| `GPS_V14` | Issues: Party favors (0) or opposes (10) women's |  |
| `GPS_V15` | Issues: Party favors (0) or opposes (10) ethnic |  |
| `GPS_V16` | Issues: Party respects (0) or undermines (10) liberal |  |
| `GPS_V17` | Issues: Party favors the distribution of public goods |  |
| `WVS_LR_PartyVoter` | _(未匹配)_ |  |
| `WVS_LibCon_PartyVoter` | _(未匹配)_ |  |
| `WVS_Polmistrust_PartyVoter` | _(未匹配)_ |  |
| `WVS_LR_MedianVoter` | _(未匹配)_ |  |
| `WVS_LibCon_MedianVoter` | _(未匹配)_ |  |

---

### 其他(8 个)

未归入上述章节的变量。

| 变量名 | Label | 备注 |
|---|---|---|
| `E_RESPINT` | Respondent interested during the interview |  |
| `E1_LITERACY` | Respondent´s literacy |  |
| `X003R` | Age recoded (6 intervals) |  |
| `X003R2` | Age recoded (3 intervals) |  |
| `X002_02B` | Respondent’s country of birth (ISO 3166-1/3 Alpha code) |  |
| `V002A_01` | Mother’s country of birth (ISO 3166-1/3 Alpha code) |  |
| `V001A_01` | Father’s country of birth (ISO 3166-1/3 Alpha code) |  |
| `compulseduc` | Compulsory education, duration (years) [World Bank, |  |

---

**合计变量数: 611**

---

## 四、数据来源(上下文/国家级指标)

上下文变量模块的外部数据来源:

| 来源 | 变量前缀 | 指标示例 |
|---|---|---|
| Freedom House (2019/2020) | `fh*`/`polregfh`/`freestfh`/`prf*`/`clf*` | 区域、政体类型、政治权利/公民自由评级 |
| Polity V (2018) | `democ`/`autoc`/`polity`/`durable` | 民主-独裁得分、政体持续时间 |
| V-Dem (最新) | `v2x_*`/`v2*` | 自由民主、参与民主、法治、腐败、表达自由等多维指数 |
| Bertelsmann 转型指数 | `bti*` | 民主 status、治理指数、市场、法治、稳定 |
| 世界银行 WGI | `td_*` | 话语问责、政治稳定、政府效能、监管质量、法治、腐败控制 |
| 世界银行宏观 | `GDPpercap*`/`giniWB`/`popWB*`/`incomeWB`/`regionWB`/`landWB` | 人均GDP、基尼、人口、收入层级 |
| UN/UNDP | `hdi`/`GII`/`DGI`/`meanschooling`/`educationHDI`/`lifeexpect*` | 人类发展指数、性别不平等、教育、预期寿命 |
| Global Party Survey (2018) | `GPS_*`/`Partyname`/`Partyabb` | 政党左右、民粹、规模、选民位置 |

> 这些国家级指标在数据集中为每个受访者行的常数,适合作为层级模型的二层变量。

---

## 五、未匹配变量说明

以下 32 个变量未能在 codebook 中直接匹配 label(多为小写国家级指标或表格内字段),含义可由变量名推断:

| 变量名 | 推断含义 |
|---|---|
| `S007` | 受访者唯一 ID |
| `N_REGION_NUTS1` | NUTS-1 地区编码 |
| `L_INTERVIEWER_NUMBER` | 访谈员编号 |
| `PWGHT` | 人口权重(Post-stratification weight) |
| `Q234AP` | Q234A 的 0-1 标准化版本 |
| `Q289CS9` | Q289 国家特定宗教派别选项 |
| `regionWB` | 世界银行地区分类 |
| `incomeWB` | 世界银行收入层级 |
| `landWB` | 世界银行土地/区域分类 |
| `giniWB` | 世界银行基尼系数 |
| `Trade` | 贸易(占 GDP 比重) |
| `educationHDI` | HDI 教育指数 |
| `hdi` | 人类发展指数 |
| `incomeindexHDI` | HDI 收入指数 |
| `lifeexpectHDI` | HDI 预期寿命指数 |
| `Refugeesorigin` | 难民来源国人数 |
| `td_voiacc` | WGI 话语问责 |
| `td_polstab` | WGI 政治稳定 |
| `td_goveff` | WGI 政府效能 |
| `td_regqual` | WGI 监管质量 |
| `td_rulelaw` | WGI 法治 |
| `td_ctrlcorr` | WGI 腐败控制 |
| `Partyname` | 政党名称(英文) |
| `Partyabb` | 政党缩写 |
| `Type_Populist_Values` | 民粹-多元政党价值观类型 |
| `Type_Partysize_vote` | 政党规模(得票) |
| `Type_Partysize_seat` | 政党规模(议席) |
| `WVS_LR_PartyVoter` | WVS 左右-政党选民 |
| `WVS_LibCon_PartyVoter` | WVS 自由保守-政党选民 |
| `WVS_Polmistrust_PartyVoter` | WVS 政治不信任-政党选民 |
| `WVS_LR_MedianVoter` | WVS 左右-中位选民 |
| `WVS_LibCon_MedianVoter` | WVS 自由保守-中位选民 |

---

## 六、使用建议

1. **价值观建模**:优先使用 `I_*` 系列、`SACSECVAL`、`RESEMAVAL`(已 0-1 标准化)。
2. **社会规范**:用 Q1–Q45、Q176–Q198(伦理弹性)、Q57–Q105(信任)。
3. **人口学控制变量**:Q260(性别)、Q261/Q262(年龄/教育)、Q288(阶层)、Q289(收入)。
4. **国家级指标**:V-Dem、Freedom House、WGI 已合并,无需另行匹配。
5. **跨国加权**:必用 `W_WEIGHT` + `S018`。
6. **政党模块**:缺失率约 96%,仅适用于投票子样本。
7. **完整变量清单**:见 `codebook_variables.json`(JSON 格式,含变量名/label/章节/页码)。

---

*报告生成于 2026-08-24,基于 WVS Wave 7 Codebook V6.0。*