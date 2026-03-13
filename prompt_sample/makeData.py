import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 設定基本參數
np.random.seed(42)
num_customers = 2500  # 增加客戶數，總筆數約 3500 筆

# 基礎設定
first_names = ["大明", "小華", "美麗", "建國", "雅婷", "俊傑", "宇軒", "子豪", "思涵", "志明", "春嬌", "柏翰", "佳穎", "怡君", "家豪", "淑芬", "志偉", "雅惠", "俊宏", "美玲", "志豪", "雅玲", "文雄", "淑惠", "俊賢", "佩君", "雅芳", "建志", "淑娟", "志強", "雅琪", "文傑", "美惠", "俊宇", "佩玲"]
last_names = ["王", "林", "張", "陳", "李", "吳", "趙", "劉", "黃", "周", "徐", "朱", "孫", "馬", "胡", "郭", "何", "高", "羅", "鄭"]
categories = ["3C電子", "家居用品", "辦公耗材", "美妝保養", "戶外休閒", "食品飲料", "服飾配件", "圖書文具", "運動用品", "寵物用品", "汽機車配件", "保健食品"]
levels = ["VIP", "一般", "VVIP"]
channels = ["自然搜尋", "FB廣告", "Google Ads", "KOL推薦", "線下實體店"]
cities = ["台北市", "新北市", "桃園市", "台中市", "台南市", "高雄市", "其他"]
statuses = ["已完成", "退貨", "取消"]

# 定價與成本率 (同前，略作精簡)
prices = {
    "3C電子": [1290, 2990, 5990, 12900, 35900], "家居用品": [450, 780, 1200, 2500, 4800],
    "辦公耗材": [150, 299, 450, 890, 1500], "美妝保養": [650, 1200, 2200, 4500],
    "戶外休閒": [1200, 2500, 4800, 12000], "食品飲料": [150, 280, 450, 890],
    "服飾配件": [490, 890, 1590, 2990, 5500], "圖書文具": [280, 450, 680, 1200],
    "運動用品": [890, 1590, 2990, 5500], "寵物用品": [299, 550, 990, 1890],
    "汽機車配件": [590, 1200, 2800, 5500], "保健食品": [590, 980, 1680, 2980]
}
cost_rates = {
    "3C電子": (0.75, 0.85), "家居用品": (0.50, 0.65), "辦公耗材": (0.60, 0.75), "美妝保養": (0.25, 0.45),
    "戶外休閒": (0.50, 0.70), "食品飲料": (0.60, 0.80), "服飾配件": (0.30, 0.45), "圖書文具": (0.55, 0.70),
    "運動用品": (0.50, 0.65), "寵物用品": (0.40, 0.60), "汽機車配件": (0.60, 0.75), "保健食品": (0.25, 0.40)
}

# 產生具有趨勢性的日期 (2024-2025)
def generate_trend_date():
    year = random.choices([2024, 2025], weights=[0.4, 0.6])[0] # 2025 業績成長
    month = random.choices(range(1, 13), weights=[1, 1, 1.1, 1, 1.2, 1.2, 1, 1, 1.5, 2, 3, 2.5])[0] # Q4 旺季爆發
    day = random.randint(1, 28)
    return datetime(year, month, day)

data = []
customers = []

# 建立客戶基本資料
for cid in range(1, num_customers + 1):
    customer_id = f"CUST-{cid:04d}"
    name = random.choice(last_names) + random.choice(first_names)
    phone_num = f"09{random.randint(10,99)}{random.randint(100,999)}{random.randint(100,999)}"
    phone = f"{phone_num[:4]}-{phone_num[4:7]}-{phone_num[7:]}" if random.random() > 0.3 else phone_num
    level = random.choices(levels, weights=[0.15, 0.75, 0.10])[0]
    city = random.choices(cities, weights=[0.3, 0.2, 0.1, 0.15, 0.05, 0.15, 0.05])[0]
    customers.append({"id": customer_id, "name": name, "phone": phone, "level": level, "city": city})

order_seq = 1
for cust in customers:
    order_count = random.randint(1, 4) if cust["level"] == "一般" else random.randint(5, 12)
    
    for _ in range(order_count):
        order_id = f"ORD-{order_seq:05d}"
        order_seq += 1
        
        # 1. 取得具備趨勢的日期
        date_obj = generate_trend_date()
        date_str = date_obj.strftime("%Y/%m/%d") if random.random() > 0.15 else date_obj.strftime("%m-%d-%Y") # 髒數據
        
        category = random.choice(categories)
        channel = random.choices(channels, weights=[0.2, 0.3, 0.2, 0.1, 0.2])[0]
        qty = random.randint(1, 10)
        
        price = random.choice(prices[category]) + random.randint(-50, 50)
        unit_cost = int(price * random.uniform(*cost_rates[category]))
        
        # 折扣邏輯：VIP/VVIP 較常有折扣，或者特定管道
        discount = 0
        if random.random() < 0.3:
            discount = int(price * qty * random.uniform(0.05, 0.15)) # 5%~15% 折扣
            
        total = (qty * price) - discount
        
        # 訂單狀態：故意讓「服飾配件」退貨率偏高，創造洞察空間
        if category == "服飾配件" and random.random() < 0.15:
            status = "退貨"
        else:
            status = random.choices(statuses, weights=[0.9, 0.05, 0.05])[0]
            
        remark = "正常訂單"

        # 製造髒數據與缺失值
        if random.random() < 0.01:
            qty = random.randint(100, 300)
            total = (qty * price) - discount
            remark = "大宗採購或輸入錯誤"
        if random.random() < 0.04:
            total = np.nan
            remark = "系統漏算總金額"
        if random.random() < 0.02:
            status = np.nan
            remark = "狀態漏填"

        data.append([order_id, status, date_str, cust["id"], cust["name"], cust["phone"], cust["city"], cust["level"], channel, category, qty, unit_cost, price, discount, total, remark])

df = pd.DataFrame(data, columns=["訂單編號", "訂單狀態", "購買日期", "客戶ID", "客戶姓名", "聯絡電話", "所在城市", "客戶等級", "行銷渠道", "商品類別", "購買數量", "單位成本", "單價", "折扣金額", "實際結帳金額", "備註"])

# 加入重複值與打亂
duplicates = df.sample(n=25, random_state=1)
df = pd.concat([df, duplicates], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)

df.to_excel("sales_data_original.xlsx", index=False)
print(f"成功生成包含 {len(df)} 筆資料的高階預測分析檔案：sales_data_ceo_pro.xlsx")