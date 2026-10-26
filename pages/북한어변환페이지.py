
import json
import re
import streamlit as st

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


st.set_page_config(
    page_title="북한어변환",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)


DICTIONARY = {
    "손전화": {
        "south": "휴대전화",
        "meaning": "가지고 다니며 통화하는 전화기",
        "difference": "남한에서는 휴대전화, 휴대폰이라는 표현을 주로 사용합니다."
    },
    "얼음보숭이": {
        "south": "아이스크림",
        "meaning": "차갑게 얼려 만든 달콤한 디저트",
        "difference": "남한에서는 아이스크림이라는 표현이 일반적입니다."
    },
    "녀성": {
        "south": "여성",
        "meaning": "여자라는 성별을 가리키는 말",
        "difference": "남한 표기에서는 두음 법칙에 따라 여성이라고 씁니다."
    },
    "로동": {
        "south": "노동",
        "meaning": "몸이나 정신을 사용하여 일하는 것",
        "difference": "남한에서는 두음 법칙에 따라 노동이라고 씁니다."
    },
    "랭면": {
        "south": "냉면",
        "meaning": "차게 먹는 국수 음식",
        "difference": "남한에서는 냉면이라고 표기합니다."
    },
    "인차": {
        "south": "곧, 이내, 바로",
        "meaning": "시간이 오래 지나지 않아",
        "difference": "문맥에 따라 곧, 이내, 바로 등으로 바꿉니다."
    },
    "꽝포": {
        "south": "허풍, 거짓말",
        "meaning": "사실과 다르거나 과장된 말을 하는 것",
        "difference": "문맥에 따라 허풍을 떨다, 거짓말하다 등으로 표현합니다."
    },
    "가락지빵": {
        "south": "도넛",
        "meaning": "고리 모양으로 만든 빵이나 과자",
        "difference": "남한에서는 도넛이라는 표현이 일반적입니다."
    },
    "살림집": {
        "south": "집, 주택",
        "meaning": "사람이 생활하며 거주하는 곳",
        "difference": "문맥에 따라 집 또는 주택으로 표현할 수 있습니다."
    },
}


