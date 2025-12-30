import pandas as pd

# 데이터 로드
crime_df = pd.read_csv('06_5대 범죄 데이터/(완료)2023년 5대 주요범죄통계.csv', encoding='utf-8')

# 시도별 발생건수 합계 계산
crime_sum = crime_df.groupby('시도')['발생건수'].sum().reset_index()
crime_sum = crime_sum.rename(columns={'발생건수': '총_발생건수'})

# 원본 데이터와 합계 데이터 병합
result_df = pd.merge(crime_df, crime_sum, on='시도', how='left')

# 결과 출력
print("\n시도별 범죄 발생 현황:")
print(result_df)

# CSV 파일로 저장
result_df.to_csv('시도별_5대범죄_발생현황.csv', encoding='utf-8-sig', index=False) 