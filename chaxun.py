import sqlite3
import csv
# 1. 数据库连接
conn = sqlite3.connect("travel.db")
cursor = conn.cursor()
# 2. 读取 CSV 并写入数据库
csv_file_path = "E:\\poi\\poi\\gis数据\\2022高德poi（gcj02坐标系csv格式）\\新建文件夹\\云南POI数据\\昆明市POI数据.csv"
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    count = 0
    for row in reader:
        if count >= 100:
            break
        name = row["名称"]
        category = row["中类"]
        longitude = float(row["经度"])
        latitude = float(row["纬度"])
        # 插入数据库
        cursor.execute('''
            INSERT INTO locations (name, category, longitude, latitude)VALUES (?, ?, ?, ?)''', (name, category, longitude, latitude))
        count += 1
# 3. 提交并关闭连接
conn.commit()
conn.close()
print(f"已成功读取并写入前 {count} 条数据到数据库！")