SYSTEM_PROMPT = """
너는 북한의 문화어를 남한의 자연스러운 한국어로 바꾸는 언어 도우미다.
원래 의미를 바꾸거나 내용을 지어내지 마라.
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
                "meaning": item["difference"]
            })

    return {
        "converted": converted,
        "summary": (
            "등록된 북한어 표현을 찾아 변환했습니다. "
            "전체 문장의 의미는 문맥에 따라 달라질 수 있습니다."
            if differences else
            "기본 사전에서 일치하는 단어를 찾지 못했습니다. "
            "AI 분석을 사용하면 문맥에 맞는 변환을 시도할 수 있습니다."
        ),
        "differences": differences,
        "confidence": "보통" if differences else "낮음"
    }


def parse_json(text):
    text = text.strip()
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
        raise RuntimeError("google-genai 라이브러리가 설치되지 않았습니다.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=SYSTEM_PROMPT + "\n\n입력 문장:\n" + text,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json"
        )
    )

    if not response.text:
        raise ValueError("AI 응답이 비어 있습니다.")

    return parse_json(response.text)


# 번역기 스타일 디자인
st.markdown("""
<style>
    .stApp {
        background: #f8f9fc;
        color: #202b3c;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .app-header {
        margin-bottom: 30px;
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

    .language-box {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 16px;
        background: white;
        border: 1px solid #dfe4ed;
        border-bottom: 0;
        border-radius: 12px 12px 0 0;
        font-size: 15px;
        font-weight: 700;
        color: #34445b;
    }

    .language-dot {
        display: inline-block;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #5478e5;
    }

    div[data-testid="stTextArea"] textarea {
        background: #ffffff !important;
        color: #253248 !important;
        border: 1px solid #dfe4ed !important;
        border-radius: 0 0 12px 12px !important;
        font-size: 18px !important;
        line-height: 1.7 !important;
        padding: 16px !important;
    }

    div[data-testid="stTextArea"] label {
        font-weight: 600;
        color: #4b5870;
    }

    div.stButton > button {
        min-height: 44px;
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

    .result-text {
        font-size: 20px;
        line-height: 1.8;
        color: #263750;
        overflow-wrap: anywhere;
        white-space: pre-wrap;
        padding: 8px 0 16px 0;
    }

    .section-heading {
        font-size: 21px;
        font-weight: 750;
        color: #25344b;
        margin: 28px 0 12px 0;
    }

    .hint {
        font-size: 13px;
        color: #7b879b;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: white;
        border-color: #e0e5ee;
        border-radius: 12px;
    }

    @media (max-width: 700px) {
        .app-title {
            font-size: 27px;
        }
    }
</style>
""", unsafe_allow_html=True)


# 제목
st.markdown("""
<div class="app-header">
    <div class="app-title">🌐 북한어변환</div>
    <div class="app-subtitle">
        북한말을 자연스러운 한국어로 변환하고 표현의 차이를 확인하세요.
    </div>
</div>
""", unsafe_allow_html=True)


# 언어 선택 표시
lang_left, lang_arrow, lang_right = st.columns([1, 0.12, 1])

with lang_left:
    st.markdown(
        '<div class="language-box">'
        '<span class="language-dot"></span> 북한어'
        '</div>',
        unsafe_allow_html=True
    )

with lang_arrow:
    st.markdown(
        '<div style="text-align:center;padding-top:10px;'
        'font-size:22px;color:#5478e5;">→</div>',
        unsafe_allow_html=True
    )

with lang_right:
    st.markdown(
        '<div class="language-box">'
        '<span class="language-dot"></span> 한국어'
        '</div>',
        unsafe_allow_html=True
    )


if "conversion_result" not in st.session_state:
    st.session_state.conversion_result = None

if "conversion_error" not in st.session_state:
    st.session_state.conversion_error = None


# 입력과 결과
left, right = st.columns(2, gap="medium")

with left:
    user_text = st.text_area(
        "북한어 입력",
        placeholder="변환할 북한어를 입력하세요.\n\n예: 인차 손전화로 알려주겠소.",
        height=250,
        max_chars=5000,
        key="north_input",
        label_visibility="collapsed"
    )

    count_col, clear_col = st.columns(2)

    with count_col:
        st.caption(f"{len(user_text)} / 5000자")

    with clear_col:
        if st.button("입력 지우기", use_container_width=True):
            st.session_state.north_input = ""
            st.session_state.conversion_result = None
            st.session_state.conversion_error = None
            st.rerun()

    use_ai = st.toggle(
        "AI 문맥 분석",
        value=True,
        help="API 키가 없으면 기본 사전을 사용합니다."
    )

    submitted = st.button(
        "번역하기 →",
        type="primary",
        use_container_width=True
    )

with right:
    result = st.session_state.conversion_result

    if result:
        converted = result.get("converted", "")

        st.text_area(
            "한국어 변환 결과",
            value=converted,
            height=250,
            disabled=True,
            key="converted_output",
            label_visibility="collapsed"
        )

        st.caption("한국어 변환 결과")

        st.button(
            "📋 결과 복사",
            use_container_width=True,
            on_click=lambda: st.session_state.update({
                "copy_text": converted
            }),
            key="copy_result"
        )

        if st.session_state.get("copy_text") == converted:
            st.code(converted, language=None)
            st.caption(
                "위 결과를 선택해 복사하거나 다운로드 기능을 이용하세요."
            )

        st.download_button(
            "⬇️ 결과 다운로드",
            data=converted,
            file_name="북한어변환결과.txt",
            mime="text/plain",
            use_container_width=True
        )

    else:
        st.text_area(
            "한국어 변환 결과",
            value="번역 결과가 여기에 표시됩니다.",
            height=250,
            disabled=True,
            key="empty_output",
            label_visibility="collapsed"
        )
        st.caption("변환 결과가 이곳에 표시됩니다.")


# 변환 실행
if submitted:
    if not user_text.strip():
        st.session_state.conversion_error = "북한어를 먼저 입력해 주세요."
        st.session_state.conversion_result = None
        st.rerun()

    api_key = ""
    try:
        api_key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except Exception:
        pass

    result = None
    error_message = None

    if use_ai and api_key:
        try:
            with st.spinner("문맥을 분석하고 있습니다..."):
                result = ai_convert(user_text.strip(), api_key)
        except Exception as error:
            error_message = (
                "AI 요청에 실패하여 기본 사전을 사용했습니다. ("
                + type(error).__name__ + ")"
            )

    elif use_ai and not api_key:
        error_message = "API 키가 없어 기본 사전으로 변환했습니다."

    if result is None:
        result = offline_convert(user_text.strip())

    st.session_state.conversion_result = result
    st.session_state.conversion_error = error_message
    st.rerun()


if st.session_state.conversion_error:
    st.info(st.session_state.conversion_error)


# 뜻풀이와 표현 비교
result = st.session_state.conversion_result

if result:
    st.markdown(
        '<div class="section-heading">📚 뜻풀이와 표현 차이</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown("**💡 쉬운 뜻풀이**")
        st.write(result.get("summary", "뜻풀이가 없습니다."))

        st.caption(
            "분석 신뢰도: " + str(result.get("confidence", "보통"))
        )

    differences = result.get("differences", [])

    if differences:
        for item in differences:
            if not isinstance(item, dict):
                continue

            with st.container(border=True):
                word_left, word_right = st.columns(2)

                with word_left:
                    st.caption("북한어")
                    st.markdown("### " + str(item.get("north", "-")))

                with word_right:
                    st.caption("한국어")
                    st.markdown("### " + str(item.get("south", "-")))

                st.write(item.get("meaning", ""))
    else:
        st.info(
            "추가로 비교할 표현을 찾지 못했습니다. "
            "문맥에 따라 변환 결과가 달라질 수 있습니다."
        )


# 자주 찾는 단어
st.markdown(
    '<div class="section-heading">자주 찾는 북한어</div>',
    unsafe_allow_html=True
)

popular_words = ["손전화", "얼음보숭이", "녀성", "로동", "랭면", "인차"]

word_cols = st.columns(6)

for i, word in enumerate(popular_words):
    with word_cols[i]:
        if st.button(word, use_container_width=True, key="word_" + word):
            st.session_state.north_input = word
            st.rerun()


st.divider()

st.caption(
    "북한어변환 · 남북한 언어 학습 도구 | 자동 변환 결과는 참고용입니다."
)
