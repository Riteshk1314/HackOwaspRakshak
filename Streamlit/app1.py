from app import result_dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]="ls__4bbef910784e41889d4bcf7604a10781"
#prompt template 
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","you are  helpful emotionally intelligent assistant please reply to the user's question keep in mind that user has also defined his emotions"),
        ("user","Question:{question}")
    ]
)
## streamlit framework

st.title('Langchain Demo With LLAMA2 API')


# ollama LLAma2 LLm 
llm=Ollama(model="llama2:13b")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

result_string = ""

for sentence, emotions in result_dict.items():
    # Format the emotions list into a string
    emotions_str = ', '.join(emotions)
    # Construct the sentence with emotions in brackets
    sentence_with_emotions = f"[{emotions_str}] {sentence}\n"
    result_string += sentence_with_emotions
input_text=st.text_input("reply")
print(result_string)
if result_string:
    st.write(chain.invoke({"question":result_string}))