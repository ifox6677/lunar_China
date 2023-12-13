import datetime
import cnlunar
import re

def get_chinese_zodiac(year):
    zodiacs = {
        0: '猴', 1: '鸡', 2: '狗', 3: '猪', 4: '鼠', 5: '牛', 
        6: '虎', 7: '兔', 8: '龙', 9: '蛇', 10: '马', 11: '羊'
    }
    zodiac_index = (year - 1900) % 12
    return zodiacs[zodiac_index]

def generate_lunar_calendar(start_year, num_of_years):
    ics_data = ""

    start_date = datetime.datetime(start_year, 1, 1)
    end_date = start_date + datetime.timedelta(days=num_of_years * 365)

    month_sizes = {
        "正月": "正月大",
        "二月": "二月平",
        "三月": "三月大",
        "四月": "四月小",
        "五月": "五月大",
        "六月": "六月小",
        "七月": "七月大",
        "八月": "八月大",
        "九月": "九月小",
        "十月": "十月大",
        "冬月": "冬月小",
        "腊月": "腊月大"
    }

    while start_date < end_date:
        try:
            a = cnlunar.Lunar(start_date, godType='8char')

            solar_summary = f"{start_date.year}-{start_date.month:02d}-{start_date.day:02d}"
            lunar_month = a.lunarMonthCn[:-1]
            lunar_day = a.lunarDayCn
            
            solar_terms = a.todaySolarTerms if a.todaySolarTerms != '无' else ''
            lunar_time = ', '.join(a.twohour8CharList[:-1])
            zodiac_mark6 = a.zodiacMark6
            twelve_day_officer = '；'.join(a.get_today12DayOfficer()).replace(',', '').replace('；', '')

            matched_chars = re.findall('[\u4e00-\u9fff]', a.todayLevelName[:2])
            level_name = '(' + ''.join(matched_chars) + ')'

            chinese_zodiac = get_chinese_zodiac(a.lunarYear)
            chinese_zodiac_clash = a.chineseZodiacClash
            east_zodiac = a.todayEastZodiac

            eight_characters = ' '.join([a.year8Char, a.month8Char, a.day8Char, a.twohour8Char])

            fetal_god = a.get_fetalGod()
            lucky_god = a.get_luckyGodsDirection()
            elements_list = a.get_today5Elements()

            elements = ''.join([''.join(elem).replace(',', '').replace('(', '').replace(')', '').replace(' ', '') for elem in elements_list])

            twelve_day_officer = twelve_day_officer.replace("收青龙黄道日", " 收青龙黄道日").replace(";", "；").replace(",", "").replace("十二神", "")

            elements_with_commas = ', '.join([elements[i:i+5] for i in range(0, len(elements), 5)])

            if isinstance(a.goodThing, list):
                good_thing_str = ' '.join(a.goodThing)
            else:
                good_thing_str = a.goodThing

            if isinstance(a.badThing, list):
                bad_thing_str = ' '.join(a.badThing)
            else:
                bad_thing_str = a.badThing

            if isinstance(lucky_god, list):
                lucky_god_str = ' '.join(lucky_god)
            else:
                lucky_god_str = lucky_god

            if lunar_month in month_sizes:
                lunar_month = month_sizes[lunar_month]

            summary = f"{lunar_day} {lunar_month}  {chinese_zodiac}年 {solar_terms} "

            description = f"今日六合: {zodiac_mark6}\\n生肖冲煞: {chinese_zodiac_clash}\\n今日胎神: {fetal_god}\\n今日五行: {elements_with_commas}; \\n时辰: {lunar_time.replace(' ', '')}; \\n十二神: {twelve_day_officer}"
            description += f"; \\n八字: {eight_characters}; \\n宜: {good_thing_str};\\n 忌: {bad_thing_str};\\n宜忌等第: {level_name} {a.todayLevelName[3:]}\\n星次: {east_zodiac}\\n吉神方位: {lucky_god_str}"

            ics_event = f"BEGIN:VEVENT\nDTSTART;VALUE=DATE:{solar_summary}\nSUMMARY:{summary}\nDESCRIPTION:{description}\nEND:VEVENT\n"
            ics_data += ics_event

            start_date += datetime.timedelta(days=1)

        except ValueError:
            pass

    return f"BEGIN:VCALENDAR\nVERSION:2.0\n{ics_data}END:VCALENDAR"

year_to_convert = 2023  # 生成开始年份
num_of_years = 3  # 想要生成的年数
ics_result = generate_lunar_calendar(year_to_convert, num_of_years)

with open(f"lunar_calendar_{year_to_convert}_to_{year_to_convert + num_of_years - 1}.ics", "w") as file:
    file.write(ics_result)

print(f"lunar_calendar_{year_to_convert}_to_{year_to_convert + num_of_years - 1}.ics 文件已生成")

