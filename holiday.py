from lunardate import LunarDate
from datetime import datetime, timedelta


# 计算复活节的日期
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


# 辅助函数：计算星期天的日期
def get_nth_weekday(year, month, weekday, nth):
    date = datetime(year, month, 1)
    count = 0
    while count < nth:
        if date.weekday() == weekday:
            count += 1
        if count < nth:
            date += timedelta(days=1)
    return date


# 辅助函数：生成农历节日的公历日期
def lunar_to_solar(year, month, day):
    lunar_date = LunarDate(year, month, day)
    return lunar_date.toSolarDate()


# 辅助函数：添加节日到事件列表
def add_event(events, date, name):
    events.append((datetime.combine(date, datetime.min.time()), name))


# 生成农历和公历节日的日历
def generate_lunar_calendar(start_year, num_of_years):
    events = []
    
    for year in range(start_year, start_year + num_of_years):
        # 获取农历节日
        mid_autumn = lunar_to_solar(year, 8, 15)
        zhongyuan = lunar_to_solar(year, 7, 15)
        yuanxiao = lunar_to_solar(year, 1, 15)
        qixi = lunar_to_solar(year, 7, 7)
        spring_festival = lunar_to_solar(year, 1, 1)
        dragon_boat_festival = lunar_to_solar(year, 5, 5)
        double_ninth_festival = lunar_to_solar(year, 9, 9)
        laba_festival = lunar_to_solar(year, 12, 8)
        kitcheng_god_day = lunar_to_solar(year, 12, 24)
        xiaonian = lunar_to_solar(year, 12, 23)
        dongzhi = lunar_to_solar(year, 11, 10)

        # 计算除夕
        lunar_new_year = lunar_to_solar(year, 1, 1)
        chuxi_date = lunar_new_year - timedelta(days=1)

        # 公历节日
        tomb_sweeping_day = datetime(year, 4, 4)
        labor_day = datetime(year, 5, 1)
        national_day = datetime(year, 10, 1)
        father_day = get_nth_weekday(year, 6, 6, 1)  # 找到6月的第一个星期天（父亲节）
        mother_day = get_nth_weekday(year, 5, 6, 2)  # 找到5月的第二个星期天（母亲节）
        thanksgiving_day = get_nth_weekday(year, 11, 3, 4)  # 感恩节，11月的第四个星期四
        easter_date = easter(year)
        valentines_day = datetime(year, 2, 14)
        christmas_day = datetime(year, 12, 25)
        chirstmas_eve = datetime(year, 12, 24)
        halloween_day = datetime(year, 10, 31)
        newyear_day = datetime(year, 1, 1)
        youth_day = datetime(year, 5, 4)
        children_day = datetime(year, 6, 1)

        # 添加事件
        add_event(events, dongzhi, "冬至节")
        add_event(events, mid_autumn, "中秋节")
        add_event(events, zhongyuan, "中元节")
        add_event(events, yuanxiao, "元宵节")
        add_event(events, qixi, "七夕节")
        add_event(events, kitcheng_god_day, "灶君上天日")
        add_event(events, spring_festival, "春节")
        add_event(events, dragon_boat_festival, "端午节")
        add_event(events, tomb_sweeping_day, "清明节")
        add_event(events, double_ninth_festival, "重阳节(生日)")
        add_event(events, laba_festival, "腊八节")
        add_event(events, xiaonian, "小年")
        add_event(events, chuxi_date, "除夕")
        add_event(events, labor_day, "劳动节")
        add_event(events, youth_day, "青年节")
        add_event(events, children_day, "儿童节")
        add_event(events, national_day, "国庆节")
        add_event(events, father_day, "父亲节")
        add_event(events, mother_day, "母亲节")
        add_event(events, thanksgiving_day, "感恩节")
        add_event(events, easter_date, "复活节")
        add_event(events, valentines_day, "情人节")
        add_event(events, chirstmas_eve, "平安夜")
        add_event(events, christmas_day, "圣诞节")
        add_event(events, halloween_day, "万圣节")
        add_event(events, newyear_day, "元旦节")
    
    # 排序
    events.sort(key=lambda x: x[0])

    # 创建 iCalendar 数据
    ics_data = ""
    for event_date, event_name in events:
        event_start = event_date.strftime("%Y%m%d")
        event_end = (event_date + timedelta(days=1)).strftime("%Y%m%d")
        event = f"BEGIN:VEVENT\nSUMMARY:{event_name}\nDTSTART;VALUE=DATE:{event_start}\nDTEND;VALUE=DATE:{event_end}\nEND:VEVENT\n"
        ics_data += event

    ics_calendar = f"BEGIN:VCALENDAR\nVERSION:2.0\n{ics_data}END:VCALENDAR"
    return ics_calendar


# 使用示例
start_year = 2024
num_of_years = 10
ics_result = generate_lunar_calendar(start_year, num_of_years)

# 写入文件
with open("lunar_holidays.ics", "w") as file:
    file.write(ics_result)

print("Calendar generated: lunar_calendar.ics")
