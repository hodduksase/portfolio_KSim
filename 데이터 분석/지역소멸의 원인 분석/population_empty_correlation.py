import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 파일 경로
empty_houses_file = '01_빈집 데이터/연도별 빈집 수와 비율 (수도권_비수도권, 2015-2023).csv'
population_file = '시도별 인구증가율 (2015 - 2023).csv'

# 데이터 로드
empty_houses = pd.read_csv(empty_houses_file, encoding='utf-8')
population = pd.read_csv(population_file, encoding='euc-kr', skiprows=[1])

# 데이터 전처리
# 빈집 데이터 처리
empty_houses['연도'] = empty_houses['연도'].astype(str)
empty_houses.rename(columns={'지역구분': '구분'}, inplace=True)

# 인구증가율 데이터 처리
# 열 이름 변경
population.columns = ['시도'] + [str(year) for year in range(2015, 2024)]

# 데이터 재구성
population_melted = pd.melt(population, 
                          id_vars=['시도'],
                          value_vars=[str(year) for year in range(2015, 2024)],
                          var_name='연도',
                          value_name='인구증가율')

# 인구증가율을 숫자로 변환
population_melted['인구증가율'] = pd.to_numeric(population_melted['인구증가율'], errors='coerce')

# 수도권/비수도권 구분
capital_region = ['서울특별시', '인천광역시', '경기도']
population_melted['구분'] = population_melted['시도'].apply(
    lambda x: '수도권' if x in capital_region 
    else ('제외' if x == '세종특별자치시' else '비수도권')
)

# 수도권/비수도권별 평균 인구증가율 계산
population_summary = population_melted[population_melted['구분'] != '제외'].groupby(['연도', '구분'])['인구증가율'].mean().reset_index()

# 데이터 병합
merged_data = pd.merge(empty_houses, population_summary, on=['연도', '구분'])

# 상관관계 분석 그래프
plt.figure(figsize=(15, 6))
regions = ['수도권', '비수도권']
correlations = {}

for i, region in enumerate(regions):
    region_data = merged_data[merged_data['구분'] == region]
    correlation = stats.pearsonr(region_data['인구증가율'], region_data['빈집수(호)'])
    correlations[region] = correlation
    
    plt.subplot(1, 2, i+1)
    sns.regplot(data=region_data, x='인구증가율', y='빈집수(호)')
    plt.title(f'{region} 인구증가율과 빈집수의 상관관계\nCorrelation: {correlation[0]:.3f} (p-value: {correlation[1]:.3f})')
    plt.xlabel('인구증가율 (%)')
    plt.ylabel('빈집수 (호)')

plt.tight_layout()
plt.savefig('인구증가율_빈집수_상관관계.png', dpi=300, bbox_inches='tight')

# 연도별 추이 시각화
fig, ax1 = plt.subplots(figsize=(15, 8))

# 첫 번째 y축 (인구증가율)
ax1.set_xlabel('연도', size=12)
ax1.set_ylabel('인구증가율(%)', size=12, color='skyblue')
for region in regions:
    region_data = merged_data[merged_data['구분'] == region]
    line1 = ax1.plot(region_data['연도'], region_data['인구증가율'], 
                     color='skyblue' if region == '수도권' else 'lightblue',
                     marker='o', linewidth=2, 
                     label=f'{region} 인구증가율(%)', markersize=8)
ax1.tick_params(axis='y', labelcolor='skyblue')

# x축 레이블 회전
plt.xticks(rotation=45, ha='right')

# 두 번째 y축 (빈집 수)
ax2 = ax1.twinx()
ax2.set_ylabel('빈집 수(호)', size=12, color='lightcoral')
for region in regions:
    region_data = merged_data[merged_data['구분'] == region]
    line2 = ax2.plot(region_data['연도'], region_data['빈집수(호)'], 
                     color='lightcoral' if region == '수도권' else 'coral',
                     linewidth=2, 
                     label=f'{region} 빈집 수(호)')
ax2.tick_params(axis='y', labelcolor='lightcoral')

# 범례 통합
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# 제목 설정 (상관계수 포함)
title = '연도별 인구증가율과 빈집 수의 관계\n'
for region, (corr, p_value) in correlations.items():
    title += f'{region} 상관계수: {corr:.4f} (p-value: {p_value:.4f})\n'
plt.title(title, pad=20, size=14)

# 여백 조정
plt.subplots_adjust(top=0.85, bottom=0.15)

# 그래프 저장
plt.savefig('인구증가율_빈집수_상관관계_선그래프.png', dpi=300, bbox_inches='tight')

# 결과 출력
print("\n=== 상관관계 분석 결과 ===")
for region, (corr, p_value) in correlations.items():
    print(f"\n{region}:")
    print(f"상관계수: {corr:.3f}")
    print(f"P-value: {p_value:.3f}")

print("\n연도별 인구증가율과 빈집 수:")
print(merged_data[['연도', '구분', '인구증가율', '빈집수(호)']]) 