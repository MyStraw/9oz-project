import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('C:\\9ozproject\\9OZ_SALES\\productcode.csv', encoding='cp949',dtype={'product_code': str})

# 분류 및 세부분류를 위한 사전 생성
classification_dict = {
    'TS': ('top', 'tshirt'),
    'TN': ('top', 'tshirtsleeveless'),
    'KT': ('top', 'knit'),  
    'KN': ('top', 'knitsleeveless'),  
    'BL': ('top', 'blouse'),  
    'WS': ('top', 'shirt'),  
    'BN': ('top', 'blousesleeveless'),  
    'CA': ('top', 'cardigan'),  
    'CD': ('top', 'cardigan'),
    'OP': ('onepiece', 'onepiece'),  
    'ST': ('onepiece', 'set'),
    'JP': ('outer','jumper'),  
    'JK': ('outer','jacket'),  
    'CT': ('outer','coat'),  
    'VT': ('outer','vest'),  
    'FU': ('outer', 'fur'),
    'OU': ('outer', 'jumper'),  
    'PT': ('bottom','pants'),  
    'DP': ('bottom','denim'),  
    'SK': ('bottom','skirt'),  
    'LG': ('bottom','leggings')
}

# product_code에서 5,6번째 글자를 추출하여 분류 및 세부분류 진행
df['class'] = df['product_code'].str[4:6].apply(lambda x: classification_dict.get(x, ('미분류', '미분류'))[0])
df['semiclass'] = df['product_code'].str[4:6].apply(lambda x: classification_dict.get(x, ('미분류', '미분류'))[1])

# 결과를 새로운 CSV 파일에 저장
df.to_csv('C:\\9ozproject\\9OZ_SALES\\productcode.csv', index=False, encoding='cp949')
