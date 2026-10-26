import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="탈북민을 위한 편의 서비스",
    page_icon="🇰🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gemini API 클라이언트 초기화 함수
def get_gemini_client():
    if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
        try:
            from google import genai
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"].strip())
            return client
        except Exception as e:
            st.error(f"Gemini API 연동 중 오류가 발생했습니다: {e}")
            return None
    return None

# 세션 상태 초기화 (페이지 이동 관리)
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# 대화 기록 초기화
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 사이드바 메뉴 구현
st.sidebar.title("📌 메뉴 안내")
page_options = {
    'home': "🏠 홈 (서비스 안내)",
    'convert': "1. 언어변환 페이지",
    'practice': "2. AI 남한어 연습 페이지",
    'culture': "3. 주요 문화 차이 페이지"
}

# 사이드바 라디오 버튼과 세션 연동
selected_page = st.sidebar.radio(
    "이동할 페이지를 선택하세요:",
    options=list(page_options.keys()),
    format_func=lambda x: page_options[x],
    index=list(page_options.keys()).index(st.session_state['page'])
)

# 라디오 선택 변경 시 세션 상태 업데이트
if selected_page != st.session_state['page']:
    st.session_state['page'] = selected_page
    st.rerun()

# -----------------------------------------------------------------------------
# 1. 홈 페이지
# -----------------------------------------------------------------------------
if st.session_state['page'] == 'home':
    st.title("탈북민을 위한 편의 서비스 안내")
    
    # 상단 안내 박스 (와이어프레임 구조 반영)
    st.info(
        "안녕하세요! 이 사이트는 탈북민을 위한 서비스이며, "
        "남한과 북한의 언어 차이, 문화 차이 등 여러 요인 때문에 남한 생활에 어려움을 겪는 탈북민들을 돕기 위한 사이트입니다."
    )
    
    st.markdown("---")
    st.subheader("주요 기능 설명 및 바로가기")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1. 언어변환 페이지")
        st.write("낯선 외래어나 남한 사회 용어를 이해하기 쉬운 표현과 북한어 대비 설명으로 변환해 드립니다.")
        if st.button("바로가기", key="btn_go_convert", use_container_width=True):
            st.session_state['page'] = 'convert'
            st.rerun()
            
    with col2:
        st.markdown("### 2. AI 남한어 연습 페이지")
        st.write("카페 주문, 면접, 관공서 방문 등 남한에서의 일상 대화를 AI 튜터와 친근하게 연습해 볼 수 있습니다.")
        if st.button("바로가기", key="btn_go_practice", use_container_width=True):
            st.session_state['page'] = 'practice'
            st.rerun()
            
    with col3:
        st.markdown("### 3. 주요 문화 차이 페이지")
        st.write("행정, 금융, 일상생활, 키오스크 이용 등 남한 생활에 꼭 필요한 문화 차이와 꿀팁을 정리해 두었습니다.")
        if st.button("바로가기", key="btn_go_culture", use_container_width=True):
            st.session_state['page'] = 'culture'
            st.rerun()

# -----------------------------------------------------------------------------
# 2. 언어변환 페이지
# -----------------------------------------------------------------------------
elif st.session_state['page'] == 'convert':
    st.title("🔤 1. 언어변환 페이지")
    st.caption("남한에서 사용하는 외래어, 신조어, 사회 용어를 쉽게 이해할 수 있도록 도와드립니다.")
    
    tab1, tab2 = st.tabs(["🤖 AI 실시간 언어 변환", "📚 자주 쓰는 용어 사전"])
    
    with tab1:
        st.subheader("AI 남한어/외래어 쉬운 풀이 서비스")
        user_input_word = st.text_input("궁금한 남한 단어나 문장을 입력하세요:", placeholder="예: 무인 키오스크, 아이스 아메리카노, 신용카드 발급")
        
        if st.button("쉬운 말로 변환하기", key="btn_translate"):
            if not user_input_word.strip():
                st.warning("단어나 문장을 입력해주세요.")
            else:
                client = get_gemini_client()
                if client is None:
                    st.warning("⚠️ GEMINI_API_KEY가 설정되지 않았습니다. Secrets 설정을 확인해 주세요. (아래 기본 용어 사전은 이용 가능합니다.)")
                else:
                    with st.spinner("Gemini AI가 쉬운 말로 설명 중입니다..."):
                        try:
                            prompt = f"""
                            너는 탈북민의 남한 정착을 돕는 친절한 언어 도우미야.
                            다음 남한 단어/문장을 탈북민이 직관적으로 이해할 수 있게 설명해줘.
                            
                            입력: "{user_input_word}"
                            
                            답변 양식:
                            1. **쉬운 뜻 풀이**: (무슨 의미인지 아주 쉬운 말로 설명)
                            2. **북한 유사 표현**: (북한에서 사용하는 비슷한 단어나 개념이 있다면 소개, 없으면 단순 상황 설명)
                            3. **일상생활 사용 예문**: (남한에서 실제로 사용되는 2개 정도의 예시 문장)
                            """
                            response = client.models.generate_content(
                                model='gemini-2.5-flash-lite',
                                contents=prompt,
                            )
                            st.success("변환 완료!")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"API 요청 중 오류가 발생했습니다: {e}")
                            
    with tab2:
        st.subheader("자주 쓰이는 주요 용어 비교")
        dictionary_data = [
            {"남한 용어 (외래어)": "키오스크 (Kiosk)", "쉬운 설명": "무인 자동 주문기 (화면을 터치하여 음식을 주문하고 결제하는 기계)", "북한 유사/참고 표현": "봉사기 / 자동주문기"},
            {"남한 용어 (외래어)": "아메리카노 (Americano)", "쉬운 설명": "에스프레소 원액에 물을 섞은 연한 원두커피", "북한 유사/참고 표현": "단물 안 넣은 서양식 쓴 커피"},
            {"남한 용어 (외래어)": "주민센터 / 동사무소", "쉬운 설명": "주민등록, 서류 발급 등 행정 업무를 처리하는 지역 기관", "북한 유사/참고 표현": "동사무소 / 인민위원회 행
