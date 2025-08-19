import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import matplotlib.font_manager as fm
import numpy as np
import platform

# 한글 폰트 설정
if platform.system() == 'Darwin':  # macOS
    font_path = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    plt.rcParams['font.family'] = 'Malgun Gothic'
    
plt.rcParams['axes.unicode_minus'] = False   # 마이너스 기호 깨짐 방지

# 그래프 스타일 설정
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# CSV 파일들 읽기
medical_2022 = pd.read_csv('면적_대비_의료기관수_2022.csv')
medical_2023 = pd.read_csv('면적_대비_의료기관수_2023.csv')
vacancy = pd.read_csv('빈집비율_시도.csv', encoding='cp949')

def standardize_region_name(name):
    # 특별/광역/자치 등의 수식어 제거
    name = name.replace('특별', '').replace('광역', '').replace('자치', '')
    
    # 시도 제거
    name = name.replace('시도', '')
    
    # 전라북도/전북 통일
    if '전북' in name or '전라북' in name:
        return '전라북도'
        
    # 나머지 정리
    name = name.strip()
    
    return name

# 데이터 전처리
def preprocess_vacancy_data(df):
    # 필요한 행과 열만 선택
    df = df.iloc[2:]  # 헤더 행 제거
    df = df[['행정구역별(시군구)', '2023']]  # 시도명과 2023년 빈집비율만 선택
    df.columns = ['시도', '빈집비율']
    
    # 빈집비율을 숫자로 변환
    df['빈집비율'] = pd.to_numeric(df['빈집비율'], errors='coerce')
    
    # 시도명 표준화
    df['시도'] = df['시도'].apply(standardize_region_name)
    
    return df[df['시도'] != '전국']  # 전국 데이터 제외

def preprocess_medical_data(df):
    # 면적당 의료기관 수 계산 (이미 계산되어 있는 열 사용)
    df = df[['시도코드명', '면적당_의료기관 수']]
    df.columns = ['시도', '면적대비의료기관수']
    
    # 시도명 표준화
    df['시도'] = df['시도'].apply(standardize_region_name)
    
    return df

def analyze_correlation(medical_data, vacancy_data, year):
    # 데이터 병합 전 각 데이터프레임 출력
    print(f"\n=== {year}년 의료기관 데이터 ===")
    print(medical_data)
    print("\n=== 빈집 데이터 ===")
    print(vacancy_data)
    
    # 데이터 병합
    merged_df = pd.merge(medical_data, vacancy_data, on='시도', how='outer')
    
    # 병합 결과 확인
    print("\n=== 병합 결과 ===")
    print(merged_df)
    
    # 결측치 확인
    print("\n=== 결측치 있는 행 ===")
    print(merged_df[merged_df.isna().any(axis=1)])
    
    # 결측치 제외한 데이터로 상관관계 분석
    clean_df = merged_df.dropna()
    
    correlation = clean_df['면적대비의료기관수'].corr(clean_df['빈집비율'])
    r_squared = correlation ** 2
    
    # 회귀분석
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        clean_df['면적대비의료기관수'], 
        clean_df['빈집비율']
    )
    
    # 시각화
    plt.figure(figsize=(12, 8))
    
    # 산점도
    plt.scatter(clean_df['면적대비의료기관수'], clean_df['빈집비율'], 
                alpha=0.7, s=100, c='dodgerblue', edgecolor='white')
    
    # 회귀선
    x_range = np.linspace(clean_df['면적대비의료기관수'].min(), 
                         clean_df['면적대비의료기관수'].max(), 100)
    plt.plot(x_range, intercept + slope * x_range, 
             'r', label=f'회귀선 (R² = {r_squared:.3f}, p = {p_value:.4f})', 
             linestyle='--', linewidth=2)
    
    # 도시 이름 표시
    for i, txt in enumerate(clean_df['시도']):
        plt.annotate(txt, 
                    (clean_df['면적대비의료기관수'].iloc[i], 
                     clean_df['빈집비율'].iloc[i]),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=11,
                    fontproperties=font_prop if platform.system() == 'Darwin' else None,
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    plt.grid(True, alpha=0.3)
    plt.xlabel('면적당 의료기관 수 (개/km²)', fontproperties=font_prop if platform.system() == 'Darwin' else None)
    plt.ylabel('빈집 비율 (%)', fontproperties=font_prop if platform.system() == 'Darwin' else None)
    plt.title(f'{year}년 면적당 의료기관 수와 빈집 비율의 상관관계\n(상관계수: {correlation:.3f})',
             fontproperties=font_prop if platform.system() == 'Darwin' else None)
    plt.legend(prop=font_prop if platform.system() == 'Darwin' else None, loc='upper right')
    
    # 여백 조정
    plt.tight_layout()
    
    # 저장
    plt.savefig(f'의료기관_빈집_상관관계_{year}_v2.png', 
                dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"\n=== {year}년 상관관계 분석 결과 ===")
    print(f"1. Pearson 상관계수: {correlation:.4f}")
    print(f"2. 결정계수(R²): {r_squared:.4f}")
    print(f"3. P-value: {p_value:.4f}")
    
    print(f"\n{year}년 데이터:")
    print(clean_df[['시도', '면적대비의료기관수', '빈집비율']].sort_values('빈집비율', ascending=False))
    
    return clean_df

# 데이터 전처리
vacancy_processed = preprocess_vacancy_data(vacancy)
medical_2022_processed = preprocess_medical_data(medical_2022)
medical_2023_processed = preprocess_medical_data(medical_2023)

# 2022년, 2023년 각각 분석 실행
result_2022 = analyze_correlation(medical_2022_processed, vacancy_processed, 2022)
result_2023 = analyze_correlation(medical_2023_processed, vacancy_processed, 2023)

# 연도별 변화 분석
print("\n=== 2022년 대비 2023년 변화 분석 ===")
common_cities = set(result_2022['시도']) & set(result_2023['시도'])
for city in common_cities:
    medical_change = (
        result_2023[result_2023['시도'] == city]['면적대비의료기관수'].iloc[0] -
        result_2022[result_2022['시도'] == city]['면적대비의료기관수'].iloc[0]
    )
    print(f"{city}: 의료기관 수 변화: {medical_change:.2f}개/km²") 