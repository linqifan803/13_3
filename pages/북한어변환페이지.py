
import json
import re
import streamlit as st

# ==========================================
# 1. 기본 설정 및 AI 라이브러리
# ==========================================
st.set_page_config(
    page_title="북한어변환",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


# ==========================================
# 2. 북한어 기본 사전
# ==========================================
DICTIONARY = {
    "손전화": {
        "south": "휴대전화",
        "meaning": "가지고 다니며 통화하는 전화기",
        "difference": "남한에서는 휴대전화 또는 휴대폰이라는 표현을 주로 사용합니다.",
    },
    "얼음보숭이": {
        "south": "아이스크림",
        "meaning": "차갑게 얼려 만든 달콤한 디저트",
        "difference": "남한에서는 아이스크림이라는 표현이 일반적입니다.",
    },
    "녀성": {
        "south": "여성",
        "meaning": "여자라는 성별을 가리키는 말",
        "difference": "남한 표기에서는 두음 법칙에 따라 여성이라고 씁니다.",
    },
    "로동": {
        "south": "노동",
        "meaning": "몸이나 정신을 사용하여 일하는 것",
        "difference": "남한에서는 두음 법칙에 따라 노동이라고 씁니다.",
    },
    "랭면": {
        "south": "냉면",
        "meaning": "차게 먹는 국수 음식",
        "difference": "남한에서는 냉면이라고 표기합니다.",
    },
    "인차": {
        "south": "곧, 이내, 바로",
        "meaning": "시간이 오래 지나지 않아",
        "difference": "문맥에 따라 곧, 이내, 바로 등으로 바꿉니다.",
    },
    "꽝포": {
        "south": "허풍, 거짓말",
        "meaning": "사실과 다르거나 과장된 말을 하는 것",
        "difference": "문맥에 따라 허풍을 떨다, 거짓말하다 등으로 표현합니다.",
    },
    "가락지빵": {
        "south": "도넛",
        "meaning": "고리 모양으로 만든 빵이나 과자",
        "difference": "남한에서는 도넛이라는 표현이 일반적입니다.",
    },
    "살림집": {
        "south": "집, 주택",
        "meaning": "사람이 생활하며 거주하는 곳",
        "difference": "문맥에 따라 집 또는 주택으로 표현할 수 있습니다.",
    },
}

SYSTEM_PROMPT = """
너는 북한의 문화어를 남한의 자연스러운 한국어로 바꾸는 언어 도우미다.
원래 의미를 바꾸거나 내용을 지어내지 마라.
문맥에 맞게 자연스러운 한국어로 바꿔라.
단어 뜻과 남북한 표현 차이를 쉬운 한국어로 설명하라.
문맥이 불확실하면 불확실하다고 밝혀라.
반드시 JSON 객체로만 답하라.

{
  "converted": "자연스러운 한국어 변환 결과",
  "summary": "쉬운 뜻풀이",
  "differences": [
    {
      "north": "북한어",
      "south": "남한어",
      "meaning": "뜻과 표현 차이"
    }
  ],
  "confidence": "높음/보통/낮음"
}
"""


# ==========================================
# 3. 변환 함수
# ==========================================
def offline_convert(text):
    converted = text
    differences = []

    for word in sorted(DICTIONARY, key=len, reverse=True):
        if word in text:
            item = DICTIONARY[word]
            converted = converted.replace(word, item["south"])

            differences.append({
                "north": word,
                "south": item["south"],
                "meaning": item["difference"],
            })

    if differences:
        summary = (
            "기본 사전에서 일치하는 북한어 표현을 찾아 변환했습니다. "
            "전체 문장의 의미는 문맥에 따라 달라질 수 있습니다."
        )
        confidence = "보통"
    else:
        summary = (
            "기본 사전에서 일치하는 단어를 찾지 못했습니다. "
            "AI 문맥 분석을 사용하면 더 자연스러운 변환을 시도할 수 있습니다."
        )
        confidence = "낮음"

    return {
        "converted": converted,
        "summary": summary,
        "differences": differences,
        "confidence": confidence,
    }


def parse_json(response_text):
    text = response_text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("AI 응답 형식이 올바르지 않습니다.")

    data = json.loads(text[start:end + 1])

    if not isinstance(data, dict):
        raise ValueError("AI 응답이 JSON 객체가 아닙니다.")

    if not isinstance(data.get("converted"), str):
        raise ValueError("변환 결과가 없습니다.")

    data.setdefault("summary", "뜻풀이가 없습니다.")
    data.setdefault("differences", [])
    data.setdefault("confidence", "보통")

    if not isinstance(data["differences"], list):
        data["differences"] = []

    return data


def ai_convert(text, api_key):
    if genai is None:
        raise RuntimeError(
            "google-genai 라이브러리가 설치되지 않았습니다."
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=SYSTEM_PROMPT + "\n\n입력 문장:\n" + text,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
        ),
    )

    if not response.text:
        raise ValueError("AI 응답이 비어 있습니다.")

    return parse_json(response.text)


