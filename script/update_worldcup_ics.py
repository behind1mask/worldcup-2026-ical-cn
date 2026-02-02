import requests
from ics import Calendar
from pathlib import Path

SOURCE_ICS_URL = "https://ics.fixtur.es/v2/league/fifa-world-cup-2026.ics"
OUTPUT_FILE = Path("docs/worldcup_cn.ics")

COUNTRY_MAP = {
    "Mexico": "墨西哥🇲🇽",
    "South Africa": "南非🇿🇦",
    "South Korea": "韩国🇰🇷",

    "Canada": "加拿大🇨🇦",
    "Qatar": "卡塔尔🇶🇦",
    "Switzerland": "瑞士🇨🇭",

    "Brazil": "巴西🇧🇷",
    "Morocco": "摩洛哥🇲🇦",
    "Haiti": "海地🇭🇹",
    "Scotland": "苏格兰🏴󠁧󠁢󠁳󠁣󠁴󠁿",

    "United States": "美国🇺🇸",
    "Paraguay": "巴拉圭🇵🇾",
    "Australia": "澳大利亚🇦🇺",

    "Germany": "德国🇩🇪",
    "Curaçao": "库拉索🇨🇼",
    "Ivory Coast": "科特迪瓦🇨🇮",
    "Ecuador": "厄瓜多尔🇪🇨",  

    "Netherlands": "荷兰🇳🇱",
    "Japan": "日本🇯🇵",
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
    "Norway": "挪威🇳🇴",

    "Argentina": "阿根廷🇦🇷",  
    "Algeria": "阿尔及利亚🇩🇿",
    "Astria": "奥地利🇦🇹",
    "Jordan": "约旦🇯🇴",

    "Portugal": "葡萄牙🇵🇹",
    "Uzbekistan": "乌兹别克斯坦🇺🇿",
    "Colombia": "哥伦比亚🇨🇴",
  
    "England": "英格兰🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Croatia": "克罗地亚🇭🇷",
    "Ghana": "加纳🇬🇭",
    "Panama": "巴拿马🇵🇦",
}

raw_ics = requests.get(SOURCE_ICS_URL, timeout=30).text
calendar = Calendar(raw_ics)

for event in calendar.events:
    title = event.name
    for en, zh in COUNTRY_MAP.items():
        title = title.replace(en, zh)
    event.name = title.replace(" - ", " vs ")

OUTPUT_FILE.parent.mkdir(exist_ok=True)
OUTPUT_FILE.write_text(calendar.serialize(), encoding="utf-8")

print("iCal updated")
