import requests
from ics import Calendar
from pathlib import Path

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

raw_ics = requests.get(SOURCE_ICS_URL, timeout=30).text
calendar = Calendar(raw_ics)

for event in calendar.events:

    title = event.name or ""
    description = event.description or ""
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

    # ===== 修复乱码 =====
    try:
        title = title.encode('latin1').decode('utf-8')
    except:
        pass

    try:
        description = description.encode('latin1').decode('utf-8')
    except:
        pass

    # ===== 国家翻译 =====
    for en, zh in COUNTRY_MAP.items():
        title = title.replace(en, zh)
        description = description.replace(en, zh)

    # ===== 特殊赛事翻译 =====
    for en, zh in SPECIAL_EVENT_MAP.items():
        title = title.replace(en, zh)
        description = description.replace(en, zh)

    # ===== 美化显示 =====
    title = title.replace(" - ", " vs ")

    event.name = title
    event.description = description

# ===== 序列化 =====
ics_content = calendar.serialize()

# ===== 日历名称 =====
lines = [
    line for line in ics_content.splitlines()
    if not line.strip().upper().startswith('X-WR-CALNAME:')
]

new_lines = []
found_vcalendar = False

for line in lines:
    new_lines.append(line)

    if line.strip() == 'BEGIN:VCALENDAR' and not found_vcalendar:
        new_lines.append('X-WR-CALNAME:2026美加墨世界杯')
        found_vcalendar = True

new_ics_content = '\n'.join(new_lines)

# ===== 输出文件 =====
OUTPUT_FILE.parent.mkdir(exist_ok=True)
OUTPUT_FILE.write_text(new_ics_content, encoding="utf-8")

print("iCal updated")
