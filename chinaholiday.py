from lunardate import LunarDate
from datetime import datetime, timedelta

def generate_lunar_calendar(start_year, num_of_years):
    end_year = start_year + num_of_years - 1
    events = []

    for year in range(start_year, end_year + 1):
        mid_autumn = LunarDate(year, 8, 15)
        zhongyuan = LunarDate(year, 7, 15)
        yuanxiao = LunarDate(year, 1, 15)
        qixi = LunarDate(year, 7, 7)
        spring_festival = LunarDate(year, 1, 1)
        dragon_boat_festival = LunarDate(year, 5, 5)
        double_ninth_festival = LunarDate(year, 9, 9)
        laba_festival = LunarDate(year, 12, 8)
        kitcheng_god_day = LunarDate(year, 12, 24)
        xiaonian = LunarDate(year, 12, 23)
        dongzhi = LunarDate(year, 11, 10)

        dongzhi_solar = dongzhi.toSolarDate()
        mid_autumn_solar = mid_autumn.toSolarDate()
        zhongyuan_solar = zhongyuan.toSolarDate()
        yuanxiao_solar = yuanxiao.toSolarDate()
        qixi_solar = qixi.toSolarDate()
        spring_festival_solar = spring_festival.toSolarDate()
        dragon_boat_festival_solar = dragon_boat_festival.toSolarDate()
        # 注意：清明节是公历节日
        tomb_sweeping_day_solar = datetime(year, 4, 4)
        double_ninth_festival_solar = double_ninth_festival.toSolarDate()
        laba_festival_solar = laba_festival.toSolarDate()
        kitcheng_god_day_solar = kitcheng_god_day.toSolarDate()
        xiaonian_solar = xiaonian.toSolarDate()

        # 农历除夕日期
        lunar_new_year = LunarDate(year, 1, 1).toSolarDate()
        chuxi_date = lunar_new_year - timedelta(days=1)  # 农历新年前一天

        # 父亲节和母亲节
        labor_day = datetime(year, 5, 1)
        national_day = datetime(year, 10, 1)
        father_day = datetime(year, 6, 1)
        while father_day.weekday() != 6:
            father_day += timedelta(days=1)
        mother_day = datetime(year, 5, 1)
        count_mother = 0
        while count_mother < 2:
            mother_day += timedelta(days=1)
            if mother_day.weekday() == 6:
                count_mother += 1

        # 感恩节、复活节、情人节、圣诞节和万圣节
        thanksgiving_day = datetime(year, 11, 1)
        while thanksgiving_day.weekday() != 3:  # 感恩节在每年的11月的第四个星期四
            thanksgiving_day += timedelta(days=1)
        easter_date = easter(year)  # 复活节日期需要计算
        valentines_day = datetime(year, 2, 14)  # 情人节
        christmas_day = datetime(year, 12, 25)  # 圣诞节
        chirstmas_eve =datetime(year, 12, 24)
        halloween_day = datetime(year, 10, 31)  # 万圣节
        newyear_day = datetime(year, 1, 1)
        youth_day = datetime(year, 5, 4)
        children_day = datetime(year, 6,1)

        events.append((datetime.combine(dongzhi_solar, datetime.min.time()), "冬至节"))
        events.append((datetime.combine(mid_autumn_solar, datetime.min.time()), "中秋节"))
        events.append((datetime.combine(zhongyuan_solar, datetime.min.time()), "中元节"))
        events.append((datetime.combine(yuanxiao_solar, datetime.min.time()), "元宵节"))
        events.append((datetime.combine(qixi_solar, datetime.min.time()), "七夕节"))
        events.append((datetime.combine(kitcheng_god_day_solar, datetime.min.time()), "灶君上天日"))
        events.append((datetime.combine(spring_festival_solar, datetime.min.time()), "春节"))
        events.append((datetime.combine(dragon_boat_festival_solar, datetime.min.time()), "端午节"))
        events.append((tomb_sweeping_day_solar, "清明节"))  # 这里是公历日期
        events.append((datetime.combine(double_ninth_festival_solar, datetime.min.time()), "重阳节"))
        events.append((datetime.combine(laba_festival_solar, datetime.min.time()), "腊八节"))
        events.append((datetime.combine(xiaonian_solar, datetime.min.time()), "小年"))
        events.append((datetime.combine(chuxi_date, datetime.min.time()), "除夕"))
        events.append((labor_day, "劳动节"))
        events.append((youth_day, "青年节"))
        events.append((children_day, "儿童节"))
        events.append((national_day, "国庆节"))
        events.append((father_day, "父亲节"))
        events.append((mother_day, "母亲节"))
        events.append((thanksgiving_day, "感恩节"))
        events.append((easter_date, "复活节"))
        events.append((valentines_day, "情人节"))
        events.append((chirstmas_eve, "平安夜"))
        events.append((christmas_day, "圣诞节"))
        events.append((halloween_day, "万圣节"))
        events.append((newyear_day, "元旦节"))

    events.sort(key=lambda x: x[0])

    ics_data = ""
    for event_date, event_name in events:
        event_start = event_date.strftime("%Y%m%d")
        event_end = (event_date + timedelta(days=1)).strftime("%Y%m%d")
        event = f"BEGIN:VEVENT\nSUMMARY:{event_name}\nDTSTART;VALUE=DATE:{event_start}\nDTEND;VALUE=DATE:{event_end}\nEND:VEVENT\n"
        ics_data += event

    ics_calendar = f"BEGIN:VCALENDAR\nVERSION:2.0\n{ics_data}END:VCALENDAR"
    return ics_calendar

# 计算复活节日期的函数
def easter(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(year, month, day)

# Example usage:
start_year = 2023
num_of_years = 5
ics_result = generate_lunar_calendar(start_year, num_of_years)

# Write the result to a file
with open("lunar_calendar.ics", "w") as file:
    file.write(ics_result)

print("Calendar generated: lunar_calendar.ics")