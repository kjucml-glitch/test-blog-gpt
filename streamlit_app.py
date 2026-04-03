import os

import streamlit as st

from blog_writer import create_blog_post


st.set_page_config(page_title="Creative Blog Writer", page_icon="✍️", layout="wide")

st.title("Creative Blog Writer")
st.caption("키워드 하나로 창의적인 블로그 글을 생성합니다.")

with st.sidebar:
    st.subheader("API / 생성 설정")
    api_key_input = st.text_input(
        "OPENAI_API_KEY",
        type="password",
        value="",
        placeholder="sk-...",
        help="비워두면 시스템 환경변수 OPENAI_API_KEY를 사용합니다.",
    )
    model = st.selectbox(
        "모델",
        options=["gpt-4.1-mini", "gpt-4o-mini"],
        index=0,
        help="기본값은 가성비가 좋은 gpt-4.1-mini입니다.",
    )
    language = st.selectbox("출력 언어", options=["Korean", "English"], index=0)
    temperature = st.slider("창의성(temperature)", min_value=0.0, max_value=2.0, value=0.9, step=0.1)

keyword = st.text_input("키워드", placeholder="예: 미니멀 라이프")
generate_clicked = st.button("블로그 글 생성", type="primary")

if generate_clicked:
    if not keyword.strip():
        st.error("키워드를 입력해주세요.")
    else:
        effective_api_key = api_key_input.strip() or os.getenv("OPENAI_API_KEY", "")
        if not effective_api_key:
            st.error("API 키가 없습니다. 사이드바에 입력하거나 OPENAI_API_KEY를 설정해주세요.")
        else:
            try:
                with st.spinner("창의적인 글을 생성하는 중입니다..."):
                    result = create_blog_post(
                        keyword=keyword.strip(),
                        model=model,
                        language=language,
                        temperature=temperature,
                        api_key=effective_api_key,
                    )

                if not result:
                    st.warning("응답이 비어 있습니다. 다시 시도해주세요.")
                else:
                    st.success("생성 완료")
                    st.markdown(result)
                    st.download_button(
                        "Markdown 다운로드",
                        data=result,
                        file_name=f"{keyword.strip().replace(' ', '_')}.md",
                        mime="text/markdown",
                    )
            except Exception as exc:
                st.error(f"생성 중 오류가 발생했습니다: {exc}")
