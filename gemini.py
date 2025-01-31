import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os

def read_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_team_info():
    st.sidebar.title("AI 연구 논문 리뷰 팀")
    
    st.sidebar.header("팀 구성")
    st.sidebar.markdown("""
    1. **Sam (AI PhD)**
       - 논문 내용을 간단한 용어로 설명
       - 핵심 포인트, 방법론, 결과 분석
    
    2. **Jenny (AI & 교육 PhD)**
       - Sam의 초안을 검토 및 개선
       - 교육적 맥락과 실제 응용 사례 추가
    
    3. **Will (팀 리더)**
       - 최종 보고서 완성
       - 정확성과 일관성 검증
    """)

def generate_report(pdf_text, model):
    # Sam의 초기 분석
    sam_prompt = f"""
    당신은 Sam입니다. AI PhD로서 다음 연구 논문을 분석하고 핵심 내용을 간단히 설명해주세요:
    {pdf_text}
    다음 구조로 작성해주세요:
    1. 핵심 포인트
    2. 연구 방법론
    3. 주요 발견
    """
    sam_analysis = model.generate_content(sam_prompt).text
    
    # Jenny의 검토 및 개선
    jenny_prompt = f"""
    당신은 Jenny입니다. AI와 교육 분야 PhD로서 Sam의 분석을 검토하고 개선해주세요:
    {sam_analysis}
    다음을 추가해주세요:
    1. 실제 응용 사례
    2. 교육적 의미
    3. 추가 설명이 필요한 부분
    """
    jenny_review = model.generate_content(jenny_prompt).text
    
    # Will의 최종 검토
    will_prompt = f"""
    당신은 Will입니다. 팀 리더로서 최종 보고서를 작성해주세요:
    Sam의 분석: {sam_analysis}
    Jenny의 검토: {jenny_review}
    
    다음 구조로 최종 보고서를 작성해주세요:
    1. 핵심 요약
    2. 연구 주제 소개
    3. 주요 발견 및 방법론
    4. 복잡한 개념의 간단한 설명
    5. 실제 응용 및 영향
    6. 결론 및 향후 연구 방향
    """
    final_report = model.generate_content(will_prompt).text
    
    return sam_analysis, jenny_review, final_report

def main():
    st.title("AI 연구 논문 리뷰 시스템")
    
    # 팀 정보 사이드바 표시
    get_team_info()
    
    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요:", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        # PDF 파일 업로드
        uploaded_file = st.file_uploader("PDF 논문을 업로드하세요", type="pdf")
        
        if uploaded_file is not None:
            try:
                # PDF 텍스트 추출
                pdf_reader = PdfReader(uploaded_file)
                pdf_text = ""
                for page in pdf_reader.pages:
                    pdf_text += page.extract_text()
                
                # Gemini 모델 설정
                model = genai.GenerativeModel('gemini-1.5-pro')
                
                # 모델 설정
                generation_config = {
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
                
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                ]
                
                model.generate_content = lambda *args, **kwargs: model.generate_content(
                    *args,
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    **kwargs
                )
                
                if st.button("논문 분석 시작"):
                    with st.spinner("분석 중..."):
                        sam_analysis, jenny_review, final_report = generate_report(pdf_text, model)
                        
                        # 결과 표시
                        st.header("Sam의 초기 분석")
                        st.write(sam_analysis)
                        
                        st.header("Jenny의 검토 및 개선")
                        st.write(jenny_review)
                        
                        st.header("Will의 최종 보고서")
                        st.write(final_report)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
    else:
        st.warning("API 키를 입력해주세요.")

if __name__ == "__main__":
    main()
