# 🚀 포트폴리오 실행 가이드
## KBO 선수 성과 분석 및 연봉 예측 머신러닝 시스템

---

## 📋 **실행 전 준비사항**

### **1. Python 환경 확인**
- **Python 버전**: 3.8 이상
- **가상환경 권장**: 프로젝트별 독립적인 환경 구성

### **2. 필수 라이브러리 설치**
```bash
# requirements.txt를 통한 일괄 설치 (권장)
pip install -r requirements.txt

# 또는 개별 설치
pip install pandas numpy matplotlib seaborn scikit-learn joblib scipy statsmodels
```

### **3. 폴더 구조 확인**
```
📂 새 폴더 (5)/
├── 📋 00_포트폴리오_개요/          # 프로젝트 개요 및 기술 스택
├── 🗃️ 01_데이터_수집_전처리/      # 데이터 수집 및 전처리 과정
├── 🔍 02_탐색적_데이터_분석/      # EDA 및 통계 분석
├── 🤖 03_머신러닝_모델링/         # ML 모델 개발 및 훈련
├── 📊 04_결과_시각화/             # 차트 및 대시보드
├── 📝 05_분석_리포트/             # 기술 리포트 및 인사이트
├── 🚀 06_실행_스크립트/           # 실행 가능한 코드
└── 📚 07_기술_문서/               # 상세 기술 문서
```

---

## 🚀 **메인 파이프라인 실행**

### **1. 전체 파이프라인 실행 (권장)**
```bash
cd "06_실행_스크립트"
python main_pipeline.py
```

**실행 결과**:
- 📊 데이터 수집 및 전처리
- 🔍 탐색적 데이터 분석
- 🤖 머신러닝 모델링
- 📈 결과 시각화
- 📝 분석 리포트 생성

### **2. 개별 모듈 실행**
```bash
# 데이터 생성기 테스트
python kbo_data_generator.py

# 특정 기능만 실행하고 싶은 경우
python -c "
from main_pipeline import KBOAnalysisPipeline
pipeline = KBOAnalysisPipeline()
df = pipeline.run_data_collection()
pipeline.run_exploratory_analysis(df)
"
```

---

## 📊 **데이터 생성기 활용**

### **1. 기본 데이터 생성**
```python
from kbo_data_generator import generate_sample_kbo_data

# 1000명의 선수 데이터 생성
df = generate_sample_kbo_data(1000)
print(f"생성된 데이터: {len(df)}개 레코드")
```

### **2. 특정 조건 데이터 생성**
```python
from kbo_data_generator import (
    generate_specific_year_data,
    generate_position_data,
    generate_high_salary_data
)

# 2024년 데이터만 생성
df_2024 = generate_specific_year_data(2024, 200)

# 투수 데이터만 생성
df_pitchers = generate_position_data('투수', 500)

# 고연봉 선수 데이터만 생성 (1억 이상)
df_high_salary = generate_high_salary_data(10000, 200)
```

---

## 🔧 **문제 해결**

### **1. 라이브러리 설치 오류**
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 가상환경 사용 권장
python -m venv kbo_analysis_env
source kbo_analysis_env/bin/activate  # Windows: kbo_analysis_env\Scripts\activate
pip install -r requirements.txt
```

### **2. 한글 폰트 오류**
```python
# matplotlib 한글 폰트 설정
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
# plt.rcParams['font.family'] = 'AppleGothic'  # macOS
# plt.rcParams['font.family'] = 'NanumGothic'  # Linux
```

### **3. 메모리 부족 오류**
```python
# 데이터 크기 조정
df = generate_sample_kbo_data(500)  # 선수 수 줄이기

# 청크 단위 처리
chunk_size = 100
for i in range(0, len(df), chunk_size):
    chunk = df[i:i+chunk_size]
    # 청크별 처리
