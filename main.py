import openai as ai
import json
import streamlit as st

print("** Loading API Key")
ai.api_key = "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" #prepare your own openAI API Key

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

    elif model_used == '学力':
        st.markdown("""[Davinci](https://beta.openai.com/docs/models/davinci)を基づいてファインディングしたガクチカ生成用のモデルです。

        """)
    elif model_used == '志望動機':
        st.markdown("""[Davinci](https://beta.openai.com/docs/models/davinci)を基づいてファインディングした志望動機生成用のモデルです。

        """)


    max_tokens = st.text_input("トークンの長さ:", "499")
    st.markdown("**重要:** 長すぎるとモデルの効果が悪くなるので、ご注意を！")

    st.write("ハイパーパラメーター")
    temperature = st.text_input("Temperature: ", "0.99")
    top_p = st.text_input("Top P: ", "1")
    st.write("Temperature is a number between 0 and 1 that determines how many creative risks the engine takes when generating text.")
    st.write("Top P is an alternative way to control the originality and creativity of the generated text.")


with st.form(key='my_form_to_submit'):
    company_name = st.text_input("会社名: ", "会社名を入力してください。（アマゾン、電通、ＮＴＴ、楽天など）。")
    
    your_name = st.text_input("名前：", "東大太郎")

    self_pr = st.text_input("あなたの強みは何ですか？", "強みを一つ入力してください。（責任感、チャレンジ精神、継続力、柔軟性、リーダーシップなど）。")

    motivation = st.text_input("あなたはどのような業界に入りたいですか？", "（コンサル業界、金融業界、銀行業界、メーカー業界、食品業界など）。")

    submit_button = st.form_submit_button(label='提出する')

if model_used == '自己ｐｒ':
    prompt = (self_pr + "に関する自己ｐｒを詳しく書いてください。")
if model_used == '学力':
    prompt = ("学生時代力を入れたことについて聞かせてください。")
if model_used == '志望動機':
    prompt = (motivation + "の志望動機について聞かせてください。")





if submit_button:
    # The Model
    if model_used == '自己ｐｒ':
        response = ai.Completion.create(
            model = 'davinci:ft-personal:model-prnew-2023-01-05-08-19-29', 
            # engine="text-davinci-002", # OpenAI has made four text completion engines available, named davinci, ada, babbage and curie. We are using davinci, which is the most capable of the four.
            prompt=prompt, # The text file we use as input (step 3)
            max_tokens=int(max_tokens), # how many maximum characters the text will consists of.
            temperature=float(temperature), # a number between 0 and 1 that determines how many creative risks the engine takes when generating text.,
            top_p=int(top_p), # an alternative way to control the originality and creativity of the generated text.
            n=1, # number of predictions to generate
            frequency_penalty=0.3, # a number between 0 and 1. The higher this value the model will make a bigger effort in not repeating itself.
            presence_penalty=0.6 # a number between 0 and 1. The higher this value the model will make a bigger effort in talking about new topics.
        )
    elif model_used == '学力':
         response = ai.Completion.create(
            model = 'davinci:ft-personal:model-gakuchika-2023-01-05-07-37-55', 
            # engine="text-davinci-002", # OpenAI has made four text completion engines available, named davinci, ada, babbage and curie. We are using davinci, which is the most capable of the four.
            prompt=prompt, # The text file we use as input (step 3)
            max_tokens=int(max_tokens), # how many maximum characters the text will consists of.
            temperature=float(temperature), # a number between 0 and 1 that determines how many creative risks the engine takes when generating text.,
            top_p=int(top_p), # an alternative way to control the originality and creativity of the generated text.
            n=1, # number of predictions to generate
            frequency_penalty=0.3, # a number between 0 and 1. The higher this value the model will make a bigger effort in not repeating itself.
            presence_penalty=0.6 # a number between 0 and 1. The higher this value the model will make a bigger effort in talking about new topics.
        )       
    elif model_used == '志望動機':
         response = ai.Completion.create(
            model = 'davinci:ft-personal:newmodel-forpr-2023-01-05-07-13-24', 
            # engine="text-davinci-002", # OpenAI has made four text completion engines available, named davinci, ada, babbage and curie. We are using davinci, which is the most capable of the four.
            prompt=prompt, # The text file we use as input (step 3)
            max_tokens=int(max_tokens), # how many maximum characters the text will consists of.
            temperature=float(temperature), # a number between 0 and 1 that determines how many creative risks the engine takes when generating text.,
            top_p=int(top_p), # an alternative way to control the originality and creativity of the generated text.
            n=1, # number of predictions to generate
            frequency_penalty=0.3, # a number between 0 and 1. The higher this value the model will make a bigger effort in not repeating itself.
            presence_penalty=0.6 # a number between 0 and 1. The higher this value the model will make a bigger effort in talking about new topics.
        ) 


    text = response['choices'][0]['text']
    print("Prompt:", prompt)
    print("Response:", text)

    st.subheader("入力プロンプト")
    st.write(prompt)
    st.subheader("生成結果")
    st.write(text)
    st.download_button(label='ダウンロード', file_name='entry_sheet.txt', data=text)



    with open('entry_sheet.txt', 'a') as f:
        f.write(text)