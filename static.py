# static.py 範例修改：
import requests
from bs4 import BeautifulSoup
import csv

# 設定目標網址
url = "https://www.books.com.tw/web/sys_saletopb/books/02/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 解析網頁中的商品項目
statics = soup.select("li.item")
static_data = []

for static in statics:
    name_tag = static.select_one("h4 a")
    author_tag = static.select_one(".msg a")

    # ✅ 處理價格：抓第二個 <b>
    price_bs = static.select("li.price_a b")
    if len(price_bs) >= 2:
        price = price_bs[1].text.strip()
    else:
        price = ""

    name = name_tag.text.strip() if name_tag else ""
    author = author_tag.text.strip() if author_tag else ""

    # 過濾全部都沒資料的項目
    if not name and not author and not price:
        continue

    static_data.append([name or "無資料", author or "無資料", price or "無價格"])

# 儲存 CSV，並且這裡保存到本地工作目錄
with open("static.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["書名", "作者", "價格"])
    writer.writerows(static_data)

print("爬蟲結果已儲存為 static.csv")
