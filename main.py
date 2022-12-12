import openai as ai
import json
import streamlit as st

print("** Loading API Key")
ai.api_key = "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"

st.title("エントリーシート生成")
st.markdown("情報を入力してください。")
st.sidebar.markdown("# 何を生成したいですか？")

with st.sidebar:
    model_used = st.selectbox(
     '自己ｐｒ、学力、志望動機から選んでください。',
    ('自己ｐｒ', '学力', '志望動機'))


    if model_used == '自己ｐｒ':
        st.markdown("""[Davinci](https://beta.openai.com/docs/models/davinci)を基づいてファインディングした自己ｐｒ生成用のモデルです。
        
        """)

    elif model_used == 'text-curie-001':
        st.markdown("""[Curie](https://beta.openai.com/docs/models/curie) is extremely powerful, yet very fast. While Davinci is stronger when it 
        comes to analyzing complicated text, Curie is quite capable for many nuanced tasks like sentiment 
        classification and summarization. Curie is also quite good at answering questions and performing 
        Q&A and as a general service chatbot.
        """)
    elif model_used == 'text-babbage-001':
        st.markdown("""[Babbage](https://beta.openai.com/docs/models/babbage) can perform straightforward tasks like simple classification. It’s also quite 
        capable when it comes to Semantic Search ranking how well documents match up with search queries.
        """)
    else:
        st.markdown("""[Ada](https://beta.openai.com/docs/models/ada) is usually the fastest model and can perform tasks like parsing text, address 
        correction and certain kinds of classification tasks that don't require too much nuance. 
        da's performance can often be improved by providing more context.
        """)

    max_tokens = st.text_input("トークンの長さ:", "999")
    st.markdown("**重要:** 長すぎるとモデルの効果が悪くなるので、ご注意を！")

    st.write("ハイパーパラメータ")
    temperature = st.text_input("Temperature: ", "0.99")
    top_p = st.text_input("Top P: ", "1")
    st.write("Temperature is a number between 0 and 1 that determines how many creative risks the engine takes when generating text.")
    st.write("Top P is an alternative way to control the originality and creativity of the generated text.")


with st.form(key='my_form_to_submit'):
    company_name = st.text_input("会社名: ", "会社名を入力してください。（アマゾン、電通、ＮＴＴ、楽天など）。")
    
    your_name = st.text_input("名前：", "東大太郎")

    self_pr = st.text_input("あなたの強みは何ですか？", "強みを一つ入力してください。（責任感、チャレンジ精神、継続力、柔軟性、リーダーシップなど）。")
    
    gakuchika = st.text_input("学生時代力を入れたことは何ですか？", "学力に関すること一つ入力してください。（どこかのアルバイト、何々部のサークル、何々の勉強など）。" )

    motivation = st.text_input("あなたの入社志望動機は何ですか？：", "一言で志望動機をまとめてください。")

    submit_button = st.form_submit_button(label='提出する')

#prompt1 = ("Write a cover letter to " + " from " + your_name +" for a " + role + " job at " + company_name +"." + " I have experience in " +personal_exp + " I am excited about the job because " +job_desc + " I am passionate about "+ passion)
prompt = (self_pr + "に関する自己ｐｒを詳しく書いてください。")
if submit_button:
    # The Model
    response = ai.Completion.create(
        model = 'davinci:ft-personal:selfpr-model-2022-12-05-06-59-56',
        # engine="text-davinci-002", # OpenAI has made four text completion engines available, named davinci, ada, babbage and curie. We are using davinci, which is the most capable of the four.
        prompt=prompt, # The text file we use as input (step 3)
        max_tokens=int(max_tokens), # how many maximum characters the text will consists of.
        temperature=0.99,
        # temperature=int(temperature), # a number between 0 and 1 that determines how many creative risks the engine takes when generating text.,
        top_p=int(top_p), # an alternative way to control the originality and creativity of the generated text.
        n=1, # number of predictions to generate
        frequency_penalty=0.3, # a number between 0 and 1. The higher this value the model will make a bigger effort in not repeating itself.
        presence_penalty=0.9 # a number between 0 and 1. The higher this value the model will make a bigger effort in talking about new topics.
    )


    text = response['choices'][0]['text']
    print("Prompt:", prompt)
    print("Response:", text)

    st.subheader("入力プロンプト")
    st.write(prompt)
    st.subheader("生成結果")
    st.write(text)
    st.download_button(label='ダウンロード', file_name='entry_sheet.txt', data=text)

    #print("Other results:", response)

    with open('entry_sheet.txt', 'a') as f:
        f.write(text)