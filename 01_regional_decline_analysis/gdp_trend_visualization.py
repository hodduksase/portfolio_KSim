import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# GDP 데이터 로드 및 전처리
gdp_df = pd.read_csv('03_일자리, 인프라 데이터/시도별_지역내총생산_2015_2023.csv')
gdp_df = gdp_df[gdp_df['경제활동별'] == '지역내총생산(시장가격)']

# 필요한 열만 선택 (시도와 연도별 명목 GDP)
years = range(2015, 2024)
columns = ['시도별'] + [f'{year}_명목' for year in years]
gdp_processed = gdp_df[columns].copy()
gdp_processed.columns = ['시도'] + [str(year) for year in years]

# 데이터 재구성 (긴 형태로)
gdp_long = pd.melt(gdp_processed, 
                   id_vars=['시도'],
                   value_vars=[str(year) for year in years],
                   var_name='연도',
                   value_name='GDP')
gdp_long['연도'] = gdp_long['연도'].astype(int)
gdp_long['GDP'] = gdp_long['GDP'].astype(float)

# 그래프 크기 설정
plt.figure(figsize=(15, 10))

# 선 그래프 그리기
sns.lineplot(data=gdp_long, x='연도', y='GDP', hue='시도', marker='o')

# 그래프 스타일링
plt.title('시도별 연도별 명목 GDP 추이 (2015-2023)', pad=20, size=15)
plt.xlabel('연도', size=12)
plt.ylabel('명목 GDP (백만원)', size=12)

# Y축 눈금 포맷 설정 (큰 숫자를 보기 좋게 표시)
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])

# 범례 위치 조정 및 스타일링
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)

# 격자 추가
plt.grid(True, linestyle='--', alpha=0.7)

# 여백 조정
plt.tight_layout()

# 그래프 저장
plt.savefig('gdp_trend_nominal.png', dpi=300, bbox_inches='tight')
print("명목 GDP 추이 그래프가 'gdp_trend_nominal.png' 파일로 저장되었습니다.") 