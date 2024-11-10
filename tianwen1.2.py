import uuid
import pytz
from skyfield.api import load, Topos
from skyfield import almanac
from datetime import datetime, timedelta
from icalendar import Calendar, Event

# 加载天体历表
eph = load('de430.bsp') 
ts = load.timescale()

# 初始化日历对象
calendar = Calendar()

# 存储所有事件的列表
events_list = []

# 设置时间范围
start_time = ts.utc(datetime.utcnow().year)
end_time = ts.utc(datetime.utcnow().year + 10)

# 定义观察位置（用于逆行计算）
observer_location = Topos(latitude_degrees=39.9042, longitude_degrees=116.4074)


# 设置中国时间（CST）
china_tz = pytz.timezone('Asia/Shanghai')

# 逆行事件判定函数，记录逆行期间的黄道值
def find_retrograde(planet, name):
    in_retrograde = False
    current_time = start_time
    while current_time < end_time:
        previous_time = current_time - timedelta(days=1)
        previous_longitude = eph['earth'].at(previous_time).observe(planet).apparent().ecliptic_latlon()[1].degrees
        current_longitude = eph['earth'].at(current_time).observe(planet).apparent().ecliptic_latlon()[1].degrees

        if not in_retrograde and current_longitude < previous_longitude:
            # 逆行开始
            in_retrograde = True
            retro_start = current_time.utc_datetime().replace(tzinfo=pytz.utc).astimezone(china_tz)  # 转换为中国时间
            retro_start_longitude = current_longitude
            print(f"{name}逆行开始: {retro_start}, 黄道值: {retro_start_longitude}")

        elif in_retrograde and current_longitude > previous_longitude:
            # 逆行结束
            in_retrograde = False
            retro_end = current_time.utc_datetime().replace(tzinfo=pytz.utc).astimezone(china_tz)  # 转换为中国时间
            retro_end_longitude = current_longitude
            description = f"{name}逆行：从 {retro_start.strftime('%Y-%m-%d')} 到 {retro_end.strftime('%Y-%m-%d')} 开始黄道值: {retro_start_longitude:.2f}°, 结束黄道值: {retro_end_longitude:.2f}°"
            print(description)

            # 添加逆行事件到事件列表
            event = Event()
            event.add('summary', f'{name}逆行')
            event.add('dtstart', retro_start.date())  # 使用日期
            event.add('dtend', retro_end.date())  # 使用日期
            event.add('description', description)
            event.add('uid', str(uuid.uuid4()))  # 为每个事件添加UID
            events_list.append(event)

        # 增加一天
        current_time = current_time + timedelta(days=1)

# 超级月亮判定函数，记录距离和相位
def find_super_moons():
    moon = eph['moon']
    earth = eph['earth']
    current_time = start_time

    while current_time < end_time:
        apparent_moon = earth.at(current_time).observe(moon).apparent()
        distance_km = apparent_moon.distance().km

        # 判断超级月亮条件
        if distance_km < 357000:
            phase = almanac.moon_phase(eph, current_time).degrees  # 相位计算
            phase_name = "满月" if abs(phase - 180) < 10 else "新月" if phase < 10 or phase > 350 else "其他"
            event_start = current_time.utc_datetime().replace(tzinfo=pytz.utc).astimezone(china_tz)  # 转换为中国时间
            description = f"超级{phase_name}：距离 {distance_km:.0f} 公里，相位 {phase:.1f}°"
            print(description)

            # 添加超级月亮事件到事件列表
            event = Event()
            event.add('summary', f'超级{phase_name}')
            event.add('dtstart', event_start.date())  # 使用日期
            event.add('dtend', event_start.date())  # 使用日期
            event.add('description', description)
            event.add('uid', str(uuid.uuid4()))  # 为每个事件添加UID
            events_list.append(event)

        # 增加一周以减少计算量
        current_time = current_time + timedelta(days=1)

# 计算水星和金星逆行数据
find_retrograde(eph['mercury'], "水星")
find_retrograde(eph['venus'], "金星")

# 计算超级月亮数据
find_super_moons()

# 计算春分、夏至、秋分和冬至节气数据
seasons = almanac.seasons(eph)
t, season = almanac.find_discrete(start_time, end_time, seasons)
season_names = ["春分", "夏至", "秋分", "冬至"]

for ti, s in zip(t, season):
    event_start = ti.utc_datetime().replace(tzinfo=pytz.utc).astimezone(china_tz)  # 转换为中国时间
    event_end = event_start + timedelta(days=1)
    # 计算节气时刻的黄道值
    sun_position = eph['earth'].at(ti).observe(eph['sun']).apparent()
    ecliptic_longitude = sun_position.ecliptic_latlon()[1].degrees
    
    description = f"{season_names[s]}发生时间：{event_start.strftime('%Y-%m-%d %H:%M:%S')} CST 太阳黄道：{ecliptic_longitude:.2f}° "
    print(description)

    # 添加节气事件到事件列表
    event = Event()
    event.add('summary', season_names[s])
    event.add('dtstart', event_start.date())  # 使用日期
    event.add('dtend', event_end.date())  # 使用日期
    event.add('description', description)
    event.add('uid', str(uuid.uuid4()))  # 为每个事件添加UID
    events_list.append(event)

# 将所有事件按开始时间排序
events_list.sort(key=lambda e: e.get('dtstart').dt)

# 将事件按顺序添加到日历
for event in events_list:
    calendar.add_component(event)

# 导出到ICS文件
with open('astronomical_events.ics', 'wb' encoding="utf-8") as f:
    f.write(calendar.to_ical())

print("事件已写入 'astronomical_events.ics'")
