# ============================================
# 2013~2015 기사 LDA 분석 (연도별 5개씩 토픽)
# ============================================

import os, re, warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import time

def simple_tokenize(text):
    """간단한 토큰화 (Java 없이)"""
    # 한글, 영문, 숫자만 추출
    text = re.sub(r'[^가-힣A-Za-z0-9\s]', ' ', str(text))
    # 연속된 공백을 하나로
    text = re.sub(r'\s+', ' ', text).strip()
    # 2글자 이상 단어만 추출
    tokens = [word for word in text.split() if len(word) >= 2]
    return tokens

def analyze_year_data(file_path, year):
    """연도별 기사 데이터 LDA 분석"""
    print(f"\n{'='*60}")
    print(f"🚀 {year}년 기사 LDA 분석 시작")
    print(f"{'='*60}")
    
    if not os.path.exists(file_path):
        print(f"❌ 파일 없음: {file_path}")
        return None
    
    print(f"✅ 파일 로드 중: {file_path}")
    df = pd.read_excel(file_path)
    print(f"📊 데이터 로드 완료: {df.shape}")
    print(f"📋 컬럼 목록: {list(df.columns)}")
    
    # 제목/본문 컬럼 자동 탐색
    def find_col(df, candidates):
        for c in candidates:
            if c in df.columns: 
                return c
        return None

    TITLE_COL   = find_col(df, ["제목","title","Title","기사제목"])
    CONTENT_COL = find_col(df, ["본문","content","Content","기사본문","기사내용","요약"])
    
    if not TITLE_COL and not CONTENT_COL:
        print(f"❌ 제목/본문 컬럼을 찾을 수 없습니다.")
        return None
    
    print(f"✅ 컬럼 찾기 완료:")
    print(f"  제목 컬럼: {TITLE_COL}")
    print(f"  본문 컬럼: {CONTENT_COL}")
    
    # 텍스트 결합
    texts = (df[TITLE_COL].fillna("") if TITLE_COL else pd.Series([""]*len(df))) + " " + \
            (df[CONTENT_COL].fillna("") if CONTENT_COL else pd.Series([""]*len(df)))
    texts = texts.astype(str)
    
    print(f"📝 텍스트 결합 완료: {len(texts)}개 문서")
    
    # 텍스트 전처리 및 토큰화
    print("🔧 텍스트 전처리 및 토큰화 중...")
    
    tokenized_docs = []
    for i, text in enumerate(texts):
        if i % 1000 == 0:
            progress = (i / len(texts)) * 100
            print(f"  진행률: {progress:.1f}% ({i}/{len(texts)})")
        
        tokens = simple_tokenize(text)
        if tokens:  # 빈 토큰 리스트 제외
            tokenized_docs.append(tokens)
    
    print(f"✅ 토큰화 완료: {len(tokenized_docs)}개 유효 문서")
    
    if len(tokenized_docs) < 10:
        print("❌ 토큰화된 문서가 너무 적습니다.")
        return None
    
    # DTM 구성
    print("📊 DTM 구성 중...")
    
    # 토큰을 공백으로 연결
    text_for_vectorizer = [' '.join(doc) for doc in tokenized_docs]
    
    vectorizer = CountVectorizer(
        min_df=5,  # 최소 5번 이상 등장
        max_df=0.5,  # 최대 50% 이하 문서에서 등장
        max_features=200  # 최대 200개 단어
    )
    
    # DTM 생성
    dtm = vectorizer.fit_transform(text_for_vectorizer)
    print(f"✅ DTM 생성 완료: {dtm.shape}")
    
    # LDA 학습
    print("🤖 LDA 모델 학습 중...")
    
    n_topics = 5
    lda = LatentDirichletAllocation(
        n_components=n_topics, 
        learning_method="batch",
        max_iter=20, 
        random_state=42, 
        evaluate_every=0, 
        n_jobs=1  # Windows 호환성을 위해 단일 프로세스 사용
    )
    
    # 모델 학습 시간 측정
    start_time = time.time()
    lda.fit(dtm)
    training_time = time.time() - start_time
    
    print(f"✅ LDA 모델 학습 완료 (소요시간: {training_time:.2f}초)")
    
    # 토픽별 상위 키워드 출력
    print(f"\n📊 {year}년 LDA 토픽별 상위 키워드")
    print("-" * 50)
    
    feature_names = vectorizer.get_feature_names_out()
    topn = min(10, len(feature_names))
    
    topics = []
    for idx, comp in enumerate(lda.components_):
        top_ids = comp.argsort()[-topn:][::-1]
        words = [feature_names[i] for i in top_ids]
        weights = [comp[i] for i in top_ids]
        
        print(f"\n🔍 토픽 {idx+1}:")
        topic_str = f"Topic #{idx+1}: "
        for i, (word, weight) in enumerate(zip(words, weights)):
            print(f"  {i+1:2d}. {word:15s} (가중치: {weight:.6f})")
            if i < 10:  # 상위 10개만
                topic_str += f"{weight:.3f}*\"{word}\" + "
        
        topic_str = topic_str.rstrip(" + ")
        topics.append(topic_str)
    
    # 성능 정보
    print(f"\n📈 {year}년 성능 정보")
    print("-" * 50)
    print(f"  총 문서 수: {len(tokenized_docs)}개")
    print(f"  어휘 크기: {dtm.shape[1]}개")
    print(f"  토픽 수: {n_topics}개")
    print(f"  학습 시간: {training_time:.2f}초")
    print(f"  평균 문서당 토큰 수: {np.mean([len(doc) for doc in tokenized_docs]):.1f}개")
    
    return topics

def main():
    print("🚀 2013~2015년 기사 LDA 분석 시작")
    
    # 연도별 파일 경로
    files = {
        2013: "NewsResult_20130101-20131231.xlsx",
        2014: "NewsResult_20140101-20141231.xlsx", 
        2015: "NewsResult_20150101-20151231.xlsx"
    }
    
    all_topics = {}
    
    # 각 연도별 분석 수행
    for year, file_path in files.items():
        topics = analyze_year_data(file_path, year)
        if topics:
            all_topics[year] = topics
    
    # 전체 결과 요약
    print(f"\n{'='*80}")
    print("📊 2013~2015년 LDA 분석 전체 결과 요약")
    print(f"{'='*80}")
    
    for year, topics in all_topics.items():
        print(f"\n🏆 {year}년 LDA Topics:")
        for topic in topics:
            print(topic)
    
    print(f"\n✅ 모든 연도 LDA 분석 완료!")
    print(f"📊 총 {len(all_topics)}개 연도, {sum(len(topics) for topics in all_topics.values())}개 토픽 분석")

if __name__ == "__main__":
    main()


