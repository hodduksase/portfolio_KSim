import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import matplotlib.ticker as ticker

# 한글 폰트 설정 (예: Apple 기본 폰트 사용)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 파일 경로
vacant_path = '인구밀도/건축연도_및_주택의_종류별_미거주_주택_빈집___시군구_20250604144932.csv'
age_path = '인구밀도/(완료)연도별_권역별_고령화비율_v4_정리본.csv'

# 연도 컬럼명
years = [str(y) for y in range(2015, 2024)]
columns = ['시도', '계'] + years

# 빈집수 데이터 읽기 (3번째 줄부터 데이터 시작, 컬럼명 직접 지정)
vacant_df = pd.read_csv(vacant_path, skiprows=2, encoding='cp949', header=None, names=columns)

# 수도권 제외
exclude = ['서울특별시', '인천광역시', '경기도']
vacant_df = vacant_df[~vacant_df['시도'].isin(exclude)]

# 연도별 빈집수 합계 계산 (호 단위)
df_vacant = vacant_df[years].apply(pd.to_numeric, errors='coerce').sum().astype(int)
df_vacant.index = df_vacant.index.astype(int)

# 고령화비율 데이터 읽기
age_df = pd.read_csv(age_path)
age_df = age_df[~age_df['시도'].isin(exclude)]

# 연도별 평균 고령화비율 계산
age_mean = age_df.groupby('연도')['고령화 비율'].mean().astype(int)

# 연도 기준으로 데이터프레임 합치기
df = pd.DataFrame({'빈집수(호)': df_vacant, '고령화비율': age_mean})

# 시각화
fig, ax1 = plt.subplots(figsize=(10,6))

# 막대그래프(빈집수)
ax1.bar(df.index, df['빈집수(호)'], color='skyblue', label='빈집수(호)')
ax1.set_xlabel('연도')
ax1.set_ylabel('빈집수(호)', color='skyblue')
ax1.tick_params(axis='y', labelcolor='skyblue')

# y축 단위 10,000 단위로 설정
ax1.yaxis.set_major_locator(ticker.MultipleLocator(10000))
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))

# 선그래프(고령화비율)
ax2 = ax1.twinx()
ax2.plot(df.index, df['고령화비율'], color='orange', marker='o', label='고령화비율(%)')
ax2.set_ylabel('고령화비율(%)', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

plt.title('비수도권 연도별 빈집수(호)와 고령화비율')
fig.tight_layout()

# 이미지로 저장
plt.savefig('인구밀도/비수도권_빈집수_고령화비율.png', dpi=300, bbox_inches='tight')
plt.show()
print('그래프가 인구밀도/비수도권_빈집수_고령화비율.png 파일로 저장되었습니다.') 