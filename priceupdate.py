import pandas as pd
import pymysql

# CSV 파일에서 데이터 불러오기 (Excel이 아니므로 pd.read_csv를 사용)
excel_data = pd.read_csv('C:/9ozproject/9OZ_SALES/productcode.csv')  # 파일 경로를 적절히 수정하세요.

# MySQL 데이터베이스 연결 설정
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tiger',  # 실제 비밀번호로 변경하세요.
    'database': '9oz'     # 실제 데이터베이스 이름으로 변경하세요.
}

# MySQL 데이터베이스 연결
connection =pymysql.connect(**db_config)
cursor = connection.cursor()

# 각 행을 순회하며 UPDATE 쿼리 실행
for index, row in excel_data.iterrows():
    sql = "UPDATE codeclass SET price = %s WHERE id = %s"  # 테이블 이름과 컬럼 이름을 적절히 수정하세요.
    cursor.execute(sql, (row['price'], row['ID']))

# 변경 사항 저장 및 연결 종료
connection.commit()
cursor.close()
connection.close()
