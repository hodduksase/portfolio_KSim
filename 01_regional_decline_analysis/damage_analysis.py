import pandas as pd
import numpy as np

# 데이터 로드
file_path = '/Users/sj1007/Downloads/주택종류별_미거주_주택_빈집_사유별_기간별_파손정도별_미거주_주택_빈집_시도_20250603124051.csv'
df = pd.read_csv(file_path, encoding='euc-kr')

# 필요한 데이터만 필터링
df = df[df['주택의종류'] == '계']
df = df[df['미거주 주택(빈집)사유'] == '미거주 주택(빈집)사유-계']

# 데이터를 숫자형으로 변환
df['2020'] = pd.to_numeric(df['2020'], errors='coerce')

# 전체 빈집수 데이터
total_houses = df[df['파손정도'] == '파손정도-계'].set_index('행정구역별(시도)')['2020']

# 반 이상 파손 데이터
severe_damage = df[df['파손정도'] == '파손정도-반 이상 파손'].set_index('행정구역별(시도)')['2020']

# 일부 파손 데이터
partial_damage = df[df['파손정도'] == '파손정도-일부파손'].set_index('행정구역별(시도)')['2020']

# 결과 데이터프레임 생성
result = pd.DataFrame({
    '전체 빈집수': total_houses,
    '반 이상 파손': severe_damage,
    '일부 파손': partial_damage
})

# 비율 계산 (정수로 반올림)
result['반이상_파손_비율'] = ((result['반 이상 파손'] / result['전체 빈집수']) * 100).round()
result['일부_파손_비율'] = ((result['일부 파손'] / result['전체 빈집수']) * 100).round()
result['전체_파손_비율'] = (((result['반 이상 파손'] + result['일부 파손']) / result['전체 빈집수']) * 100).round()

# 결과를 CSV 파일로 저장
result.to_csv('행정구역별_빈집_파손_현황.csv', encoding='utf-8-sig')

# 결과 출력 (터미널)
print("\n=== 행정구역별 빈집 파손 비율 분석 ===\n")
print("행정구역별 | 전체 빈집수 | 반이상 파손(%) | 일부 파손(%) | 전체 파손(%)")
print("-" * 75)

for idx, row in result.iterrows():
    if idx != '전국':  # 전국은 마지막에 따로 출력
        print(f"{idx:<10} | {int(row['전체 빈집수']):>10,} | {int(row['반이상_파손_비율']):>12} | {int(row['일부_파손_비율']):>11} | {int(row['전체_파손_비율']):>11}")

# 전국 데이터 출력
print("\n=== 전국 현황 ===")
national = result.loc['전국']
print(f"전체 빈집 수: {int(national['전체 빈집수']):,}호")
print(f"반 이상 파손 비율: {int(national['반이상_파손_비율'])}%")
print(f"일부 파손 비율: {int(national['일부_파손_비율'])}%")
print(f"전체 파손 비율: {int(national['전체_파손_비율'])}%")

print("\nCSV 파일이 '행정구역별_빈집_파손_현황.csv'로 저장되었습니다.") 