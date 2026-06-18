import requests
from pathlib import Path
from icalendar import Calendar

SOURCE_ICS_URL = "https://ics.fixtur.es/v2/league/fifa-world-cup-2026.ics"
OUTPUT_FILE = Path("docs/worldcup_cn.ics")

COUNTRY_MAP = {
    "Mexico": "墨西哥🇲🇽",
    "South Africa": "南非🇿🇦",
    "South Korea": "韩国🇰🇷",
    "Czech Republic": "捷克🇨🇿",

    "Canada": "加拿大🇨🇦",
    "Bosnia and Herzegovina": "波黑🇧🇦",
    "Qatar": "卡塔尔🇶🇦",
    "Switzerland": "瑞士🇨🇭",

    "Brazil": "巴西🇧🇷",
    "Morocco": "摩洛哥🇲🇦",
    "Haiti": "海地🇭🇹",
    "Scotland": "苏格兰🏴󠁧󠁢󠁳󠁣󠁴󠁿",

    "United States": "美国🇺🇸",
    "Paraguay": "巴拉圭🇵🇾",
    "Australia": "澳大利亚🇦🇺",
    "Türkiye": "土耳其🇹🇷",
    "TÃ¼rkiye": "土耳其🇹🇷",

    "Germany": "德国🇩🇪",
    "Curaçao": "库拉索🇨🇼",
    "CuraÃ§ao": "库拉索🇨🇼",
    "Ivory Coast": "科特迪瓦🇨🇮",
    "Ecuador": "厄瓜多尔🇪🇨",

    "Netherlands": "荷兰🇳🇱",
    "Japan": "日本🇯🇵",
    "Sweden": "瑞典🇸🇪",
    "Tunisia": "突尼斯🇹🇳",

    "Belgium": "比利时🇧🇪",
    "Egypt": "埃及🇪🇬",
    "Iran": "伊朗🇮🇷",
    "New Zealand": "新西兰🇳🇿",

    "Spain": "西班牙🇪🇸",
    "Cape Verde": "佛得角🇨🇻",
    "Saudi Arabia": "沙特阿拉伯🇸🇦",
    "Uruguay": "乌拉圭🇺🇾",

    "France": "法国🇫🇷",
    "Senegal": "塞内加尔🇸🇳",
    "Iraq": "伊拉克🇮🇶",
    "Norway": "挪威🇳🇴",

    "Argentina": "阿根廷🇦🇷",
    "Algeria": "阿尔及利亚🇩🇿",
    "Austria": "奥地利🇦🇹",
    "Jordan": "约旦🇯🇴",

    "Portugal": "葡萄牙🇵🇹",
    "DR Congo": "刚果（金）🇨🇩",
    "Uzbekistan": "乌兹别克斯坦🇺🇿",
    "Colombia": "哥伦比亚🇨🇴",

    "England": "英格兰🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Croatia": "克罗地亚🇭🇷",
    "Ghana": "加纳🇬🇭",
    "Panama": "巴拿马🇵🇦",
}

SPECIAL_EVENT_MAP = {
    "World Cup Round of 32": "世界杯32强赛",
    "Start of the FIFA World Cup 2026 knockout stage.": "2026美加墨世界杯淘汰赛阶段开始。",

    "World Cup Round of 16": "世界杯16强赛",
    "Start of the FIFA World Cup 2026 Round of 16.": "2026美加墨世界杯16强赛开始。",

    "World Cup quarter-finals": "世界杯四分之一决赛",
    "Start of the FIFA World Cup 2026 quarter-finals.": "2026美加墨世界杯四分之一决赛开始。",

    "World Cup semi-finals": "世界杯半决赛",
    "Start of the FIFA World Cup 2026 semi-finals.": "2026美加墨世界杯半决赛开始。",

    "World Cup third-place match": "世界杯季军赛",
    "FIFA World Cup 2026 third-place play-off day.": "2026美加墨世界杯季军赛比赛日。",

    "World Cup final": "世界杯决赛",
    "FIFA World Cup 2026 final day.": "2026美加墨世界杯决赛比赛日。",
}

VENUE_MAP = {
    "Estadio Banorte": "阿兹特克体育场，墨西哥城，墨西哥",
    "Estadio Akron": "阿克伦球场，萨波潘，墨西哥",
    "BMO Field": "BMO球场，多伦多，加拿大",
    "SoFi": "SoFi体育场，英格尔坞德，美国",
    "Levi's": "李维斯体育场，圣克拉拉，美国",
    "MetLife": "大都会人寿体育场，东拉瑟福德，美国",
    "Gillette": "吉列体育场，福克斯伯勒，美国",
    "BC Place": "不列颠哥伦比亚体育馆，温哥华，加拿大",
    "NRG": "NRG体育场，休斯敦，美国",
    "AT&T": "AT&T体育场，阿灵顿，美国",
    "Lincoln Financial Field": "林肯金融球场，费城，美国",
    "Estadio BBVA": "BBVA体育场，瓜达卢佩，墨西哥",
    "Mercedes-Benz": "梅赛德斯-奔驰体育场，亚特兰大，美国",
    "Lumen Field": "流明球场，西雅图，美国",
    "Hard Rock": "硬石体育场，迈阿密加登斯，美国",
    "GEHA Field at Arrowhead": "箭头体育场，堪萨斯城，美国",
}

response = requests.get(SOURCE_ICS_URL, timeout=30)
response.raise_for_status()

calendar = Calendar.from_ical(response.content)

for component in calendar.walk():

    if component.name != "VEVENT":
        continue

    summary = str(component.get("SUMMARY", ""))
    description = str(component.get("DESCRIPTION", ""))
    location = str(component.get("LOCATION", ""))

   # 修复乱码
    try:
        summary = summary.encode("latin1").decode("utf-8")
    except:
        pass

    try:
        description = description.encode("latin1").decode("utf-8")
    except:
        pass

    try:
        location = location.encode("latin1").decode("utf-8")
    except:
        pass

    # 国家翻译
    for en, zh in COUNTRY_MAP.items():
        summary = summary.replace(en, zh)
        description = description.replace(en, zh)
        location = location.replace(en, zh)

    # 特殊赛事翻译
    for en, zh in SPECIAL_EVENT_MAP.items():
        summary = summary.replace(en, zh)
        description = description.replace(en, zh)

    # 美化
    summary = summary.replace(" - ", " vs ")
    
    # 场馆与地名翻译
    for en, zh in VENUE_MAP.items():
        summary = summary.replace(en, zh)
        description = description.replace(en, zh)
        location = location.replace(en, zh)

    # 删除原作者广告
    description = description.replace(
        "Calendar not up to date? Check https://fixtur.es/up-to-date?path=league/fifa-world-cup-2026",
        ""
    )

    description = description.replace(
        "Support Fixtur.es via Buy Me a Coffee https://buymeacoffee.com/fixtures",
        ""
    )

    description = description.strip()

    if description:
        description += "\n\n"

    description += (
        "☕ 觉得这个订阅对你有帮助？\n"
        "欢迎赞助支持后续维护与更新。\n\n"
        "支付宝：luyaoxiansen@foxmail.com"
    )

    component["SUMMARY"] = summary
    component["DESCRIPTION"] = description

    if location:
        component["LOCATION"] = location

# 日历名称
calendar["X-WR-CALNAME"] = "2026美加墨世界杯"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "wb") as f:
    f.write(calendar.to_ical())

print("World Cup iCal updated successfully.")
