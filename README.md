# 데이터 분석 포트폴리오

이 리포지토리는 데이터 분석 전문가의 분석 프로젝트를 포함합니다. 다양한 데이터 분석 기술과 머신러닝 기법을 활용하여 인사이트를 도출합니다.

## 📁 프로젝트 구조

```
.
├── data/                          # 데이터 디렉토리
│   ├── raw_data.csv              # 원본 데이터
│   └── processed_data.csv        # 전처리된 데이터
├── models/                        # 학습된 모델 저장
├── results/                       # 분석 결과 및 시각화
├── logs/                          # 실행 로그
├── 01_EDA_and_Data_Preprocessing.ipynb    # 탐색적 데이터 분석 및 전처리
├── 02_Machine_Learning_Modeling.ipynb     # 머신러닝 모델링
├── 03_Data_Visualization_Dashboard.py     # 데이터 시각화 대시보드
├── 04_Instagram_Data_Collection.py        # 인스타그램 데이터 수집 (크롤링)
├── 05_Instagram_Data_Analysis.py          # 인스타그램 수집 데이터 분석
├── data_analysis_pipeline.py              # 자동화된 분석 파이프라인
├── requirements.txt                        # 필요한 패키지 목록
└── README.md                               # 프로젝트 설명서
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상 환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터 준비

`data/raw_data.csv` 파일에 분석할 데이터를 준비합니다. 데이터가 없는 경우 파이프라인 실행 시 샘플 데이터가 자동으로 생성됩니다.

### 3. 분석 실행

#### 옵션 1: 전체 파이프라인 실행 (자동화)

```bash
python data_analysis_pipeline.py
```

#### 옵션 2: 단계별 실행 (Jupyter Notebook)

1. **탐색적 데이터 분석 및 전처리**
   ```bash
   jupyter notebook 01_EDA_and_Data_Preprocessing.ipynb
   ```

2. **머신러닝 모델링**
   ```bash
   jupyter notebook 02_Machine_Learning_Modeling.ipynb
   ```

3. **데이터 시각화 대시보드**
   ```bash
   python 03_Data_Visualization_Dashboard.py
   ```

4. **인스타그램 데이터 수집** (선택사항)
   ```bash
   python 04_Instagram_Data_Collection.py
   ```
   - 참고: [인스타그램 크롤링 가이드](https://hamhands.tistory.com/entry/챗gpt로-인스타그램-크롤링-하기인스타-api-없이-크롤링-성공)
   - 스크립트 내에서 계정명과 수집할 게시물 수를 설정해야 합니다.

5. **인스타그램 데이터 분석**
   ```bash
   python 05_Instagram_Data_Analysis.py
   ```
   - 먼저 04_Instagram_Data_Collection.py를 실행하여 데이터를 수집해야 합니다.

## 📊 주요 기능

### 1. 탐색적 데이터 분석 (EDA)
- 데이터 기본 통계량 분석
- 결측치 및 이상치 탐지
- 변수 간 상관관계 분석
- 데이터 분포 시각화

### 2. 데이터 전처리
- 결측치 처리 (수치형: 중앙값, 범주형: 최빈값)
- 범주형 변수 인코딩 (Label Encoding)
- 수치형 변수 표준화 (StandardScaler)
- 이상치 탐지 및 처리

### 3. 머신러닝 모델링
- 여러 모델 비교 학습:
  - Logistic Regression
  - Random Forest
  - Gradient Boosting
  - Support Vector Machine
- 교차 검증을 통한 모델 성능 평가
- 하이퍼파라미터 튜닝
- 모델 성능 시각화 (ROC 곡선, 혼동 행렬)

### 4. 데이터 시각화
- 정적 차트 (Matplotlib, Seaborn)
- 인터랙티브 대시보드 (Plotly)
- 분포 비교 차트
- 상관관계 히트맵

### 5. 인스타그램 데이터 수집 및 분석
- Selenium을 활용한 웹 크롤링
- 인스타그램 계정 게시물 데이터 수집 (본문, 좋아요, 댓글, 링크)
- 수집 데이터 분석 및 시각화
- 참여도(Engagement) 분석
- 게시물 성과 리포트 생성

## 📈 분석 결과

분석 결과는 `results/` 디렉토리에 저장됩니다:
- `data_quality_report.csv`: 데이터 품질 리포트
- `statistics_report.csv`: 통계 요약 리포트
- `model_comparison.png`: 모델 성능 비교 차트
- `confusion_matrix.png`: 혼동 행렬
- `roc_curves.png`: ROC 곡선
- `interactive_dashboard.html`: 인터랙티브 대시보드
- 기타 시각화 차트들

## 🔧 기술 스택

- **데이터 처리**: Pandas, NumPy
- **시각화**: Matplotlib, Seaborn, Plotly
- **머신러닝**: Scikit-learn
- **통계 분석**: SciPy
- **웹 크롤링**: Selenium
- **개발 환경**: Jupyter Notebook, Python 3.8+

## 📝 주의사항

1. 데이터 파일 경로를 확인하세요. `data/raw_data.csv`에 분석할 데이터를 준비해야 합니다.
2. 타겟 변수 설정: `02_Machine_Learning_Modeling.ipynb`에서 타겟 변수명을 실제 데이터에 맞게 수정해야 합니다.
3. 한글 폰트: 시각화에서 한글이 깨지는 경우 시스템에 설치된 한글 폰트 경로를 확인하세요.
4. 인스타그램 크롤링:
   - Chrome 브라우저와 ChromeDriver가 필요합니다.
   - `04_Instagram_Data_Collection.py`에서 계정명과 로그인 정보를 설정해야 합니다.
   - 인스타그램의 HTML 구조가 변경될 경우 코드 수정이 필요할 수 있습니다.
   - 크롤링 시 인스타그램 이용약관을 준수해야 합니다.

## 📧 문의

프로젝트에 대한 문의사항이나 제안사항이 있으시면 언제든지 연락주세요.

---

**데이터 분석 전문가 포트폴리오 프로젝트**

