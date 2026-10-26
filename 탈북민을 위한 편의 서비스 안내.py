import os
import streamlit as st
from google import genai

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="탈북민을 위한 편의 서비스 안내",
    page_icon="🤝",
    layout="wide"
)

# 2. 세션 상태 안전 초기화 (단일 세션 키로 동기화 에러 차단)
if "page" not in st.session_state:
    st.session_state.page = "홈"

# 3. Gemini API 키 안전 추출 (Secrets -> 환경변수 -> 사용자 직접 입력)
def get_api_key():
    try:
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key:
        return env_key
        
    return st.session_state.get("user_input_api_key", "")

# 4. 사이드바 메뉴 및 API 키 비상 입력란
st.sidebar.title("📌 메뉴 바로가기")

pages = ["홈", "1. 언어변환 페이지", "2. AI 남한어 연습 페이지", "3. 주요 문화 차이 페이지"]

# 현재 선택된 페이지 인덱스 계산
try:
    current_index = pages.index(st.session_state.page)
except ValueError:
    current_index = 0

selected_page = st.sidebar.radio("페이지 이동", pages, index=current_index)
st.session_state.page = selected_page

# Secrets 미설정 시 예외 방지를 위한 백업 API 키 입력창
api_key = get_api_key()
if not api_key:
    st.sidebar.markdown("---")
    st.sidebar.warning("🔑 Secrets 설정이 안 되어 있다면 아래에 API 키를 입력하세요.")
    user_key = st.sidebar.text_input("Gemini API Key 입력", type="password")
    if user_key:
        st.session_state.user_input_api_key = user_key
        st.rerun()

# 5. Gemini API 호출 함수 (오류 시 앱 멈춤 없이 경고 출력)
def call_gemini(prompt: str) -> str:
    current_key = get_api_key()
    if not current_key:
        return "⚠️ `GEMINI_API_KEY`가 설정되지 않았습니다. Streamlit Secrets에 키를 등록하거나 사이드바에 키를 입력해 주세요."
    
    try:
        client = genai.Client(api_key=current_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"⚠️ API 호출 도중 오류가 발생했습니다: {str(e)}"

# -----------------------------------------------------------------------------
# PAGE 1: 홈 (메인 안내 페이지)
# -----------------------------------------------------------------------------
if st.session_state.page == "홈":
    st.title("탈북민을 위한 편의 서비스 안내")
    
    st.info(
        "안녕하세요! 이사이트는 2026년 10월에 만들어진 탈북민을 위한 사이트이며 "
        "남한과 북한언어 차이, 문화 차이 등 여러 요인 때문에 남한 생활에 어려움을 겪는 탈북민들을 돕기 위한 사이트입니다."
    )
    
    st.markdown("---")
    st.subheader("주요 기능 설명 및 바로가기")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1. 언어변환 페이지")
        st.write("생소한 남한의 외래어, 신조어, 전문 용어를 북한 어휘와 쉬운 뜻풀이로 변환해 드립니다.")
        if st.button("바로가기 ➔", key="btn_go_p1"):
            st.session_state.page = "1. 언어변환 페이지"
            st.rerun()

    with col2:
        st.markdown("### 2. AI 남한어 연습 페이지")
        st.write("은행, 병원, 관공서 등 남한 생활에 필요한 실전 대화를 AI와 자유롭게 연습할 수 있습니다.")
        if st.button("바로가기 ➔", key="btn_go_p2"):
            st.session_state.page = "2. AI 남한어 연습 페이지"
            st.rerun()

    with col3:
        st.markdown("### 3. 주요 문화 차이 페이지")
        st.write("금융, 의료, 행정 제도 등 남북한 생활 문화 차이를 비교 표와 AI Q&A로 알기 쉽게 정리해 드립니다.")
        if st.button("바로가기 ➔", key="btn_go_p3"):
            st.session_state.page = "3. 주요 문화 차이 페이지"
            st.rerun()

# -----------------------------------------------------------------------------
# PAGE 2: 언어변환 페이지
# -----------------------------------------------------------------------------
elif st.session_state.page == "1. 언어변환 페이지":
    st.title("🔤 1. 언어변환 페이지")
    st.write("남한 생활 중 이해하기 어려웠던 단어나 문장을 입력해 보세요.")

    example_choice = st.selectbox(
        "자주 쓰이는 남한 표현 예시 선택:",
        [
            "직접 입력",
            "아이스 아메리카노 테이크아웃으로 키오스크에서 주문해 주세요.",
            "모바일 뱅킹으로 공과금을 자동이체 신청하려고 합니다.",
            "주민센터에서 주민등록등본 발급받으려면 신분증이 필요합니다."
        ]
    )

    default_value = "" if example_choice == "직접 입력" else example_choice
    user_input = st.text_area("변환할 남한어 문장/단어 입력:", value=default_value, placeholder="예: 패스트푸드점에서 키오스크로 결제하세요.", height=120)

    if st.button("언어 변환하기", type="primary"):
        if not user_input.strip():
            st.warning("변환할 문장이나 단어를 입력해 주세요.")
        else:
            with st.spinner("AI가 분석 및 변환 중입니다..."):
                prompt = f"""
                당신은 탈북민의 남한 사회 정착을 돕는 친절한 언어 튜터입니다.
                아래 남한어 문장이나 단어에 대해 다음 항목으로 친절히 해설해 주세요:

                1. **알기 쉬운 뜻풀이**: 핵심 의미를 쉬운 말로 요약해 주세요.
                2. **외래어 및 어휘 비교**: 남한 표현과 상응하는 북한 어휘 또는 쉬운 우리말 설명.
                3. **실생활 팁**: 해당 상황에서 알아두면 좋은 행동 요령이나 에티켓.

                [입력 문장]: {user_input}
                """
                result = call_gemini(prompt)
                st.markdown("### 💡 변환 결과")
                st.markdown(result)

# -----------------------------------------------------------------------------
# PAGE 3: AI 남한어 연습 페이지
# -----------------------------------------------------------------------------
elif st.session_state.page == "2. AI 남한어 연습 페이지":
    st.title("💬 2. AI 남한어 연습 페이지")
    st.write("실전 상황별로 AI 직원과 가상 대화를 나누며 자연스러운 남한 표현을 연습해 보세요.")

    scenario = st.selectbox(
        "연습할 상황을 선택하세요:",
        ["은행 창구에서 계좌 개설하기", "주민센터에서 서류 발급받기", "병원 접수 및 증상 설명하기", "카페에서 음료 주문하기"]
    )

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "current_scenario" not in st.session_state or st.session_state.current_scenario != scenario:
        st.session_state.current_scenario = scenario
        st.session_state.chat_messages = [
            {"role": "assistant", "content": f"안녕하세요! **[{scenario}]** 대화 연습입니다.\n\n'어서 오세요! 무엇을 도와드릴까요?'"}
        ]

    for msg in st.session_state.chat_messages:
        st.chat_message(
