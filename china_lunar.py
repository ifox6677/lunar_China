import datetime
import cnlunar

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

    while start_date < end_date:
        try:
            a = cnlunar.Lunar(start_date, godType='8char')

            solar_summary = f"{start_date.year}-{start_date.month:02d}-{start_date.day:02d}"
            lunar_month = a.lunarMonthCn
            lunar_day = a.lunarDayCn
            solar_terms = a.todaySolarTerms if a.todaySolarTerms != '无' else ''
            lunar_time = ', '.join(a.twohour8CharList)
            twelve_day_officer = '；'.join(a.get_today12DayOfficer()).replace(',', '').replace('；', '')

            chinese_zodiac = get_chinese_zodiac(a.lunarYear)
            chinese_zodiac_clash = a.chineseZodiacClash
            east_zodiac = a.todayEastZodiac
            eight_characters = ' '.join([a.year8Char, a.month8Char, a.day8Char, a.twohour8Char])

            fetal_god = a.get_fetalGod()

            elements_list = a.get_today5Elements()

            elements = ''.join([''.join(elem).replace(',', '').replace('(', '').replace(')', '').replace(' ', '') for elem in elements_list])

            twelve_day_officer = twelve_day_officer.replace("收青龙黄道日", " 收青龙黄道日").replace(";", "；").replace(",", "").replace("十二神", "").replace("成", "").replace("日", "")

            elements_with_commas = ', '.join([elements[i:i+5] for i in range(0, len(elements), 5)])

            summary = f"{lunar_day} {lunar_month} ({solar_terms} - {chinese_zodiac} {chinese_zodiac_clash} ({fetal_god}))"

            description = f"今日五行: ({elements_with_commas}); 时辰: {lunar_time.replace(' ', '')}; 今日十二神: {twelve_day_officer}"
            description += f"; 八字: ({eight_characters}); 星次: ({east_zodiac})"

            ics_event = f"BEGIN:VEVENT\nDTSTART;VALUE=DATE:{solar_summary}\nSUMMARY:{summary}\nDESCRIPTION:{description}\nEND:VEVENT\n"
            ics_data += ics_event

            start_date += datetime.timedelta(days=1)

        except ValueError:
            pass

    return f"BEGIN:VCALENDAR\nVERSION:2.0\n{ics_data}END:VCALENDAR"

year_to_convert = 2025 #生成开始年份
num_of_years = 5 # 想要生成的年数
ics_result = generate_lunar_calendar(year_to_convert, num_of_years)

with open(f"lunar_calendar_{year_to_convert}_to_{year_to_convert + num_of_years - 1}.ics", "w") as file:
    file.write(ics_result)

print(f"lunar_calendar_{year_to_convert}_to_{year_to_convert + num_of_years - 1}.ics 文件已生成")
