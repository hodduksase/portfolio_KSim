import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 파일 경로
empty_houses_file = '01_빈집 데이터/연도별 빈집 수와 비율 (수도권_비수도권, 2015-2023).csv'
aging_ratio_file = '02_인구 분포 데이터/인구밀도/(완료)수도권_비수도권 고령화 비율 비교 (2015-2023).csv'

# 데이터 로드
empty_houses = pd.read_csv(empty_houses_file, encoding='utf-8')
aging_ratio = pd.read_csv(aging_ratio_file, encoding='utf-8')

# 데이터 전처리
# 빈집 데이터 처리
empty_houses['연도'] = empty_houses['연도'].astype(str)
empty_houses.rename(columns={'지역구분': '구분'}, inplace=True)

# 고령화 비율 데이터 처리
aging_ratio['연도'] = aging_ratio['연도'].astype(str)

# 65세 이상 인구 비율 계산
aging_summary = []
for year in aging_ratio['연도'].unique():
    year_data = aging_ratio[aging_ratio['연도'] == year]
    
    # 전국 데이터에서 65세 이상 인구 비율 계산
    total_data = year_data[year_data['시도'] == '전국']
    total_pop = total_data[total_data['연령대'] == '합계']['총인구'].iloc[0]
    elderly_pop = total_data[total_data['연령대'].str.contains('65', na=False)]['총인구'].sum()
    
    # 수도권과 비수도권의 비율 계산
    aging_rate = (elderly_pop / total_pop) * 100
    
    # 수도권과 비수도권에 동일한 고령화 비율 적용
    for region in ['수도권', '비수도권']:
        aging_summary.append({
            '연도': year,
            '구분': region,
            '고령화비율': aging_rate
        })

aging_summary = pd.DataFrame(aging_summary)

# 데이터 병합
merged_data = pd.merge(empty_houses, aging_summary, on=['연도', '구분'])

# 상관관계 분석 그래프
plt.figure(figsize=(15, 6))
regions = ['수도권', '비수도권']
correlations = {}

for i, region in enumerate(regions):
    region_data = merged_data[merged_data['구분'] == region]
    correlation = stats.pearsonr(region_data['고령화비율'], region_data['빈집수(호)'])
    correlations[region] = correlation
    
    plt.subplot(1, 2, i+1)
    sns.regplot(data=region_data, x='고령화비율', y='빈집수(호)')
    plt.title(f'{region} 고령화비율과 빈집수의 상관관계\nCorrelation: {correlation[0]:.3f} (p-value: {correlation[1]:.3f})')
    plt.xlabel('고령화비율 (%)')
    plt.ylabel('빈집수 (호)')

plt.tight_layout()
plt.savefig('고령화_빈집수_상관관계.png', dpi=300, bbox_inches='tight')

# 연도별 추이 시각화
fig, ax1 = plt.subplots(figsize=(15, 8))

# 첫 번째 y축 (고령화 비율)
ax1.set_xlabel('연도', size=12)
ax1.set_ylabel('고령화 비율(%)', size=12, color='skyblue')
for region in regions:
    region_data = merged_data[merged_data['구분'] == region]
    line1 = ax1.plot(region_data['연도'], region_data['고령화비율'], 
                     color='skyblue' if region == '수도권' else 'lightblue',
                     marker='o', linewidth=2, 
                     label=f'{region} 고령화 비율(%)', markersize=8)
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
title = '연도별 고령화 비율과 빈집 수의 관계\n'
for region, (corr, p_value) in correlations.items():
    title += f'{region} 상관계수: {corr:.4f} (p-value: {p_value:.4f})\n'
plt.title(title, pad=20, size=14)

# 여백 조정
plt.subplots_adjust(top=0.85, bottom=0.15)

# 그래프 저장
plt.savefig('고령화_빈집수_상관관계_선그래프.png', dpi=300, bbox_inches='tight')

# 결과 출력
print("\n=== 상관관계 분석 결과 ===")
for region, (corr, p_value) in correlations.items():
    print(f"\n{region}:")
    print(f"상관계수: {corr:.3f}")
    print(f"P-value: {p_value:.3f}")

print("\n연도별 고령화 비율과 빈집 수:")
print(merged_data[['연도', '구분', '고령화비율', '빈집수(호)']]) 