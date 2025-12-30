import pandas as pd
import os

def process_hospital_data(year, month):
    # Excel 파일 경로 설정
    excel_file = os.path.join('병원', '전국 병의원 및 약국 현황', f'병원정보서비스 {year}.{month}.xlsx')
    print(f"\n=== {year}년 {month}월 데이터 처리 ===")
    print(f"파일 경로: {os.path.abspath(excel_file)}")

    try:
        df = pd.read_excel(excel_file)
        print("\n[컬럼명]")
        for col in df.columns:
            print(col)
        print("\n[샘플 데이터]")
        print(df.head(5))

        # 시도코드명 결측치를 '미상'으로 채우기
        df['시도코드명'] = df['시도코드명'].fillna('미상')

        # 시도코드명 표기 매핑
        sido_mapping = {
            '서울': '서울특별시',
            '부산': '부산광역시',
            '대구': '대구광역시',
            '인천': '인천광역시',
            '광주': '광주광역시',
            '대전': '대전광역시',
            '울산': '울산광역시',
            '세종': '세종특별자치시',
            '경기': '경기도',
            '강원': '강원특별자치도',
            '충북': '충청북도',
            '충남': '충청남도',
            '전북': '전북특별자치도',
            '전남': '전라남도',
            '경북': '경상북도',
            '경남': '경상남도',
            '제주': '제주특별자치도'
        }

        # 시도코드명 표기 변경
        df['시도코드명'] = df['시도코드명'].map(sido_mapping)

        # 집계 대상 병원 종류
        hospital_types = ['상급종합', '종합병원', '한의원', '의원']

        # 집계 대상만 필터링
        df_hosp = df[df['종별코드명'].isin(hospital_types)]

        # 광역시/도별 집계
        gwangyeok_summary = df_hosp.groupby(['시도코드명', '종별코드명']).size().unstack(fill_value=0).reset_index()

        # 누락된 병원 종류 컬럼이 있으면 0으로 추가
        for col in ['상급종합', '종합병원', '한의원', '의원']:
            if col not in gwangyeok_summary.columns:
                gwangyeok_summary[col] = 0

        # 컬럼명 한글로 변경
        column_mapping = {
            '상급종합': '상급종합병원 수',
            '종합병원': '종합병원 수',
            '한의원': '한의원 수',
            '의원': '의원 수'
        }
        gwangyeok_summary = gwangyeok_summary.rename(columns=column_mapping)
        # 컬럼 순서 맞추기
        final_columns = ['시도코드명', '상급종합병원 수', '종합병원 수', '한의원 수', '의원 수']
        gwangyeok_summary = gwangyeok_summary.reindex(columns=final_columns)

        # 시도코드명 기준으로 정렬 (서울특별시, 부산광역시, ... 순서)
        sido_order = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', 
                      '울산광역시', '세종특별자치시', '경기도', '강원특별자치도', '충청북도', '충청남도', 
                      '전북특별자치도', '전라남도', '경상북도', '경상남도', '제주특별자치도', '미상']
        gwangyeok_summary['시도코드명'] = pd.Categorical(gwangyeok_summary['시도코드명'], categories=sido_order, ordered=True)
        gwangyeok_summary = gwangyeok_summary.sort_values('시도코드명')

        # 시군구별 집계
        sigungu_summary = df_hosp.groupby(['시도코드명', '시군구코드명', '종별코드명']).size().unstack(fill_value=0).reset_index()
        for col in ['상급종합', '종합병원', '한의원', '의원']:
            if col not in sigungu_summary.columns:
                sigungu_summary[col] = 0
        sigungu_summary = sigungu_summary.rename(columns=column_mapping)
        final_columns_sg = ['시도코드명', '시군구코드명', '상급종합병원 수', '종합병원 수', '한의원 수', '의원 수']
        sigungu_summary = sigungu_summary.reindex(columns=final_columns_sg)

        # 파일 저장
        gwangyeok_output = f'의료기관_현황_{year}년_{month}월_광역시도별.csv'
        sigungu_output = f'의료기관_현황_{year}년_{month}월_시군구별.csv'

        gwangyeok_summary.to_csv(gwangyeok_output, index=False, encoding='utf-8-sig')
        sigungu_summary.to_csv(sigungu_output, index=False, encoding='utf-8-sig')

        print(f'\n=== {year}년 {month}월 광역시/도별 의료기관 현황 ===')
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(gwangyeok_summary)
        print(f'\n파일이 생성되었습니다:')
        print(f'- {gwangyeok_output}')
        print(f'- {sigungu_output}')

    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")
        print("현재 작업 디렉토리:", os.getcwd())
        print("디렉토리 내용:")
        print(os.listdir('.'))

# 2025년 3월 데이터만 처리
process_hospital_data('2025', '3') 