import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# 데이터 파일 경로
population_file = '02_인구 분포 데이터/인구수 데이터/연도별_시군구_총인구_2013_2025.csv'

# 데이터 로드
df = pd.read_csv(population_file, encoding='utf-8')

# 수도권 지역 정의
capital_regions = ['서울특별시', '인천광역시', '경기도']

# 연도별 수도권/비수도권 인구 계산
years = sorted(df['연도'].unique())
population_ratios = []

for year in years:
    year_data = df[df['연도'] == year]
    
    # 수도권 인구
    capital_pop = year_data[year_data['시도'].isin(capital_regions)]['총인구'].sum()
    
    # 전체 인구
    total_pop = year_data['총인구'].sum()
    
    # 비수도권 인구
    non_capital_pop = total_pop - capital_pop
    
    # 비율 계산
    capital_ratio = (capital_pop / total_pop) * 100
    non_capital_ratio = (non_capital_pop / total_pop) * 100
    
    population_ratios.append({
        '연도': year,
        '수도권_인구': capital_pop,
        '비수도권_인구': non_capital_pop,
        '총인구': total_pop,
        '수도권_비율': capital_ratio,
        '비수도권_비율': non_capital_ratio
    })

# 데이터프레임 생성
result_df = pd.DataFrame(population_ratios)

# 그래프 생성
plt.figure(figsize=(12, 6))

# 선 그래프 그리기
plt.plot(result_df['연도'], result_df['수도권_비율'], marker='o', label='수도권', linewidth=2)
plt.plot(result_df['연도'], result_df['비수도권_비율'], marker='s', label='비수도권', linewidth=2)

plt.title('연도별 수도권/비수도권 인구 비율')
plt.xlabel('연도')
plt.ylabel('인구 비율 (%)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.xticks(rotation=45)

# 값 표시
for i, row in result_df.iterrows():
    plt.text(row['연도'], row['수도권_비율'], f'{row["수도권_비율"]:.1f}%', 
             ha='center', va='bottom')
    plt.text(row['연도'], row['비수도권_비율'], f'{row["비수도권_비율"]:.1f}%', 
             ha='center', va='top')

plt.tight_layout()
plt.savefig('population_ratio_analysis.png', dpi=300, bbox_inches='tight')

# 통계 출력
print("\n=== 인구 비율 통계 ===")
print("\n수도권:")
print(f"평균 인구 비율: {result_df['수도권_비율'].mean():.1f}%")
print(f"최대 인구 비율: {result_df['수도권_비율'].max():.1f}% ({result_df.loc[result_df['수도권_비율'].idxmax(), '연도']}년)")
print(f"최소 인구 비율: {result_df['수도권_비율'].min():.1f}% ({result_df.loc[result_df['수도권_비율'].idxmin(), '연도']}년)")

print("\n비수도권:")
print(f"평균 인구 비율: {result_df['비수도권_비율'].mean():.1f}%")
print(f"최대 인구 비율: {result_df['비수도권_비율'].max():.1f}% ({result_df.loc[result_df['비수도권_비율'].idxmax(), '연도']}년)")
print(f"최소 인구 비율: {result_df['비수도권_비율'].min():.1f}% ({result_df.loc[result_df['비수도권_비율'].idxmin(), '연도']}년)")

# 연도별 상세 데이터 출력
print("\n=== 연도별 상세 데이터 ===")
for _, row in result_df.iterrows():
    print(f"\n{int(row['연도'])}년:")
    print(f"수도권 인구: {row['수도권_인구']:,.0f}명 ({row['수도권_비율']:.1f}%)")
    print(f"비수도권 인구: {row['비수도권_인구']:,.0f}명 ({row['비수도권_비율']:.1f}%)")
    print(f"총인구: {row['총인구']:,.0f}명") 