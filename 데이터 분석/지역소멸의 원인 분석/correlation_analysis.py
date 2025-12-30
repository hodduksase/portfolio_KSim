import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
plt.rcParams['font.family'] = 'AppleGothic'

# 데이터 파일 경로
empty_houses_file = '01_빈집 데이터/연도별 빈집 수와 비율 (수도권_비수도권, 2015-2023).csv'
aging_ratio_file = '02_인구 분포 데이터/인구밀도/연도별_권역별_고령화비율_v4.csv'

# 데이터 로드
empty_houses = pd.read_csv(empty_houses_file, encoding='utf-8')
aging_ratio = pd.read_csv(aging_ratio_file, encoding='utf-8')

# 데이터 전처리
# 빈집 데이터 처리
empty_houses['연도'] = empty_houses['연도'].astype(str)
empty_houses.rename(columns={'지역구분': '구분'}, inplace=True)

# 고령화 비율 데이터 처리
aging_ratio['연도'] = aging_ratio['연도'].astype(str)

# 수도권/비수도권 고령화 비율 계산
aging_summary = aging_ratio.groupby(['연도', '권역구분']).agg({
    '65세이상비율': 'mean'
}).reset_index()
aging_summary.rename(columns={'권역구분': '구분', '65세이상비율': '고령화비율'}, inplace=True)

# 수도권과 비수도권 데이터 분리
regions = ['수도권', '비수도권']
correlations = {}

plt.figure(figsize=(15, 6))

for i, region in enumerate(regions):
    # 해당 지역의 데이터 추출
    empty_region = empty_houses[empty_houses['구분'] == region]
    aging_region = aging_summary[aging_summary['구분'] == region]
    
    # 연도를 기준으로 데이터 병합
    merged_data = pd.merge(empty_region, aging_region, on=['연도', '구분'])
    
    # 상관계수 계산
    correlation = stats.pearsonr(merged_data['고령화비율'], merged_data['빈집수(호)'])
    correlations[region] = correlation
    
    # 산점도 그리기
    plt.subplot(1, 2, i+1)
    sns.regplot(data=merged_data, x='고령화비율', y='빈집수(호)')
    plt.title(f'{region} 고령화비율과 빈집수의 상관관계\nCorrelation: {correlation[0]:.3f} (p-value: {correlation[1]:.3f})')
    plt.xlabel('고령화비율 (%)')
    plt.ylabel('빈집수 (호)')

plt.tight_layout()
plt.savefig('correlation_analysis_count.png', dpi=300, bbox_inches='tight')

# 상관관계 결과 출력
print("\n=== 상관관계 분석 결과 ===")
for region, (corr, p_value) in correlations.items():
    print(f"\n{region}:")
    print(f"상관계수: {corr:.3f}")
    print(f"P-value: {p_value:.3f}")

# 연도별 추이 시각화
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

for region in regions:
    empty_region = empty_houses[empty_houses['구분'] == region]
    aging_region = aging_summary[aging_summary['구분'] == region]
    merged_data = pd.merge(empty_region, aging_region, on=['연도', '구분'])
    
    line1 = ax1.plot(merged_data['연도'], merged_data['빈집수(호)'], marker='o', label=f'{region} 빈집수')
    line2 = ax2.plot(merged_data['연도'], merged_data['고령화비율'], marker='s', linestyle='--', label=f'{region} 고령화비율')

ax1.set_xlabel('연도')
ax1.set_ylabel('빈집수 (호)')
ax2.set_ylabel('고령화비율 (%)')

# 범례 통합
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title('연도별 고령화비율과 빈집수 추이')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('trend_analysis_count.png', dpi=300, bbox_inches='tight') 