import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기 (인코딩 옵션 수정)
empty_houses = pd.read_csv('건축연도_및_주택의_종류별_미거주_주택_빈집___시군구_20250604144932.csv', encoding='latin1')
population = pd.read_csv('인구밀도_연령대별_수도권_비수도권_집중도 복사본.csv', encoding='latin1')

# 수도권/비수도권 구분
capital_area = ['서울특별시', '인천광역시', '경기도']
empty_houses['region_type'] = empty_houses['시도'].apply(lambda x: '수도권' if x in capital_area else '비수도권')

# 비수도권 빈집 수 계산
non_capital_empty = empty_houses[empty_houses['region_type'] == '비수도권'].groupby('연도')['빈집수'].sum().reset_index()

# 비수도권 고령화 비율 데이터 준비
non_capital_aging = population[~population['시도'].isin(capital_area)].groupby('연도')['고령화비율'].mean().reset_index()

# 그래프 그리기
fig, ax1 = plt.subplots(figsize=(12, 6))

# 빈집 수 막대 그래프 (좌측 y축)
ax1.bar(non_capital_empty['연도'], non_capital_empty['빈집수'], color='skyblue', alpha=0.7)
ax1.set_xlabel('연도')
ax1.set_ylabel('빈집 수(호)')

# 고령화 비율 선 그래프 (우측 y축)
ax2 = ax1.twinx()
ax2.plot(non_capital_aging['연도'], non_capital_aging['고령화비율'], color='red', linewidth=2, marker='o')
ax2.set_ylabel('고령화비율(%)')

plt.title('비수도권 빈집 수와 고령화 비율 추이')
plt.tight_layout()
plt.savefig('analysis_result.png', dpi=300, bbox_inches='tight')
plt.close() 