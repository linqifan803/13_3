
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
    page_title="북한어 변환소",
    page_icon="🗣️",
    layout="wide"
)

# 예시 사전: AI 없이도 작동하는 기본 변환
DICTIONARY = {
    "손전화": {
        "south": "휴대전화",
        "meaning": "가지고 다니며 통화하는 전화기",
        "difference": "남한에서는 휴대전화, 휴대폰이라는 표현을 주로 사용합니다."
    },
    "얼음보숭이": {
        "south": "아이스크림",
        "meaning": "차갑게 얼려 만든 달콤한 디저트",
        "difference": "남한에서는 외래어인 아이스크림이 일반적입니다."
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
사용자가 입력한 의미를 바꾸거나 내용을 지어내지 마라.
단어 뜻과 남북한 표현 차이를 쉬운 한국어로 설명하라.
문맥이 불확실하면 불확실하다고 밝혀라.
반드시 JSON 객체로만 답하라. 형식:
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

    # 긴 단어부터 찾아서 치환
    for word in sorted(DICTIONARY, key=len, reverse=True):
        if word in text:
            item = DICTIONARY[word]
            converted = converted.replace(word, item["south"])
            differences.append({
                "north": word,
                "south": item["south"],
                "meaning": item["difference"]
            })

    if differences:
        summary = (
            "예시 사전에 등록된 단어를 바꿨습니다. "
            "문맥에 따라 가장 자연스러운 표현은 달라질 수 있습니다."
        )
        confidence = "보통"
    else:
        summary = (
            "예시 사전에서 일치하는 단어를 찾지 못했습니다. "
            "AI 기능을 사용하면 문맥에 맞는 분석을 시도할 수 있습니다."
        )
        confidence = "낮음"

    return {
        "converted": converted,
        "summary": summary,
        "differences": differences,
        "confidence": confidence
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


def display_result(result):
    st.markdown("### 🇰🇷 한국어 변환 결과")
    st.text_area(
        "변환된 문장",
        value=result["converted"],
        height=120,
        key="converted_output"
    )

    st.markdown("### 💡 쉬운 뜻풀이")
    st.write(result.get("summary", "뜻풀이가 없습니다."))

    st.caption(
        "분석 신뢰도: "
        + str(result.get("confidence", "보통"))
    )

    st.markdown("### 🔍 북한어와 남한어의 차이")

    differences = result.get("differences", [])

    if not differences:
        st.info(
            "별도의 표현 차이를 찾지 못했습니다. "
            "문맥에 따라 결과를 확인해 주세요."
        )

    for item in differences:
        if not isinstance(item, dict):
            continue

        with st.container(border=True):
            left, right = st.columns(2)

            with left:
                st.markdown("**북한어**")
                st.write(item.get("north", "-"))

            with right:
                st.markdown("**남한어**")
                st.write(item.get("south", "-"))

            st.caption(item.get("meaning", ""))


# 화면 디자인
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f8fc;
    }
    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #203c60;
        text-align: center;
        padding: 12px 0 4px 0;
    }
    .sub-title {
        text-align: center;
        color: #63758a;
        margin-bottom: 28px;
    }
    div.stButton > button[kind="primary"] {
        background-color: #376da8;
        border-radius: 10px;
        height: 48px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">🗣️ 북한어 변환소</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">'
    '북한말을 자연스러운 한국어로 바꾸고 표현의 차이를 알아보세요.'
    '</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("📖 이용 안내")
    st.write("1. 북한어 단어나 문장을 입력하세요.")
    st.write("2. 변환 버튼을 누르세요.")
    st.write("3. 변환 결과와 뜻풀이를 확인하세요.")

    st.divider()
    st.markdown("**변환 예시**")
    for word in DICTIONARY:
        st.write("• " + word)

    st.caption(
        "AI 기능을 사용하려면 Streamlit Secrets에 "
        "GEMINI_API_KEY를 등록하세요."
    )

left, right = st.columns(2, gap="large")

with left:
    st.markdown("### 📝 북한어 입력")

    user_text = st.text_area(
        "변환할 북한어",
        placeholder="예: 인차 손전화로 알려주겠소.",
        height=200,
        max_chars=5000
    )

    use_ai = st.toggle(
        "AI 문맥 분석 사용",
        value=True,
        help="API 키가 없으면 예시 사전으로 변환합니다."
    )

    submitted = st.button(
        "한국어로 변환하기 →",
        type="primary",
        use_container_width=True
    )

with right:
    st.markdown("### ✨ 변환 결과")

    if not submitted:
        st.info("왼쪽에 북한어를 입력하고 변환 버튼을 눌러주세요.")

        st.markdown("**이런 기능을 이용할 수 있어요.**")
        st.write("✔ 자연스러운 한국어로 변환")
        st.write("✔ 단어의 의미를 쉽게 설명")
        st.write("✔ 남북한 표현의 차이 비교")

    elif not user_text.strip():
        st.warning("변환할 단어나 문장을 입력해 주세요.")

    else:
        try:
            api_key = str(
                st.secrets.get("GEMINI_API_KEY", "")
            ).strip()
        except Exception:
            api_key = ""

        if use_ai and api_key:
            try:
                with st.spinner("AI가 문맥을 분석하고 있습니다..."):
                    result = ai_convert(user_text.strip(), api_key)

                st.success("AI 문맥 분석 완료")
                display_result(result)

            except Exception as error:
                st.warning(
                    "AI 요청에 실패했습니다. "
                    "예시 사전 기반 결과를 표시합니다."
                )
                st.caption(
                    "오류 유형: " + type(error).__name__
                    + ". API 키, 네트워크 및 모델 설정을 확인하세요."
                )
                display_result(offline_convert(user_text.strip()))

        else:
            if use_ai and not api_key:
                st.info(
                    "GEMINI_API_KEY가 등록되지 않아 "
                    "예시 사전으로 변환합니다."
                )

            display_result(offline_convert(user_text.strip()))

st.divider()

st.caption(
    "이 서비스는 언어 학습용 참고 도구입니다. "
    "예시 사전은 제한적이며 자동 변환 결과에는 오류가 있을 수 있습니다."
)
