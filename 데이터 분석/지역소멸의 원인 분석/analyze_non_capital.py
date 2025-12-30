import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.ticker import ScalarFormatter

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 현재 디렉토리 확인
current_dir = os.getcwd()
print(f"현재 디렉토리: {current_dir}")

# 파일 내용 직접 확인
print("\n=== 빈집 데이터 파일 내용 ===")
vacancy_file = '건축연도_및_주택의_종류별_미거주_주택_빈집___시군구_20250604144932.csv'

# 여러 인코딩 시도
encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']
for encoding in encodings:
    try:
        print(f"\n{encoding} 인코딩으로 시도:")
        with open(vacancy_file, 'r', encoding=encoding) as f:
            for i, line in enumerate(f):
                if i < 5:  # 처음 5줄만 출력
                    print(f"Line {i+1}: {line.strip()}")
                else:
                    break
        print("성공!")
        break
    except Exception as e:
        print(f"실패: {e}")

print("\n=== 고령화 데이터 파일 내용 ===")
aging_file = '(완료)연도별_권역별_고령화비율_v4_정리본.csv'

# 여러 인코딩 시도
for encoding in encodings:
    try:
        print(f"\n{encoding} 인코딩으로 시도:")
        with open(aging_file, 'r', encoding=encoding) as f:
            for i, line in enumerate(f):
                if i < 5:  # 처음 5줄만 출력
                    print(f"Line {i+1}: {line.strip()}")
                else:
                    break
        print("성공!")
        break
    except Exception as e:
        print(f"실패: {e}")

# 데이터 읽기
aging_df = pd.read_csv('(완료)연도별_권역별_고령화비율_v4_정리본.csv', encoding='utf-8-sig')
vacancy_df = pd.read_csv('건축연도_및_주택의_종류별_미거주_주택_빈집___시군구_20250604144932.csv', 
                        encoding='cp949', 
                        engine='python',
                        header=1)

print("\n빈집 데이터 구조:")
print(vacancy_df.head())
print("\n빈집 데이터 컬럼:")
print(vacancy_df.columns)

# 수도권 지역 리스트
capital_areas = ['서울특별시', '인천광역시', '경기도']

# 비수도권 데이터만 필터링 (wide format)
vacancy_df_non_capital = vacancy_df[~vacancy_df['행정구역별(시군구)(1)'].isin(capital_areas)]

# melt로 연도별로 변환 (컬럼명이 '주택_계', '주택_계.1', ... 형태)
value_vars = ['주택_계', '주택_계.1', '주택_계.2', '주택_계.3', '주택_계.4', '주택_계.5', '주택_계.6', '주택_계.7', '주택_계.8']
year_labels = [str(y) for y in range(2015, 2024)]
vacancy_long = vacancy_df_non_capital.melt(
    id_vars=['행정구역별(시군구)(1)', '주택의 종류별(1)'],
    value_vars=value_vars,
    var_name='연도', value_name='빈집수'
)
vacancy_long['연도'] = vacancy_long['연도'].map(dict(zip(value_vars, year_labels)))
# 숫자형 변환
vacancy_long['빈집수'] = pd.to_numeric(vacancy_long['빈집수'], errors='coerce')

# 연도별 빈집수 합계
vacancy_by_year = vacancy_long.groupby('연도')['빈집수'].sum().reset_index()
# 연도 컬럼을 정수형으로 변환
vacancy_by_year['연도'] = vacancy_by_year['연도'].astype(int)

# 고령화 데이터도 비수도권만 필터
aging_df_non_capital = aging_df[~aging_df['시도'].isin(capital_areas)]
aging_by_year = aging_df_non_capital.groupby('연도')['고령화 비율'].mean().reset_index()
# 연도 컬럼을 정수형으로 변환
aging_by_year['연도'] = aging_by_year['연도'].astype(int)

# 그래프 그리기
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# 고령화 비율 그래프
sns.lineplot(data=aging_by_year, x='연도', y='고령화 비율', marker='o', ax=ax1)
ax1.set_title('비수도권 연도별 고령화 비율 추이', pad=20, fontsize=14)
ax1.set_xlabel('연도', fontsize=12)
ax1.set_ylabel('고령화 비율 (%)', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.7)
# 각 마커 위에 고령화 비율 값 표시
for i, row in aging_by_year.iterrows():
    ax1.annotate(f"{row['고령화 비율']:.1f}%", (row['연도'], row['고령화 비율']), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10, color='blue')

# 빈집 수 그래프
sns.lineplot(data=vacancy_by_year, x='연도', y='빈집수', marker='o', ax=ax2)
ax2.set_title('비수도권 연도별 빈집 수 추이', pad=20, fontsize=14)
ax2.set_xlabel('연도', fontsize=12)
ax2.set_ylabel('빈집 수', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.7)

# y축 레이블 형식 변경 (과학적 표기법 비활성화 및 쉼표 추가)
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)
ax2.yaxis.set_major_formatter(formatter)

# 각 마커 위에 빈집 수 값 표시 (쉼표 형식)
for i, row in vacancy_by_year.iterrows():
    ax2.annotate(f"{row['빈집수']:,}", (row['연도'], row['빈집수']), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10, color='red')

# 그래프 저장
plt.tight_layout()
plt.savefig('비수도권_고령화_빈집_추이_v2.png', dpi=300, bbox_inches='tight')
plt.close()

# 결과 출력
print("\n비수도권 연도별 고령화 비율:")
print(aging_by_year)
print("\n비수도권 연도별 빈집 수:")
print(vacancy_by_year) 