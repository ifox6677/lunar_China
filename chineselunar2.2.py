from skyfield.api import load, Topos
from datetime import datetime, timedelta, timezone
from lunardate import LunarDate
import numpy as np
import pytz
import cnlunar
import re
import time
import random

# 加载星历文件和时间
eph = load('de430.bsp')
earth = eph['earth']
sun = eph['sun']
moon = eph['moon']
observer = earth + Topos(latitude_degrees=0.0, longitude_degrees=0.0)
time_scale = load.timescale()

# 定义黄经差计算函数
def delta_l(t):
    T = time_scale.utc(datetime.fromtimestamp(t, tz=timezone.utc))
    _, l1, _ = earth.at(T).observe(sun).ecliptic_latlon()
    _, l2, _ = earth.at(T).observe(moon).ecliptic_latlon()
    return (l2.degrees - l1.degrees) % 360

# 定义生成农历日历的函数
def generate_lunar_calendar(start_year, num_of_years):
    ics_data = ""
    start_date = datetime(start_year, 1, 1)
    end_date = start_date + timedelta(days=num_of_years * 365)

    month_sizes = {
        "正月": "正月大", "二月": "二月平", "三月": "三月大", "四月": "四月小",
        "五月": "五月大", "六月": "六月小", "七月": "七月大", "八月": "八月大",
        "九月": "九月小", "十月": "十月大", "冬月": "冬月小", "腊月": "腊月大"
    }

    while start_date < end_date:
        try:
            a = cnlunar.Lunar(start_date, godType='8char')
            timestamp = start_date.timestamp()
            delta_longitude = delta_l(timestamp)

            # 获取农历信息
            lunar_month = month_sizes.get(a.lunarMonthCn[:-1], a.lunarMonthCn)
            lunar_day = a.lunarDayCn
            solar_summary = f"{start_date.year}{start_date.month:02d}{start_date.day:02d}"
            solar_terms = a.todaySolarTerms if a.todaySolarTerms != '无' else ''
            
            lunar_time = ', '.join(a.twohour8CharList[:-1])
            chinese_zodiac = a.chineseYearZodiac
            elements_list = a.get_today5Elements()
            elements = ''.join([''.join(elem).replace(',', '').replace('(', '').replace(')', '').replace(' ', '') for elem in elements_list])
            elements_with_commas = ', '.join([elements[i:i+5] for i in range(0, len(elements), 5)])
            
            # 八字信息和吉凶
            eight_characters = ' '.join([a.year8Char, a.month8Char, a.day8Char, a.twohour8Char])
            lucky_god_str = ' '.join(a.get_luckyGodsDirection()) if isinstance(a.get_luckyGodsDirection(), list) else a.get_luckyGodsDirection()
            good_thing_str = ' '.join(a.goodThing) if isinstance(a.goodThing, list) else a.goodThing
            bad_thing_str = ' '.join(a.badThing) if isinstance(a.badThing, list) else a.badThing
            level_name = f"({''.join(re.findall('[\u4e00-\u9fff]', a.todayLevelName[:2]))}) {a.todayLevelName[3:]}"

            # 星体信息
            current_time = time_scale.utc(start_date.year, start_date.month, start_date.day)
            apparent_sun = observer.at(current_time).observe(sun).apparent()
            apparent_mercury = observer.at(current_time).observe(eph['mercury']).apparent()
            mercury_d = apparent_mercury.radec()[1]._degrees
            dec_sun = apparent_sun.radec()[1]._degrees

            # 调整黄经差
            moon_d = (360 - delta_longitude) if delta_longitude > 180 else delta_longitude

            # 生成事件描述
            description = (
                f"水星黄经: ({mercury_d:.2f}) {a.starZodiac} \\n太阳黄道: {dec_sun:.3f} 月亮相位: {moon_d:.2f} "
                f"\\n八字: {eight_characters} \\n今日六合: {a.zodiacMark6} \\n生肖冲煞: {a.chineseZodiacClash} "
                f"\\n今日胎神: {a.get_fetalGod()} \\n今日五行: {elements_with_commas} \\n时辰: {lunar_time.replace(' ', '')} "
                f"\\n十二神: {'；'.join(a.get_today12DayOfficer()).replace(',', '').replace('；', '')} \\n宜: {good_thing_str} "
                f"\\n忌: {bad_thing_str} \\n宜忌等第: {level_name} \\n星次: {a.todayEastZodiac} \\n吉神方位: {lucky_god_str}"
            )

            # 生成唯一标识和ICS事件
            unique_identifier = f"{random.randint(1, 100000)}@zhangjq.com"
            solar_end_day = (start_date + timedelta(days=1)).strftime("%Y%m%d")
            summary_0 = f"{lunar_day} {lunar_month} {chinese_zodiac}年 {solar_terms}"

            ics_event = (
                f"BEGIN:VEVENT\nUID:{unique_identifier}\nDTSTART;VALUE=DATE:{solar_summary}\n"
                f"DTEND;VALUE=DATE:{solar_end_day}\nSUMMARY:{summary_0}\nDESCRIPTION:{description}\nEND:VEVENT\n"
            )

            ics_data += ics_event
            start_date += timedelta(days=1)

        except ValueError:
            start_date += timedelta(days=1)  # 跳过无效日期

    return f"BEGIN:VCALENDAR\nVERSION:2.0\n{ics_data}END:VCALENDAR"

# 生成农历日历文件
year_to_convert = 2025
num_of_years = 8
ics_result = generate_lunar_calendar(year_to_convert, num_of_years)

with open(f"lunar_calendar_{year_to_convert}_to_{year_to_convert + num_of_years - 1}.ics", "w") as file:
    file.write(ics_result)

print(f"文件 lunar_calendar_{year_to_convert}_to_{year_to_convert + num_of_years - 1}.ics 已生成")
