#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 파일 내용 추출 및 분석 스크립트
"""

import pdfplumber
import PyPDF2
import os

def read_pdf_with_pdfplumber(pdf_path):
    """pdfplumber를 사용하여 PDF 내용 추출"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
    except Exception as e:
        print(f"pdfplumber 오류: {e}")
        return None

def read_pdf_with_pypdf2(pdf_path):
    """PyPDF2를 사용하여 PDF 내용 추출"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
    except Exception as e:
        print(f"PyPDF2 오류: {e}")
        return None

def analyze_pdf_content(pdf_path, project_name):
    """PDF 파일 내용 분석"""
    print(f"\n{'='*80}")
    print(f"📖 {project_name} PDF 분석")
    print(f"{'='*80}")
    print(f"파일 경로: {pdf_path}")
    print(f"파일 크기: {os.path.getsize(pdf_path) / (1024*1024):.1f} MB")
    
    # pdfplumber로 먼저 시도
    text = read_pdf_with_pdfplumber(pdf_path)
    
    # 실패하면 PyPDF2로 시도
    if not text:
        print("pdfplumber 실패, PyPDF2로 재시도...")
        text = read_pdf_with_pypdf2(pdf_path)
    
    if text:
        print(f"✅ PDF 내용 추출 성공!")
        print(f"📝 총 텍스트 길이: {len(text)} 문자")
        
        # 첫 1000자 미리보기
        preview = text[:1000].replace('\n', ' ').strip()
        print(f"\n📋 내용 미리보기 (처음 1000자):")
        print("-" * 50)
        print(preview)
        print("-" * 50)
        
        # 키워드 검색
        keywords = ['KBO', '야구', '선수', '연봉', '분석', '머신러닝', '데이터', '예측', '모델']
        print(f"\n🔍 키워드 검색 결과:")
        for keyword in keywords:
            count = text.count(keyword)
            if count > 0:
                print(f"  {keyword}: {count}회 등장")
        
        return text
    else:
        print("❌ PDF 내용 추출 실패")
        return None

def main():
    """메인 실행 함수"""
    print("🚀 PDF 파일 내용 분석 시작")
    
    # 분석할 PDF 파일들
    pdf_files = [
        ("미드 프로젝트 11조 발표.pdf", "프로젝트 1: 미드 프로젝트 11조"),
        ("14조 final project.pdf", "프로젝트 2: 14조 Final Project"),
        ("White Blue Simple Modern Enhancing Sales Strategy Presentation.pdf", "프로젝트 3: 세이버메트릭스 KBO 연봉분석")
    ]
    
    results = {}
    
    for pdf_path, project_name in pdf_files:
        if os.path.exists(pdf_path):
            content = analyze_pdf_content(pdf_path, project_name)
            results[project_name] = content
        else:
            print(f"❌ 파일을 찾을 수 없음: {pdf_path}")
    
    # 결과 요약
    print(f"\n{'='*80}")
    print("📊 PDF 분석 결과 요약")
    print(f"{'='*80}")
    
    for project_name, content in results.items():
        if content:
            print(f"✅ {project_name}: 성공 ({len(content)} 문자)")
        else:
            print(f"❌ {project_name}: 실패")
    
    return results

if __name__ == "__main__":
    main()
