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

def main():
    st.title("PDF 문서 분석기 with Gemini")
    
    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요:", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        # PDF 파일 경로 설정
        pdf_path = "/Users/jongmin/Documents/Project For Cursor/THE_AI_REPORT.pdf"  # 예: "C:/Documents/sample.pdf"

        if os.path.exists(pdf_path):
            try:
                # PDF 텍스트 추출
                pdf_text = read_pdf(pdf_path)
                
                # Gemini 모델 설정
                model = genai.GenerativeModel('gemini-pro')
                
                # 사용자 질문 입력
                user_question = st.text_input("PDF 문서에 대해 질문하세요:")
                
                if user_question:
                    # 프롬프트 생성
                    prompt = f"다음 문서를 바탕으로 질문에 답변해주세요.\n\n문서 내용:\n{pdf_text}\n\n질문: {user_question}"
                    
                    # Gemini API 호출
                    response = model.generate_content(prompt)
                    
                    # 결과 표시
                    st.write("답변:")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
        else:
            st.error("PDF 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    else:
        st.warning("API 키를 입력해주세요.")

if __name__ == "__main__":
    main()
