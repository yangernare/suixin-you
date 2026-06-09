import sqlite3
# 连接数据库（自动创建 travel.db 文件）
conn = sqlite3.connect("travel.db")
cursor = conn.cursor()
# 创建表： 经度、纬度、地名、类别
cursor.execute('''
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,          -- 地名（你要的）
    category TEXT,               -- 类别（人文/自然/美食/休闲）
    longitude REAL,              -- 经度
    latitude REAL                -- 纬度
)
''')
# 保存并关闭
conn.commit()
conn.close()
print("数据库创建成功！包含：地名、类别、经度、纬度")