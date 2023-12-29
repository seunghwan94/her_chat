import openai
import streamlit as st
from streamlit_chat import message

# 사용할 모델 버전
model = 'gpt-3.5-turbo'

# 실제 API 키를 입력하세요
api_key = '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'
#api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = api_key

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []
    st.session_state.messages.append({"role": "system", "content":
        """애니메이션 '짱구는 못말려'에서 맹구 캐릭터로 대화를 진행합니다. 맹구의 특징적인 말투, 행동 및 성격을 반영하여, 다음과 같은 방식으로 응답하세요.
        1. **맹구의 말투 사용**: 특유의 억양과 단어 선택을 사용합니다.
        2. **성격 반영**: 맹구의 무던하고 소심한 성격을 표현합니다.
        3. **반응 스타일**: 맹구 특유의 반응 방식을 따릅니다.
        예시:사용자: 맹구야, 오늘 날씨 어때?
        맹구 챗봇: 음, 나가 보진 않았지만 창문으로 보니까 햇살이 쨍쨍하네. 나가서 놀기 좋은 날씨 같아!
        사용자: 맹구, 수학 숙제 좀 도와줘.
        맹구 챗봇: 수학 숙제라... 나도 잘 못하지만, 함께 생각해보자. 뭐가 어려운 건데?"""
        })


def add_user_message(content):
    st.session_state.messages.append({"role": "user", "content": content})

def add_bot_response():
    try:
        print(st.session_state.messages)
        completion = openai.ChatCompletion.create(
            model=model,
            messages=st.session_state.messages,
            temperature=0.3,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        response = completion.choices[0].message['content']
        st.session_state.messages.append({"role": "assistant", "content": response})
        print(st.session_state.messages)
        return response
    except Exception as e:
        print(f"GPT Error: {str(e)}")
        return None


st.header("🤖chatGPT3.5v")

# 입력 폼
with st.form('form', clear_on_submit=True):
    user_input = st.text_input('You: ', '', key='input')
    submitted = st.form_submit_button('Send')

if submitted and user_input:
    add_user_message(user_input)
    output = add_bot_response()
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# 메시지 출력
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))