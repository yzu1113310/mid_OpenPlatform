# api.py 範例修改：
import requests
import csv
import os

# API 金鑰
API_KEY = 'a22d2da119614959557d69b52fad7ab1'

# 中英文城市對照表
CITIES = {
    "Taipei,TW": "台北",
    "Kaohsiung,TW": "高雄",
    "Taichung,TW": "台中",
    "Tainan,TW": "台南",
    "Hsinchu,TW": "新竹",
    "Keelung,TW": "基隆",
    "Taitung City,TW": "台東",
    "Hualien City,TW": "花蓮",
    "Chiayi City,TW": "嘉義",
    "Pingtung,TW": "屏東",
    "Yilan,TW": "宜蘭",
    "Changhua,TW": "彰化"
}

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(city_query, city_name_zh):
    params = {
        'q': city_query,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'zh_tw'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        return [city_name_zh, temperature, humidity, description]
    else:
        print(f"❌ 無法取得 {city_query} 資料：{data.get('message', '未知錯誤')}")
        return None

def save_to_csv(data, filename='api.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['城市', '氣溫(°C)', '濕度(%)', '天氣描述'])
        for entry in data:
            if entry:
                writer.writerow(entry)

# 主程式
if __name__ == '__main__':
    all_weather_data = []
    for city_query, city_name_zh in CITIES.items():
        result = fetch_weather_data(city_query, city_name_zh)
        if result:
            all_weather_data.append(result)

    save_to_csv(all_weather_data)
    print("✅ 天氣資料已儲存（中文城市名）至 api.csv")
