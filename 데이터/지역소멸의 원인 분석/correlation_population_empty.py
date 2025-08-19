import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# 데이터 파일 경로
empty_houses_file = '01_빈집 데이터/연도별 빈집 수와 비율 (수도권_비수도권, 2015-2023).csv'
population_file = '02_인구 분포 데이터/인구수 데이터/연도별_시군구_총인구_2013_2025.csv'

# 데이터 로드
empty_df = pd.read_csv(empty_houses_file, encoding='utf-8')
empty_df.rename(columns={'지역구분': '구분'}, inplace=True)

# 인구 데이터 처리
df = pd.read_csv(population_file, encoding='utf-8')
capital_regions = ['서울특별시', '인천광역시', '경기도']

# 연도별 수도권/비수도권 인구 비율 계산
population_ratios = []
for year in range(2015, 2024):  # 2015-2023년 데이터만 사용
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
        '구분': '수도권',
        '인구비율': capital_ratio
    })
    population_ratios.append({
        '연도': year,
        '구분': '비수도권',
        '인구비율': non_capital_ratio
    })

# 데이터프레임 생성
pop_df = pd.DataFrame(population_ratios)

# 데이터 병합
merged_df = pd.merge(empty_df, pop_df, on=['연도', '구분'])

# 수도권과 비수도권 각각의 상관관계 분석
regions = ['수도권', '비수도권']
correlations = {}

# 그래프 생성
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('빈집 비율과 인구 비율의 상관관계 분석 (2015-2023)', y=1.05)

for i, region in enumerate(regions):
    region_data = merged_df[merged_df['구분'] == region]
    
    # 상관계수 계산
    correlation = stats.pearsonr(region_data['빈집비율(%)'], region_data['인구비율'])
    correlations[region] = correlation
    
    # 산점도 그리기
    ax = axes[i]
    sns.regplot(data=region_data, x='인구비율', y='빈집비율(%)', ax=ax)
    ax.set_title(f'{region}\nCorrelation: {correlation[0]:.3f} (p-value: {correlation[1]:.3f})')
    ax.set_xlabel('인구 비율 (%)')
    ax.set_ylabel('빈집 비율 (%)')
    
    # 연도 레이블 추가
    for _, row in region_data.iterrows():
        ax.annotate(str(int(row['연도'])), 
                   (row['인구비율'], row['빈집비율(%)']),
                   xytext=(5, 5), textcoords='offset points')

plt.tight_layout()
plt.savefig('correlation_population_empty.png', dpi=300, bbox_inches='tight')

# 연도별 데이터 출력
print("\n=== 연도별 상세 데이터 ===")
for region in regions:
    print(f"\n{region}:")
    region_data = merged_df[merged_df['구분'] == region].sort_values('연도')
    print("\n연도    인구비율    빈집비율")
    print("-------------------------")
    for _, row in region_data.iterrows():
        print(f"{int(row['연도'])}년: {row['인구비율']:.1f}%    {row['빈집비율(%)']:.1f}%")

# 상관관계 분석 결과 출력
print("\n=== 상관관계 분석 결과 ===")
for region, (corr, p_value) in correlations.items():
    print(f"\n{region}:")
    print(f"상관계수: {corr:.3f}")
    print(f"P-value: {p_value:.3f}")
    
    # 상관관계 해석
    print("해석:", end=" ")
    if abs(corr) < 0.3:
        strength = "매우 약한"
    elif abs(corr) < 0.5:
        strength = "약한"
    elif abs(corr) < 0.7:
        strength = "중간 정도의"
    elif abs(corr) < 0.9:
        strength = "강한"
    else:
        strength = "매우 강한"
        
    direction = "양의" if corr > 0 else "음의"
    significance = "통계적으로 유의미한" if p_value < 0.05 else "통계적으로 유의미하지 않은"
    
    print(f"{significance} {strength} {direction} 상관관계가 있습니다.") 