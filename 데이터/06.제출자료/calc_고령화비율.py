import pandas as pd

# 파일 경로
file_path = '인구밀도/(완료)연도별_권역별_고령화비율_v4.csv'
output_path = '인구밀도/(완료)연도별_권역별_고령화비율_v4_정리본.csv'

# 데이터 읽기
df = pd.read_csv(file_path)

# '합계'와 '65세이상' 데이터만 추출
df_total = df[df['연령대'] == '합계'][['시도', '연도', '총인구']].rename(columns={'총인구': '전체인구'})
df_old = df[df['연령대'] == '65세이상'][['시도', '연도', '총인구']].rename(columns={'총인구': '65세이상인구'})

# 연도, 시도별로 merge
merged = pd.merge(df_total, df_old, on=['시도', '연도'])

# 고령화 비율 계산 (소수점 첫째 자리에서 반올림 후 정수)
merged['고령화 비율'] = ((merged['65세이상인구'] / merged['전체인구']) * 100).round().astype(int)

# 필요한 컬럼만 남기기
result = merged[['연도', '시도', '고령화 비율']]

# 결과 저장
result.to_csv(output_path, index=False)

print('고령화 비율(정수, 반올림)로 저장 완료!') 