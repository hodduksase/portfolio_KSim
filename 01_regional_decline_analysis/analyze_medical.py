import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# 시도와 시군구코드 추출 함수
def extract_sido_sigungu(address):
    try:
        parts = str(address).split()
        if len(parts) >= 2:
            sido = parts[0]
            # 세종시인 경우 시군구를 '전체'로 설정
            if sido == '세종특별자치시':
                return sido, '전체'
            sigungu = parts[1]
            return sido, sigungu
    except:
        pass
    return pd.NA, pd.NA

def analyze_medical_facilities():
    # 파일 경로
    file_path = '병원/전국 병의원 및 약국 현황/병원정보서비스 2024.12.xlsx'
    
    try:
        print(f"\n📊 데이터 분석 시작...")
        
        # 엑셀 파일 읽기
        df = pd.read_excel(file_path)
        
        # 주소에서 시도와 시군구코드 추출
        df[['시도', '시군구코드']] = df['주소'].apply(extract_sido_sigungu).apply(pd.Series)
        
        # 수도권과 비수도권 구분
        capital_area = ['서울특별시', '경기도', '인천광역시']
        df['지역구분'] = df['시도'].apply(lambda x: '수도권' if x in capital_area else '비수도권')
        
        # 의료기관 유형별 필터링
        medical_types = {
            '의원': df['종별코드명'] == '의원',
            '보건소': df['종별코드명'] == '보건소',
            '상급종합': df['종별코드명'] == '상급종합병원',
            '종합병원': df['종별코드명'] == '종합병원',
            '한의원': df['종별코드명'] == '한의원'
        }
        
        # 결과를 저장할 리스트
        results = []
        
        # 전체 합계 계산
        total_counts = {}
        for type_name, mask in medical_types.items():
            total_counts[type_name] = len(df[mask])
        
        # 수도권과 비수도권 각각에 대해
        for area in ['수도권', '비수도권']:
            area_df = df[df['지역구분'] == area]
            
            # 의료기관 유형별 집계
            for type_name, mask in medical_types.items():
                type_df = area_df[mask]
                
                # 시도별 집계
                sido_count = type_df.groupby('시도').size().reset_index(name='개수')
                sido_count['종별코드명'] = type_name
                sido_count['시군구'] = '전체'  # 시도별 집계는 시군구를 '전체'로 표시
                sido_count['지역구분'] = area
                results.append(sido_count)
                
                # 시군구코드별 집계 (세종시 제외)
                sigungu_count = type_df[type_df['시도'] != '세종특별자치시'].groupby(['시도', '시군구코드']).size().reset_index(name='개수')
                sigungu_count['종별코드명'] = type_name
                sigungu_count = sigungu_count.rename(columns={'시군구코드': '시군구'})
                sigungu_count['지역구분'] = area
                results.append(sigungu_count)
        
        # 결과 합치기
        final_df = pd.concat(results, ignore_index=True)
        
        # 컬럼 순서 변경
        final_df = final_df[['지역구분', '시도', '시군구', '종별코드명', '개수']]
        
        # 시도별 전체 현황과 시군구별 상세 현황 분리
        sido_total = final_df[final_df['시군구'] == '전체'].sort_values(['지역구분', '종별코드명', '시도'])
        sigungu_detail = final_df[final_df['시군구'] != '전체'].sort_values(['지역구분', '종별코드명', '시도', '시군구'])
        
        # 결과 파일 저장
        output_file = '의료기관_현황_2024_수도권비수도권.csv'
        
        # 전체 합계 정보 추가
        with open(output_file, 'w', encoding='cp949') as f:
            f.write("=== 전체 의료기관 현황 ===\n")
            f.write("의료기관종류,개수\n")
            for type_name, count in total_counts.items():
                f.write(f"{type_name},{count}\n")
            f.write("\n")
        
        # 시도별 전체 현황 저장
        sido_total.to_csv(output_file, mode='a', index=False, encoding='cp949')
        print(f"\n📊 시도별 전체 현황이 '{output_file}'에 저장되었습니다.")
        
        # 시군구별 상세 현황 저장 (같은 파일에 추가)
        with open(output_file, 'a', encoding='cp949') as f:
            f.write("\n\n=== 시군구별 상세 현황 (세종시 제외) ===\n")
            sigungu_detail.to_csv(f, index=False, encoding='cp949')
        
        print(f"📊 시군구별 상세 현황이 '{output_file}'에 추가되었습니다.")
        
        # 결과 미리보기
        print("\n=== 전체 의료기관 현황 ===")
        for type_name, count in total_counts.items():
            print(f"{type_name}: {count}개")
        
        print("\n=== 시도별 전체 현황 미리보기 ===")
        print(sido_total.head())
        print("\n=== 시군구별 상세 현황 미리보기 ===")
        print(sigungu_detail.head())
        
    except Exception as e:
        print(f"❌ 데이터 분석 실패: {str(e)}")

if __name__ == "__main__":
    analyze_medical_facilities() 