# ==========================================
# 4. 세션 상태 및 버튼 콜백
# ==========================================
if "north_input" not in st.session_state:
    st.session_state.north_input = ""

if "conversion_result" not in st.session_state:
    st.session_state.conversion_result = None

if "conversion_error" not in st.session_state:
    st.session_state.conversion_error = None


def clear_north_input():
    st.session_state.north_input = ""
    st.session_state.conversion_result = None
    st.session_state.conversion_error = None


def choose_word(word):
    st.session_state.north_input = word
    st.session_state.conversion_result = None
    st.session_state.conversion_error = None


# ==========================================
# 5. 화면 디자인
# ==========================================
st.markdown(
    """
    <style>
    .stApp {
        background: #f7f8fc;
        color: #243047;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .app-header {
        margin-bottom: 28px;
    }

    .app-title {
        font-size: 32px;
        font-weight: 800;
        color: #202b3c;
        letter-spacing: -1px;
    }

    .app-subtitle {
        color: #758096;
        font-size: 15px;
        margin-top: 6px;
    }

    /* 양쪽 언어 표시 칸을 같은 높이로 */
    .language-box {
        width: 100%;
        height: 52px;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        gap: 9px;
        padding: 0 16px;
        background: #ffffff;
        border: 1px solid #dfe4ed;
        border-radius: 12px 12px 0 0;
        font-size: 16px;
        font-weight: 700;
        color: #34445b;
    }

    .language-dot {
        display: inline-block;
        width: 9px;
        height: 9px;
        flex-shrink: 0;
        border-radius: 50%;
        background: #5478e5;
    }

    /* 입력창과 결과창의 크기와 모양 통일 */
    div[data-testid="stTextArea"] {
        width: 100%;
    }

    div[data-testid="stTextArea"] textarea {
        box-sizing: border-box;
        background: #ffffff !important;
        color: #253248 !important;
        border: 1px solid #dfe4ed !important;
        border-radius: 0 0 12px 12px !important;
        font-size: 17px !important;
        line-height: 1.7 !important;
        padding: 16px !important;
    }

    div[data-testid="stTextArea"] label {
        font-weight: 600;
        color: #4b5870;
    }

    /* 모든 버튼 높이 통일 */
    div.stButton > button,
    div.stDownloadButton > button {
        min-height: 44px;
        width: 100%;
        border-radius: 9px;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"] {
        background: #4268db;
        border: 1px solid #4268db;
        color: white;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #3455bd;
        border-color: #3455bd;
    }

    .section-heading {
        font-size: 21px;
        font-weight: 750;
        color: #25344b;
        margin: 28px 0 12px 0;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border-color: #e0e5ee;
        border-radius: 12px;
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .app-title {
            font-size: 27px;
        }

        .app-subtitle {
            font-size: 14px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 6. 제목
# ==========================================
st.markdown(
    """
    <div class="app-header">
        <div class="app-title">🌐 북한어변환</div>
        <div class="app-subtitle">
            북한말을 자연스러운 한국어로 변환하고 표현의 차이를 확인하세요.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 7. 대칭형 번역 영역
# ==========================================
# 언어 표시와 입력·결과 영역 모두 같은 비율로 나눕니다.
left, right = st.columns([1, 1], gap="medium")

with left:
    st.markdown(
        '<div class="language-box">'
        '<span class="language-dot"></span> 북한어'
        '</div>',
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        '<div class="language-box">'
        '<span class="language-dot"></span> 한국어'
        '</div>',
        unsafe_allow_html=True,
    )

left, right = st.columns([1, 1], gap="medium")

with left:
    user_text = st.text_area(
        "북한어 입력",
        placeholder="변환할 북한어를 입력하세요.\n\n예: 인차 손전화로 알려주겠소.",
        height=250,
        max_chars=5000,
        key="north_input",
        label_visibility="collapsed",
    )

    count_col, clear_col = st.columns([1, 1], gap="small")

    with count_col:
        st.caption(f"{len(user_text)} / 5000자")

    with clear_col:
        st.button(
            "입력 지우기",
            on_click=clear_north_input,
            use_container_width=True,
        )

    use_ai = st.toggle(
        "AI 문맥 분석",
        value=True,
        help="API 키가 없거나 AI 요청이 실패하면 기본 사전을 사용합니다.",
    )

    submitted = st.button(
        "번역하기 →",
        type="primary",
        use_container_width=True,
    )

with right:
    result = st.session_state.conversion_result

    # 결과 유무와 관계없이 같은 위젯을 사용해 칸의 크기를 유지합니다.
    output_text = (
        result.get("converted", "")
        if result
        else "번역 결과가 여기에 표시됩니다."
    )

    st.text_area(
        "한국어 변환 결과",
        value=output_text,
        height=250,
        disabled=True,
        key="converted_output",
        label_visibility="collapsed",
    )

    if result:
        st.caption("한국어 변환 결과")

        st.download_button(
            "⬇️ 결과 다운로드",
            data=result.get("converted", ""),
            file_name="북한어변환결과.txt",
            mime="text/plain",
            use_container_width=True,
        )
    else:
        st.caption("변환 결과가 이곳에 표시됩니다.")


# ==========================================
# 8. 변환 실행
# ==========================================
if submitted:
    text_to_convert = user_text.strip()

    if not text_to_convert:
        st.session_state.conversion_error = (
            "북한어를 먼저 입력해 주세요."
        )
        st.session_state.conversion_result = None
        st.rerun()

    api_key = ""

    try:
        api_key = str(
            st.secrets.get("GEMINI_API_KEY", "")
        ).strip()
    except Exception:
        api_key = ""

    result = None
    error_message = None

    if use_ai and api_key:
        try:
            with st.spinner("문맥을 분석하고 있습니다..."):
                result = ai_convert(text_to_convert, api_key)
        except Exception as error:
            error_message = (
                "AI 변환에 실패하여 기본 사전으로 변환했습니다. "
                f"오류 유형: {type(error).__name__}"
            )

    elif use_ai and not api_key:
        error_message = (
            "API 키가 설정되지 않아 기본 사전으로 변환했습니다. "
            "AI 기능을 사용하려면 Streamlit Secrets에 "
            "GEMINI_API_KEY를 설정해 주세요."
        )

    if result is None:
        result = offline_convert(text_to_convert)

    st.session_state.conversion_result = result
    st.session_state.conversion_error = error_message
    st.rerun()


# ==========================================
# 9. 오류 및 안내 메시지
# ==========================================
if st.session_state.conversion_error:
    st.info(st.session_state.conversion_error)


# ==========================================
# 10. 뜻풀이와 표현 차이
# ==========================================
result = st.session_state.conversion_result

if result:
    st.markdown(
        '<div class="section-heading">📚 뜻풀이와 표현 차이</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown("**💡 쉬운 뜻풀이**")
        st.write(result.get("summary", "뜻풀이가 없습니다."))

        st.caption(
            "분석 신뢰도: "
            + str(result.get("confidence", "보통"))
        )

    differences = result.get("differences", [])

    if differences:
        for index, item in enumerate(differences):
            if not isinstance(item, dict):
                continue

            with st.container(border=True):
                word_left, word_right = st.columns([1, 1], gap="medium")

                with word_left:
                    st.caption("북한어")
                    st.markdown(
                        "### " + str(item.get("north", "-"))
                    )

                with word_right:
                    st.caption("한국어")
                    st.markdown(
                        "### " + str(item.get("south", "-"))
                    )

                st.write(item.get("meaning", ""))
    else:
        st.info(
            "추가로 비교할 표현을 찾지 못했습니다. "
            "문맥에 따라 변환 결과가 달라질 수 있습니다."
        )


# ==========================================
# 11. 자주 찾는 북한어
# ==========================================
st.markdown(
    '<div class="section-heading">자주 찾는 북한어</div>',
    unsafe_allow_html=True,
)

popular_words = [
    "손전화",
    "얼음보숭이",
    "녀성",
    "로동",
    "랭면",
    "인차",
]

word_cols = st.columns(6, gap="small")

for i, word in enumerate(popular_words):
    with word_cols[i]:
        st.button(
            word,
            key="word_" + word,
            use_container_width=True,
            on_click=choose_word,
            args=(word,),
        )


# ==========================================
# 12. 하단 안내
# ==========================================
st.divider()

st.caption(
    "북한어변환 · 남북한 언어 학습 도구 | "
    "자동 변환 결과는 참고용입니다."
)
