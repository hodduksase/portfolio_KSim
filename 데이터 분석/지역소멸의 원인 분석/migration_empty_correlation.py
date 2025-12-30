import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# 데이터 로드
migration_df = pd.read_csv('04_인구 이동 데이터 (전입, 전출 및 종사자 수)/인구이동자수 데이터/연도별_시군구_전입률_전출률_2013_2024 - 완료.csv')

# 빈집 데이터 로드 및 전처리
empty_df = pd.read_csv('01_빈집 데이터/빈집비율_시_군_구.csv', encoding='utf-8', skiprows=[1])
empty_df.columns = ['시군구'] + [f'{year}_{col}' for year in range(2015, 2024) for col in ['빈집비율', '빈집수', '전체주택']]

# 빈집 데이터 재구성
empty_data = []
for year in range(2015, 2024):
    year_data = empty_df[['시군구', f'{year}_빈집비율']].copy()
    year_data.columns = ['시군구', '빈집비율']
    year_data['연도'] = year
    year_data['빈집비율'] = pd.to_numeric(year_data['빈집비율'], errors='coerce')
    empty_data.append(year_data)

empty_processed = pd.concat(empty_data, ignore_index=True)

# 데이터 전처리
migration_df = migration_df[['시군구', '연도', '순이동']]
migration_df['연도'] = migration_df['연도'].astype(int)

# 연도와 시군구별로 데이터 병합
merged_df = pd.merge(migration_df, empty_processed, on=['시군구', '연도'], how='inner')

# 결측치 제거
merged_df = merged_df.dropna()

# 전체 기간에 대한 상관관계 분석
correlation = stats.pearsonr(merged_df['순이동'], merged_df['빈집비율'])
print(f'전체 기간 상관계수: {correlation[0]:.4f}')
print(f'p-value: {correlation[1]:.4f}')

# 연도별 상관관계 분석
yearly_correlations = []
for year in range(2015, 2024):
    year_data = merged_df[merged_df['연도'] == year]
    if len(year_data) > 1:  # 상관관계 계산을 위해 최소 2개 이상의 데이터 필요
        corr = stats.pearsonr(year_data['순이동'], year_data['빈집비율'])
        yearly_correlations.append({
            '연도': year,
            '상관계수': corr[0],
            'p-value': corr[1]
        })

yearly_corr_df = pd.DataFrame(yearly_correlations)
print('\n연도별 상관관계:')
print(yearly_corr_df)

# 시각화
plt.figure(figsize=(15, 12))

# 산점도
plt.subplot(2, 1, 1)
sns.scatterplot(data=merged_df, x='순이동', y='빈집비율', alpha=0.5)
plt.title('순이동과 빈집비율의 산점도 (2015-2023)')
plt.xlabel('순이동 (명)')
plt.ylabel('빈집비율 (%)')

# 추세선 추가
z = np.polyfit(merged_df['순이동'], merged_df['빈집비율'], 1)
p = np.poly1d(z)
x_range = np.linspace(merged_df['순이동'].min(), merged_df['순이동'].max(), 100)
plt.plot(x_range, p(x_range), "r--", alpha=0.8, label=f'추세선 (y = {z[0]:.2e}x + {z[1]:.2f})')
plt.legend()

# 연도별 상관계수 추이
plt.subplot(2, 1, 2)
plt.plot(yearly_corr_df['연도'], yearly_corr_df['상관계수'], marker='o', linewidth=2)
plt.title('연도별 상관계수 추이 (2015-2023)')
plt.xlabel('연도')
plt.ylabel('상관계수')
plt.grid(True)

# y축 범위 설정
plt.ylim(-1, 1)

# 0선 추가
plt.axhline(y=0, color='r', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.savefig('migration_empty_correlation.png', dpi=300, bbox_inches='tight')
plt.close()

# 상관관계 해석을 위한 추가 통계
print("\n추가 통계:")
print(f"분석된 지역 수: {len(merged_df['시군구'].unique())}")
print("\n상관계수 해석:")
print("- 상관계수가 -1에 가까울수록: 순이동이 증가할 때 빈집비율이 감소")
print("- 상관계수가 1에 가까울수록: 순이동이 증가할 때 빈집비율도 증가")
print("- 상관계수가 0에 가까울수록: 두 변수 간 선형적 관계가 약함") 