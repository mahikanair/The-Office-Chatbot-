from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI 
from googleapiclient.discovery import build
import warnings
import yaml
warnings.filterwarnings("ignore")

'''#get openai api key - USE THIS PART BY CREATING YOUR OWN YAML FILE WHEN HOSTING THE APP LOCALLY 
with open('./myauth.yaml', "r") as f:
    credentials = yaml.safe_load(f)
openai_api_key = credentials.get('openai', {}).get('access_key')
gemini_api_key = credentials.get('gemini', {}).get('access_key')
yt_api_key = credentials.get('youtube', {}).get('access_key')
'''


#for privacy reasons getting api keys this way 
openai_api_key = st.secrets['OPENAI']
gemini_api_key = st.secrets['GEMINI']
yt_api_key = st.secrets['YOUTUBE']

embeddings = OpenAIEmbeddings(openai_api_key = openai_api_key)
db = Chroma(persist_directory='./db', embedding_function=embeddings) 
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

#this is for your youtube search - find a related video that could interest the user 
def search_youtube(query):
    youtube = build("youtube", "v3", developerKey=yt_api_key)
    request = youtube.search().list(part="snippet", q=query, type="video", maxResults=1)
    response = request.execute()

    if 'items' in response and response['items']:
        video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    else:
        return None
    
def QnA_Prompt(query):
  answer = db.similarity_search_with_relevance_scores(query, k=2) #get top 2 responses together incase the first one itself isn't sufficient 
  source = "\n".join([doc.page_content for doc, _ in answer])
  print('The context:',source) #to see what chunk it comes up with 
  #we make sure to tell OpenAI to only answer from the context and say I don't know if it's not present 
  p = f"Use only the source I have given to give an answer to the question. If you are not able to find an answer in the source, say that you don't know and require further context to answer the question. When you are able to answer the question, just answer it, do not say 'the source says' or mention that you got it from an article. Always ask for further context if you cannot find the answer. Do not make up an answer. Source : {source}, Question {query}"
  return p

# defining the streamlit app layout
st.title("The Office - An American Workplace ChatBot")
st.markdown("Hi! I'm a chatbot made for The Office newbies! Ever feel lost when your friends make references from the office and you have no idea what they're talking about? Or you want to quickly understand what all the hype is about, surrounding this show? Or perhaps you're a fan who cant remeber some aspects of the show and want to quickly verify? Well, That's what I'm here for! Ask me a question about the office and I'll give you an answer while taking you to a youtube video that pertains to your question. Yes, this is only for the American version of the show (which we all know, deep down, is better)")
st.image("./The office.jpeg", use_column_width=True)

#giving the user some prompts to get started, which becmomes a query from the user if pressed 
user_prompt1 = st.button("What is The Office?")
user_prompt2 = st.button("Who Created the Office?")
user_prompt3 = st.button("What happens in the dinner party episode?")

#if we dont have a history of messages yet we create it 
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        
query = st.chat_input("Hi There! Ask any questions you may have about The Office (US)") #this will be there in the search bar when there is no input from the user 

#button query creation
if user_prompt1:
    query = "What is The Office?"
elif user_prompt2:
    query = "Who Created the Office?"
elif user_prompt3:
    query = "What happens in the dinner party episode?"

if query: #if we get a query from the user 
    with st.chat_message('user'):
        st.markdown(query)
    st.session_state.messages.append({'role':'user', 'content':query}) #what the user said
    pr = QnA_Prompt(query)
    answer = llm.invoke(pr) 
    video_prompt = llm.invoke(f"Turn Question:{pr} + Answer:{answer} into a compact sentence that could be put into youtubes search bar to get to a related video the user might be interested in. Incase the Answer part was along the lines of I dont know, respond with the exact words in uppercase: 'NOTHING'")
    video_link = None
    if 'NOTHING' not in video_prompt: #condition we have given for when the RAG chatbot cant find the answer, so we wouldn't want it to show a random video that doesnt pertain to the office
        video_link = search_youtube(video_prompt)
    if video_link:
        video_answer = f'Here is a link that might interest you {video_link}'
        answer = answer + "\n" + video_answer #add link to the prompt 
    with st.chat_message('assistant'):
        st.markdown(answer) 
    st.session_state.messages.append({'role':'assistant', 'content':answer}) #what the chatbot responded with 
