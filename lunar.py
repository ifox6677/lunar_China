from skyfield.api import load, Topos
from datetime import datetime, timedelta, timezone
import cnlunar
import random
import time
import re

# 加载星历文件和时间
eph = load('de430.bsp')
earth = eph['earth']
sun = eph['sun']
moon = eph['moon']
observer = earth + Topos(latitude_degrees=0.0, longitude_degrees=0.0)
time_scale = load.timescale()

# 定义黄经差计算函数
def delta_l(t):
    T = time_scale.utc(datetime.fromtimestamp(t, tz=timezone.utc))  # 使用 datetime 处理
    _, l1, _ = earth.at(T).observe(sun).ecliptic_latlon()
    _, l2, _ = earth.at(T).observe(moon).ecliptic_latlon()
    return (l2.degrees - l1.degrees) % 360

# 定义生成农历日历的函数
def generate_lunar_calendar(start_year, num_of_years):
    ics_data = ""
    start_date = datetime(start_year, 1, 1)  # 使用 datetime
    end_date = start_date + timedelta(days=num_of_years * 365) 

    while start_date < end_date:
        try:
            a = cnlunar.Lunar(start_date, godType='8char')  # 使用 cnlunar 库
            timestamp = start_date.timestamp()
            delta_longitude = delta_l(timestamp)

            # 获取农历信息
            lunar_month = a.lunarMonthCn
            lunar_day = a.lunarDayCn
            solar_summary = f"{start_date.year}{start_date.month:02d}{start_date.day:02d}"
            solar_terms = a.todaySolarTerms if a.todaySolarTerms != '无' else ''
            
            lunar_time = ', '.join(a.twohour8CharList)
            chinese_zodiac = a.chineseYearZodiac
            elements_list = a.get_today5Elements()
            elements = ''.join([''.join(elem).replace(',', '').replace('(', '').replace(')', '').replace(' ', '') for elem in elements_list])
            elements_with_commas = ', '.join([elements[i:i+5] for i in range(0, len(elements), 5)])
            
            # 八字信息和吉凶
            eight_characters = ' '.join([a.year8Char, a.month8Char, a.day8Char, a.twohour8Char])
            lucky_god_str = ' '.join(a.get_luckyGodsDirection()) if isinstance(a.get_luckyGodsDirection(), list) else a.get_luckyGodsDirection()
            good_thing_str = ' '.join(a.goodThing) if isinstance(a.goodThing, list) else a.goodThing
            bad_thing_str = ' '.join(a.badThing) if isinstance(a.badThing, list) else a.badThing
            level_name = f"({''.join(re.findall('[\\u4e00-\\u9fff]', a.todayLevelName[:2]))}) {a.todayLevelName[3:]}"


            # 星体信息
            current_time = time_scale.utc(start_date.year, start_date.month, start_date.day)
            apparent_sun = observer.at(current_time).observe(sun).apparent()
            apparent_mercury = observer.at(current_time).observe(eph['mercury']).apparent()
            mercury_d = apparent_mercury.radec()[1]._degrees
            dec_sun = apparent_sun.radec()[1]._degrees

            # 调整黄经差
            moon_d = delta_longitude

            # 定义月相描述
            if moon_d < 15 or moon_d > 345:
                moon_phase = "新月"
            elif 75 <= moon_d < 105:
                moon_phase = "上弦月"
            elif 165 <= moon_d < 195:
                moon_phase = "满月"
            elif 255 <= moon_d < 285:
                moon_phase = "下弦月"
            elif 15 < moon_d < 75:
                moon_phase = "娥眉月"  # 新月到上弦月之间
            elif 105 < moon_d < 165:
                moon_phase = "盈凸月"  # 上弦月到满月之间
            elif 195 < moon_d < 255:
                moon_phase = "亏凸月"  # 满月到下弦月之间
            else:
                moon_phase = "残月"    # 下弦月到新月之间

            # 生成事件描述
            description = (
                f"太阳黄道: {dec_sun:.1f} 月亮相位: {moon_d:.1f} {a.starZodiac} "
                f"\\n八字: {eight_characters} \\n今日六合: {a.zodiacMark6} \\n生肖冲煞: {a.chineseZodiacClash} "
                f"\\n今日胎神: {a.get_fetalGod()} \\n今日五行: {elements_with_commas} \\n时辰: {lunar_time.replace(' ', '')} "
                f"\\n十二神: {'；'.join(a.get_today12DayOfficer()).replace(',', '').replace('；', '')} \\n宜: {good_thing_str} "
                f"\\n忌: {bad_thing_str} \\n宜忌等第: {level_name} \\n星次: {a.todayEastZodiac} \\n吉神方位: {lucky_god_str}"
            )

            # 生成唯一标识和ICS事件
            unique_identifier = f"{random.randint(1, 100000)}@zhangjq.com"
            solar_end_day = (start_date + timedelta(days=1)).strftime("%Y%m%d")
            summary_0 = f"{lunar_day} {lunar_month} {chinese_zodiac}年 {solar_terms} {moon_phase}"

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
year_to_convert = datetime.now().year

# 你想转换的年份数
num_of_years = 2

# 调用生成函数
ics_result = generate_lunar_calendar(year_to_convert, num_of_years)

filename = f"lunar_calendar.ics"
with open(filename, "w", encoding="utf-8") as file:
    file.write(ics_result)

print(f"文件 lunar_calendar_{year_to_convert}_to_{year_to_convert + num_of_years - 1}.ics 已生成")