```

---

## 📈 **결과 확인**

### **1. 생성된 파일들**
```
📁 results/
├── 📊 charts/
│   └── analysis_summary.png          # 분석 요약 차트
├── 🤖 models/
│   ├── salary_prediction_model.pkl   # 연봉 예측 모델
│   └── award_prediction_model.pkl    # 수상 예측 모델
├── 📝 reports/
│   ├── analysis_report.md            # 분석 리포트
│   ├── basic_statistics.csv          # 기본 통계
│   ├── position_statistics.csv       # 포지션별 통계
│   └── correlation_matrix.csv        # 상관관계 행렬
└── 📊 data/
    └── preprocessed_kbo_data.csv     # 전처리된 데이터
```

### **2. 로그 파일 확인**
```
📄 pipeline_execution.log              # 실행 로그
```

---

## 🎯 **커스터마이징**

### **1. 모델 파라미터 조정**
```python
# main_pipeline.py에서 모델 파라미터 수정
model = RandomForestRegressor(
    n_estimators=200,      # 트리 개수 증가
    max_depth=15,          # 최대 깊이 제한
    random_state=42
)
```

### **2. 특성 엔지니어링 추가**
```python
# feature_engineering 함수에 새로운 특성 추가
def feature_engineering(df):
    # 기존 특성들...
    
    # 새로운 특성 추가
    df['연봉_대비_성과'] = df['성과_지수'] / df['연봉']
    df['경력_효율성'] = df['성과_지수'] / df['경력_연수']
    
    return df
```

### **3. 시각화 커스터마이징**
```python
# run_visualization 함수에서 차트 스타일 수정
plt.style.use('seaborn-v0_8')  # 차트 스타일 변경
plt.rcParams['figure.figsize'] = (15, 10)  # 차트 크기 조정
```

---

## 🔮 **고급 활용**

### **1. Jupyter Notebook 활용**
```bash
# Jupyter 설치 및 실행
pip install jupyter
jupyter notebook

# 새 노트북에서 import
from main_pipeline import KBOAnalysisPipeline
from kbo_data_generator import generate_sample_kbo_data
```

### **2. 배치 처리**
```bash
# 여러 연도 데이터 처리
for year in 2020 2021 2022 2023 2024; do
    python main_pipeline.py --year $year
done
```

### **3. 성능 모니터링**
```python
import time
import psutil

# 실행 시간 및 메모리 사용량 모니터링
start_time = time.time()
start_memory = psutil.Process().memory_info().rss / 1024 / 1024

# 파이프라인 실행
pipeline.run_complete_pipeline()

end_time = time.time()
end_memory = psutil.Process().memory_info().rss / 1024 / 1024

print(f"실행 시간: {end_time - start_time:.2f}초")
print(f"메모리 사용량: {end_memory - start_memory:.2f}MB")
```

---

## 📞 **지원 및 문의**

### **문제 발생 시 확인사항**
1. **Python 버전**: `python --version`
2. **설치된 패키지**: `pip list`
3. **에러 메시지**: 전체 에러 로그 확인
4. **시스템 정보**: OS, 메모리, CPU 정보

### **자주 발생하는 문제**
- **ModuleNotFoundError**: requirements.txt 설치 확인
- **MemoryError**: 데이터 크기 줄이기
- **FontError**: 한글 폰트 설정 확인
- **PermissionError**: 파일 권한 확인

---

## 🎉 **성공적인 실행 확인**

### **정상 실행 시 출력 메시지**
```
🚀 KBO 선수 분석 파이프라인 시작
==================================================
📊 1단계: 데이터 수집 및 전처리 시작
==================================================
📥 KBO 데이터베이스에서 데이터 수집 중...
✅ 데이터 수집 완료: 1000개 레코드
📅 데이터 기간: 2020 - 2024
👥 선수 수: 1000명
...
🎉 전체 파이프라인 실행 완료!
⏱️ 총 소요 시간: 0:00:45.123456
📁 결과 파일들은 'results/' 폴더에 저장되었습니다.
```

### **결과 파일 확인**
- ✅ `results/charts/analysis_summary.png` 생성
- ✅ `results/models/` 폴더에 모델 파일들 저장
- ✅ `results/reports/analysis_report.md` 생성
- ✅ `results/data/preprocessed_kbo_data.csv` 생성

---

**🚀 이제 포트폴리오를 실행하여 데이터분석사 역량을 보여주세요!**
