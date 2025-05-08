import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
import io  # ✅ Import thư viện để xử lý file từ Streamlit
import chardet  # Add chardet for encoding detection

from src.logger.base import BaseLogger
from src.utils import execute_plt_code

# Load environment variables
load_dotenv()
logger = BaseLogger()

# Lấy API Key từ biến môi trường
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("⚠️ API Key của Gemini chưa được thiết lập trong file .env!")
    st.stop()

# Cấu hình Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Sử dụng model có sẵn từ list_models()
MODEL_NAME = "gemini-1.5-pro-latest"  # Hoặc "gemini-2.0-pro-exp"


def load_gemini_llm():
    """Tạo hàm để gọi Gemini API"""
    return genai.GenerativeModel(MODEL_NAME)


def process_query(df, llm, query):
    """Xử lý truy vấn dữ liệu với Gemini"""
    try:
        # Create a more specific prompt for data analysis and visualization
        prompt = f"""You are a data analysis assistant. Analyze this data and answer the question.
        If you need to create a visualization, use matplotlib and return the code in a code block starting with ```python.
        
        Data sample:
        {df.head().to_string()}
        
        Question: {query}
        
        If you need to create a visualization, make sure to:
        1. Use plt.figure() to create a new figure
        2. Create the visualization
        3. Use plt.title() to add a title
        4. Use plt.xlabel() and plt.ylabel() for axis labels
        5. Return the code in a ```python block
        """
        
        response = llm.generate_content(prompt)
        response_text = response.text

        st.write("### 🔍 Kết quả từ Gemini AI:")
        st.write(response_text)

        # Extract code from response if it contains a code block
        if "```python" in response_text:
            code_block = response_text.split("```python")[1].split("```")[0].strip()
            st.write("**Generated visualization code:**")
            st.code(code_block)
            
            fig = execute_plt_code(code_block, df=df)
            if fig:
                st.pyplot(fig)

        st.session_state.history.append((query, response_text))
    
    except Exception as e:
        st.error(f"❌ Lỗi khi gọi Gemini API: {e}")
        logger.error(f"Gemini API Error: {e}")


def display_chat_history():
    """Hiển thị lịch sử chat"""
    if "history" in st.session_state and st.session_state.history:
        st.markdown("## 📜 Chat History")
        for i, (q, r) in enumerate(st.session_state.history):
            st.markdown(f"**Query {i+1}:** {q}")
            st.markdown(f"**Response {i+1}:** {r}")
            st.markdown("---")


def main():
    """Hàm chính cho ứng dụng Streamlit"""

    # Set up Streamlit UI
    st.set_page_config(
        page_title="📊 Smart Data Analysis Tool",
        page_icon="📊",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    st.header("📊 Smart Data Analysis Tool")
    st.write(
        "### Welcome to our data analysis tool. This tool can assist with your daily data analysis tasks. Enjoy!"
    )

    # Load Gemini LLM model
    llm = load_gemini_llm()
    logger.info(f"### Successfully loaded {MODEL_NAME} !###")

    # Upload CSV file
    with st.sidebar:
        uploaded_file = st.file_uploader("📂 Upload your CSV file here", type="csv")
        if uploaded_file is not None:
            file_details = {
                "Filename": uploaded_file.name,
                "FileType": uploaded_file.type,
                "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
            }
            st.write("### File Details:")
            for key, value in file_details.items():
                st.write(f"- {key}: {value}")

    # Initialize chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Read CSV file
    if uploaded_file is not None:
        try:
            # Read file content and detect encoding
            file_content = uploaded_file.read()
            
            # Reset file pointer
            uploaded_file.seek(0)
            
            try:
                # Try reading with semicolon separator and specified encoding
                st.session_state.df = pd.read_csv(
                    uploaded_file,
                    encoding='utf-8',
                    sep=';',
                    on_bad_lines='skip'
                )
            except:
                try:
                    # Reset file pointer
                    uploaded_file.seek(0)
                    # Try with detected encoding
                    encoding_result = chardet.detect(file_content)
                    detected_encoding = encoding_result['encoding']
                    
                    st.session_state.df = pd.read_csv(
                        uploaded_file,
                        encoding=detected_encoding,
                        sep=';',
                        on_bad_lines='skip'
                    )
                except:
                    # If that fails, try common encodings
                    encodings_to_try = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
                    for encoding in encodings_to_try:
                        try:
                            uploaded_file.seek(0)  # Reset file pointer
                            st.session_state.df = pd.read_csv(
                                uploaded_file,
                                encoding=encoding,
                                sep=';',
                                on_bad_lines='skip'
                            )
                            break
                        except:
                            continue
                    else:
                        raise Exception(f"Could not read file with any of these encodings: {', '.join(encodings_to_try)}")

            # Validate that we have data
            if st.session_state.df.empty:
                st.error("❌ The uploaded CSV file is empty!")
            else:
                # Clean column names
                st.session_state.df.columns = st.session_state.df.columns.str.strip()
                
                # Display data info
                st.write("### 📊 Thông tin dữ liệu:")
                st.write(f"- Số dòng: {len(st.session_state.df)}")
                st.write(f"- Số cột: {len(st.session_state.df.columns)}")
                
                # Display the dataframe with better formatting
                st.write("### 📊 Dữ liệu của bạn:")
                st.dataframe(
                    st.session_state.df.head(),
                    use_container_width=True,
                    hide_index=False
                )

                # Display column information
                st.write("### 📋 Thông tin các cột:")
                for col in st.session_state.df.columns:
                    st.write(f"- {col}")

                # Nhập truy vấn từ người dùng
                query = st.text_input("💬 Nhập câu hỏi về dữ liệu của bạn:")

                if st.button("🔍 Phân tích"):
                    with st.spinner("Đang xử lý..."):
                        process_query(st.session_state.df, llm, query)

        except Exception as e:
            st.error(f"""❌ Lỗi khi đọc file CSV:
            - Chi tiết lỗi: {str(e)}
            - Vui lòng kiểm tra:
                1. File CSV có đúng định dạng không
                2. File có bị hỏng không
                3. Thử xuất file CSV với encoding UTF-8 và dấu phân cách là dấu chấm phẩy (;)
            """)
            logger.error(f"CSV Reading Error: {str(e)}")

    # Hiển thị lịch sử chat
    st.divider()
    display_chat_history()


if __name__ == "__main__":
    main()
