import pymysql
import pandas as pd

# MySQL 데이터베이스에 연결
conn = pymysql.connect(host='localhost', 
                       user='root', 
                       password='tiger', 
                       db='9ozproject')

# SQL 쿼리 실행하여 데이터 가져오기
sql = "SELECT * FROM codeclass;"
df = pd.read_sql(sql, conn)

# null 값은 pandas에서 자동으로 NaN으로 변환됩니다.
# 이 상태를 유지하고 CSV로 저장하면, NaN은 CSV에서 빈 필드로 저장됩니다.
df.to_csv('./codeclass.csv', index=False, encoding='utf-8-sig')  # encoding을 'utf-8-sig'로 설정하여 한글을 올바르게 저장
