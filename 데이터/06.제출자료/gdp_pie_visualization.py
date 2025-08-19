import pandas as pd
import matplotlib.pyplot as plt

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

# 연도별 파이 차트 생성
fig = plt.figure(figsize=(20, 15))
fig.suptitle('연도별 시도 명목 GDP 비율', fontsize=16, y=0.95)

# 3x3 그리드로 배치
for i, year in enumerate(years, 1):
    ax = plt.subplot(3, 3, i)
    
    # 해당 연도의 GDP 데이터 추출
    year_data = gdp_processed[['시도', str(year)]].copy()
    
    # GDP 비율 계산
    total_gdp = year_data[str(year)].sum()
    year_data['비율'] = year_data[str(year)] / total_gdp * 100
    
    # 비율이 3% 미만인 지역은 '기타'로 통합
    threshold = 3
    small_regions = year_data[year_data['비율'] < threshold]
    large_regions = year_data[year_data['비율'] >= threshold]
    
    if not small_regions.empty:
        others = pd.DataFrame({
            '시도': ['기타'],
            str(year): [small_regions[str(year)].sum()],
            '비율': [small_regions['비율'].sum()]
        })
        plot_data = pd.concat([large_regions, others])
    else:
        plot_data = large_regions
    
    # 파이 차트 그리기
    wedges, texts, autotexts = ax.pie(plot_data['비율'], 
                                     labels=plot_data['시도'],
                                     autopct='%1.1f%%',
                                     textprops={'fontsize': 8})
    
    # 비율 텍스트 조정
    plt.setp(autotexts, size=7)
    plt.setp(texts, size=7)
    
    # 연도 제목 추가
    ax.set_title(f'{year}년', pad=20)

plt.tight_layout()
plt.savefig('gdp_pie_charts.png', dpi=300, bbox_inches='tight')
print("연도별 GDP 비율 파이 차트가 'gdp_pie_charts.png' 파일로 저장되었습니다.")

# 2023년 기준 상위 5개 지역의 비율 출력
year_2023 = gdp_processed[['시도', '2023']].copy()
year_2023['비율'] = year_2023['2023'] / year_2023['2023'].sum() * 100
top_5_2023 = year_2023.nlargest(5, '비율')

print("\n2023년 기준 상위 5개 지역 GDP 비율:")
for _, row in top_5_2023.iterrows():
    print(f"{row['시도']}: {row['비율']:.1f}%") 