import pandas as pd
import numpy as np

# 엑셀 파일 읽기 (openpyxl 엔진 사용)
df = pd.read_excel('인구(나이).xls', engine='openpyxl')

# 연령대별 컬럼 리스트 생성
ages = [f'{i}세' for i in range(0, 100)] + ['100세 이상']

# 연령대 그룹핑
age_groups = {
    '유아': [f'{i}세' for i in range(0, 10)],
    '10대': [f'{i}세' for i in range(10, 20)],
    '20대': [f'{i}세' for i in range(20, 30)],
    '30대': [f'{i}세' for i in range(30, 40)],
    '40대': [f'{i}세' for i in range(40, 50)],
    '50대': [f'{i}세' for i in range(50, 60)],
    '60대': [f'{i}세' for i in range(60, 70)],
    '70대': [f'{i}세' for i in range(70, 80)],
    '80세 이상': [f'{i}세' for i in range(80, 100)] + ['100세 이상']
}

# 2014~2023년 데이터만 필터링
df = df[df['연도'].between(2014, 2023)]

# 연도별로 그룹화하여 연령대별 합계 계산
results = df[['연도']].copy()
for group, cols in age_groups.items():
    # 실제 존재하는 컬럼만 사용
    valid_cols = [col for col in cols if col in df.columns]
    results[group] = df[valid_cols].sum(axis=1)

# 결과를 연도별로 집계
results = results.groupby('연도').sum().reset_index()

# 결과 출력 및 저장
print(results)
results.to_csv('연령대별_인구_분석_결과.csv', index=False, encoding='utf-8-sig')

# Read the population movement data
df = pd.read_csv('인구이동(연령월별).csv', encoding='cp949')

# Extract year from the column names
years = []
for col in df.columns:
    if '년' in col:
        year = col.split('.')[0]
        if year not in years:
            years.append(year)

# Calculate out-migration rate by age group for each year
results = []
for year in years:
    # Get columns for the current year
    year_cols = [col for col in df.columns if year in col]
    
    # Calculate total out-migration for each age group
    for _, row in df.iterrows():
        age_group = row['연령']
        if age_group == '전체':
            continue
            
        # Sum up out-migration for the year
        out_migration = row[year_cols].sum()
        
        # Calculate rate (per 1000 people)
        rate = (out_migration / 1000)
        
        results.append({
            'Year': year,
            'Age Group': age_group,
            'Out-migration Rate': rate
        })

# Convert results to DataFrame
result_df = pd.DataFrame(results)

# Pivot the data to get years as columns
pivot_df = result_df.pivot(index='Age Group', columns='Year', values='Out-migration Rate')

# Save results to CSV
pivot_df.to_csv('연령대별_지방이탈율.csv', encoding='utf-8-sig')

print("Analysis complete. Results saved to '연령대별_지방이탈율.csv'")