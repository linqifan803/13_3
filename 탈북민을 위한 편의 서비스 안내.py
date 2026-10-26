import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="탈북민을 위한 편의 서비스 안내", layout="wide")

# 세션 상태를 통한 페이지 이동 관리
if "page" not in st.session_state:
    st.session_state.page = "home"

# -----------------------------------------------------------------------------
# 메인 홈 화면 (제시된 이미지 구성 반영)
# -----------------------------------------------------------------------------
if st.session_state.page == "home":
    # 1. 상단 타이틀
    st.title("탈북민을 위한 편의 서비스 안내")
    
    # 2. 상단 안내 박스
    st.info(
        "안녕하세요! 이 사이트는 2026년 10월에 만들어진 탈북민을 위한 사이트이며 "
        "남한과 북한언어 차이, 문화 차이 등 여러 요인 때문에 남한 생활에 어려움을 겪는 "
        "탈북민들을 돕기 위한 사이트입니다."
    )
    
    st.write("")
    st.subheader("주요 기능 설명 및 바로가기")
    st.write("")
    
    # 3. 주요 기능 3가지 카드 (가로 3열 배치)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1. 언어변환 페이지")
        st.write("남한의 외래어 및 낯선 생활 용어를 탈북민이 이해하기 쉬운 단어로 해석해 드립니다.")
        if st.button("바로가기", key="btn1", use_container_width=True):
            st.session_state.page = "convert"
            st.rerun()
            
    with col2:
        st.markdown("### 2. AI 남한어 연습 페이지")
        st.write("카페 주문, 관공서 방문 등 남한에서의 일상 대화를 AI와 자유롭게 실습해 볼 수 있습니다.")
        if st.button("바로가기", key="btn2", use_container_width=True):
            st.session_state.page = "practice"
            st.rerun()
            
    with col3:
        st.markdown("### 3. 주요 문화 차이 페이지")
        st.write("행정, 금융, 대중교통, 분리수거 등 남한 정착 시 꼭 필요한 핵심 문화 차이를 정리해 두었습니다.")
        if st.button("바로가기", key="btn3", use_container_width=True):
            st.session_state.page = "culture"
            st.rerun()

# -----------------------------------------------------------------------------
# 1. 언어변환 페이지
# -----------------------------------------------------------------------------
elif st.session_state.page == "convert":
    if st.button("← 메인으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()
        
    st.title("1. 언어변환 페이지")
    st.write("궁금한 남한 단어나 외래어를 입력하세요.")
    user_input = st.text_input("단어 입력:", placeholder="예: 키오스크, 아메리카노")
    if st.button("변환"):
        st.info(f"'{user_input}'에 대한 쉽게 풀이된 설명이 들어가는 공간입니다.")

# -----------------------------------------------------------------------------
# 2. AI 남한어 연습 페이지
# -----------------------------------------------------------------------------
elif st.session_state.page == "practice":
    if st.button("← 메인으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()
        
    st.title("2. AI 남한어 연습 페이지")
    st.write("상황별 대화 연습을 진행해 보세요.")
    st.text_input("AI에게 말하기:", placeholder="안녕하세요, 주문하고 싶어요.")

# -----------------------------------------------------------------------------
# 3. 주요 문화 차이 페이지
# -----------------------------------------------------------------------------
elif st.session_state.page == "culture":
    if st.button("← 메인으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()
        
    st.title("3. 주요 문화 차이 페이지")
    st.write("남한 생활 가이드 및 문화 차이 안내 내용입니다.")
