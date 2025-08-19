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

# 증감률 계산 함수
def calculate_growth_rate(series):
    return ((series - series.shift(1)) / series.shift(1)) * 100

# 연도별 수도권/비수도권 인구 계산
population_data = []
for year in range(2015, 2024):  # 2015-2023년 데이터만 사용
    year_data = df[df['연도'] == year]
    
    # 수도권 인구
    capital_pop = year_data[year_data['시도'].isin(capital_regions)]['총인구'].sum()
    
    # 비수도권 인구
    non_capital_pop = year_data[~year_data['시도'].isin(capital_regions)]['총인구'].sum()
    
    population_data.append({
        '연도': year,
        '수도권_인구': capital_pop,
        '비수도권_인구': non_capital_pop
    })

# 인구 데이터프레임 생성
pop_df = pd.DataFrame(population_data)

# 빈집 데이터 처리
empty_pivot = empty_df.pivot(index='연도', columns='구분', values='빈집수(호)')
empty_pivot.columns = ['수도권_빈집', '비수도권_빈집']
empty_pivot = empty_pivot.reset_index()

# 데이터 병합
merged_df = pd.merge(pop_df, empty_pivot, on='연도')

# 증감률 계산
for col in ['수도권_인구', '비수도권_인구', '수도권_빈집', '비수도권_빈집']:
    merged_df[f'{col}_증감률'] = calculate_growth_rate(merged_df[col])

# 첫 해 제거 (증감률 계산 불가)
merged_df = merged_df.dropna()

# 수도권과 비수도권 각각의 상관관계 분석
regions = ['수도권', '비수도권']
correlations = {}

# 그래프 생성
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('인구 증감률과 빈집 증감률의 상관관계 분석 (2016-2023)', y=1.05)

for i, region in enumerate(regions):
    # 상관계수 계산
    correlation = stats.pearsonr(merged_df[f'{region}_인구_증감률'], 
                               merged_df[f'{region}_빈집_증감률'])
    correlations[region] = correlation
    
    # 산점도 그리기
    ax = axes[i]
    sns.regplot(data=merged_df, 
                x=f'{region}_인구_증감률', 
                y=f'{region}_빈집_증감률',
                ax=ax)
    
    ax.set_title(f'{region}\nCorrelation: {correlation[0]:.3f} (p-value: {correlation[1]:.3f})')
    ax.set_xlabel('인구 증감률 (%)')
    ax.set_ylabel('빈집 증감률 (%)')
    
    # 연도 레이블 추가
    for _, row in merged_df.iterrows():
        ax.annotate(str(int(row['연도'])), 
                   (row[f'{region}_인구_증감률'], row[f'{region}_빈집_증감률']),
                   xytext=(5, 5), textcoords='offset points')

plt.tight_layout()
plt.savefig('growth_rate_correlation.png', dpi=300, bbox_inches='tight')

# 연도별 데이터 출력
print("\n=== 연도별 증감률 데이터 ===")
for region in regions:
    print(f"\n{region}:")
    print("\n연도    인구증감률    빈집증감률")
    print("--------------------------------")
    for _, row in merged_df.iterrows():
        print(f"{int(row['연도'])}년: {row[f'{region}_인구_증감률']:.1f}%    {row[f'{region}_빈집_증감률']:.1f}%")

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