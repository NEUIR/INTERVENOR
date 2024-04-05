from openai import OpenAI
import streamlit as st

with st.sidebar:
    # logo = "demo/figures/logo.png"
    # st.sidebar.image(logo,width=200)
    st.sidebar.title("About INTERVENOR 🎈 ")

    markdown = """
INTERVENOR conducts an interactive code-repair process, facilitating the collaboration among agents and the code compiler.
- 📜 [Paper](https://arxiv.org/abs/2311.09868)
- [![Open in GitHub](https://github.com/codespaces/badge.svg)](https://github.com/NEUIR/INTERVENOR)
"""
    st.sidebar.info(markdown)

    st.sidebar.subheader("OpenAI API Key 🎈 ")
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "🌐 [Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title(":sunglasses: INTERVENOR")
st.caption("🚀 Your code repair assistant!")


# 这段代码检查st.session_state中是否不存在键为"messages"的项目。如果不存在，它将使用包含一个字典的列表初始化st.session_state["messages"]
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi, I am INTERVENOR, a code bug repair assistant developed by NEUIR."}]

# 将messages中的内容写入到聊界面
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# 检查是否有用户在聊天输入框中输入了内容，如果有的话，将内容赋值给prompt。
if prompt := st.chat_input():
    # 检查是否已经设置了OpenAI API密钥。如果没有设置密钥，它会在应用程序界面上显示一条信息，提示用户添加OpenAI API密钥以继续。然后通过st.stop()停止应用程序的执行。
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()


    client = OpenAI(api_key=openai_api_key)
    prompt = "Here is a buggy code, please point out the error in the code, provide the repair method and correct code.\n" + prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    try:
        exec(prompt)
    except Exception as e:
        exec_result = e
    response = client.chat.completions.create(model="gpt-3.5-turbo-0125", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    response = f"""
    Execution Results:
    {exec_result}
    
    Repair Method:
    {msg}
    """
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
