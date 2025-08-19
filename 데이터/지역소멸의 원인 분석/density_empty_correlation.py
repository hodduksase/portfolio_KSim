import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# 데이터 파일 경로
empty_houses_file = '01_빈집 데이터/연도별 빈집 수와 비율 (수도권_비수도권, 2015-2023).csv'
density_file = '02_인구 분포 데이터/인구밀도/연도별_수도권_비수도권_평균_인구밀도차이.csv'

# 데이터 로드
empty_df = pd.read_csv(empty_houses_file, encoding='utf-8')
density_df = pd.read_csv(density_file, encoding='utf-8')

# 빈집 데이터 처리
empty_df.rename(columns={'지역구분': '구분'}, inplace=True)

# 인구밀도 데이터 재구성
density_long = pd.melt(density_df, 
                      id_vars=['연도'], 
                      value_vars=['수도권', '비수도권'],
                      var_name='구분',
                      value_name='평균 인구밀도')

# 데이터 병합
merged_df = pd.merge(density_long, empty_df[['연도', '구분', '빈집비율(%)']], on=['연도', '구분'])

# 수도권과 비수도권 각각의 상관관계 분석
regions = ['수도권', '비수도권']
correlations = {}

# 그래프 생성
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('인구밀도와 빈집 비율의 상관관계 분석 (2015-2023)', y=1.05)

for i, region in enumerate(regions):
    region_data = merged_df[merged_df['구분'] == region]
    
    # 상관계수 계산
    correlation = stats.pearsonr(region_data['평균 인구밀도'], 
                               region_data['빈집비율(%)'])
    correlations[region] = correlation
    
    # 산점도 그리기
    ax = axes[i]
    sns.regplot(data=region_data, 
                x='평균 인구밀도', 
                y='빈집비율(%)',
                ax=ax)
    
    ax.set_title(f'{region}\nCorrelation: {correlation[0]:.3f} (p-value: {correlation[1]:.3f})')
    ax.set_xlabel('평균 인구밀도 (명/km²)')
    ax.set_ylabel('빈집 비율 (%)')
    
    # 연도 레이블 추가
    for _, row in region_data.iterrows():
        ax.annotate(str(int(row['연도'])), 
                   (row['평균 인구밀도'], row['빈집비율(%)']),
                   xytext=(5, 5), textcoords='offset points')

plt.tight_layout()
plt.savefig('density_empty_correlation.png', dpi=300, bbox_inches='tight')

# 연도별 데이터 출력
print("\n=== 연도별 상세 데이터 ===")
for region in regions:
    region_data = merged_df[merged_df['구분'] == region].sort_values('연도')
    print(f"\n{region}:")
    print("\n연도    평균인구밀도    빈집비율")
    print("--------------------------------")
    for _, row in region_data.iterrows():
        print(f"{int(row['연도'])}년: {row['평균 인구밀도']:.1f}명/km²    {row['빈집비율(%)']:.1f}%")

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

# 추가 통계 분석
print("\n=== 추가 통계 분석 ===")
for region in regions:
    region_data = merged_df[merged_df['구분'] == region]
    density_mean = region_data['평균 인구밀도'].mean()
    density_std = region_data['평균 인구밀도'].std()
    empty_mean = region_data['빈집비율(%)'].mean()
    empty_std = region_data['빈집비율(%)'].std()
    
    print(f"\n{region}:")
    print(f"평균 인구밀도: {density_mean:.1f}명/km² (표준편차: {density_std:.1f})")
    print(f"평균 빈집비율: {empty_mean:.1f}% (표준편차: {empty_std:.1f})") 