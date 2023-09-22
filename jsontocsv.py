import pandas as pd
import json

# JSON 파일 읽어오기
with open('./dbproductcode.json', 'r', encoding='utf-8-sig') as f:
    json_data = json.load(f)

# 모든 가능한 키를 명시적으로 확인
columns = ['id', 'product_code', 'product_name', 'color_name', 'size', 'mainclass', 'semiclass', 'image_path', 'totalsale', 'sale_price']
# 빈 값을 NaN으로 채워넣기 위해 DataFrame 생성
df = pd.DataFrame(json_data, columns=columns)

# 한국어 인코딩 문제 해결과 함께 CSV 파일로 저장
df.to_csv("./dbproductcode.csv", index=False, encoding='utf-8-sig')
