import os
import streamlit as st
from google import genai

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="탈북민을 위한 편의 서비스 안내",
    page_icon="🤝",
    layout="wide"
)

# 2. Gemini API 키 안전하게 불러오기 (Secrets -> 환경변수 -> 사이드바 입력 순)
api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY", "")

# 사이드바 설정 및 메뉴
st.sidebar.title("📌 메뉴 및 설정")

# Secrets 미설정 시를 대비한 백업 API 키 입력란 (오류 방지용)
if not api_key:
    user_key = st.sidebar.text_input("Gemini API Key (Secrets 미설정 시 입력)", type="password")
    if user_key:
        api_key = user_key

def generate_ai_response(prompt: str) -> str:
    if not api_key:
        return "⚠️ `GEMINI_API_KEY`가 설정되지 않았습니다. Streamlit Secrets에 키를 등록하거나 사이드바에 입력해 주세요."
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"⚠️ AI 서비스 호출 중 오류가 발생했습니다: {str(e)}"

# 3. 내비게이션 세션 관리 (Streamlit 오류 방지용 안전한 콜백 방식)
menu_options = ["홈", "1. 언어변환 페이지", "2. AI 남한어 연습 페이지", "3. 주요 문화 차이 페이지"]

if "nav" not in st.session_state or st.session_state["nav"] not in menu_options:
    st.session_state["nav"] = "홈"

def set_page(page_name):
    st.session_state["nav"] = page_name

# 라디오 버튼 내비게이션
selected_page = st.sidebar.radio("페이지 이동", menu_options, key="nav")

# -----------------------------------------------------------------------------
# PAGE 1: 홈 (안내 및 바로가기)
# -----------------------------------------------------------------------------
if selected_page == "홈":
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
        st.button("바로가기 ➔", key="btn_p1", on_click=set_page, args=("1. 언어변환 페이지",))

    with col2:
        st.markdown("### 2. AI 남한어 연습 페이지")
        st.write("은행, 병원, 관공서 등 남한 생활에 필요한 실전 대화를 AI와 자유롭게 연습할 수 있습니다.")
        st.button("바로가기 ➔", key="btn_p2", on_click=set_page, args=("2. AI 남한어 연습 페이지",))

    with col3:
        st.markdown("### 3. 주요 문화 차이 페이지")
        st.write("금융, 의료, 행정 제도 등 남북한 생활 문화 차이를 비교 표와 AI Q&A로 알기 쉽게 정리해 드립니다.")
        st.button("바로가기 ➔", key="btn_p3", on_click=set_page, args=("3. 주요 문화 차이 페이지",))

# -----------------------------------------------------------------------------
# PAGE 2: 언어변환 페이지
# -----------------------------------------------------------------------------
elif selected_page == "1. 언어변환 페이지":
    st.title("🔤 1. 언어변환 페이지")
    st.write("남한 생활 중 뜻을 잘 모르겠거나 생소한 단어 및 문장을 입력해 보세요.")

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
                result = generate_ai_response(prompt)
                st.markdown("### 💡 변환 결과")
                st.markdown(result)

# -----------------------------------------------------------------------------
# PAGE 3: AI 남한어 연습 페이지
# -----------------------------------------------------------------------------
elif selected_page == "2. AI 남한어 연습 페이지":
    st.title("💬 2. AI 남한어 연습 페이지")
    st.write("실전 상황별로 AI 직원과 가상 대화를 나누며 자연스러운 남한 표현을 연습해 보세요.")

    scenario = st.selectbox(
        "연습할 상황을 선택하세요:",
        ["은행 창구에서 계좌 개설하기", "주민센터에서 서류 발급받기", "병원 접수 및 증상 설명하기", "카페에서 음료 주문하기"]
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "last_scenario" not in st.session_state or st.session_state.last_scenario != scenario:
        st.session_state.last_scenario = scenario
        st.session_state.chat_history = [
            {"role": "assistant", "content": f"안녕하세요! **[{scenario}]** 대화 연습입니다.\n\n'어서 오세요! 무엇을 도와드릴까요?'"}
        ]

    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_chat := st.chat_input("답변을 입력하세요..."):
        st.session_state.chat_history.append({"role": "user", "content": user_chat})
        st.chat_message("user").write(user_chat)

        with st.spinner("AI 답변 생성 중..."):
            prompt = f"""
            당신은 탈북민의 남한 언어적응을 돕는 친절한 AI 대화 상대입니다.
            현재 상황: [{scenario}]

            사용자의 말: "{user_chat}"

            다음 구성을 따라 응답을 제공해 주세요:
            1. [직원 응답]: 상황에 맞는 자연스럽고 친절
