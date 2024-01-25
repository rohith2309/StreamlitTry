import streamlit as st
import os
from pathlib import Path
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage

class pdf_metaData:
  def __init__(self):
    self.fileName_ind=None
    
  def setfilename(self,fileName):
   self.fileName_ind=fileName
   
  def getfilename(self):
    return self.fileName_ind
  
meta=pdf_metaData()
@st.cache(allow_output_mutation=True)
def get_chat_history():
        return []
    

 
def update_chat_history(chat_history, user_input, response):
      chat_history.append(f"<b>You:</b> {user_input}<br><b>ChatGPT:</b> {response}<br>")
     
def main():
  os.environ["OPENAI_API_KEY"]='ENTER YOUR OPENAI API KEY'
  st.title("file saver")
  menu=["upload_pdf","query"]
  choice=st.sidebar.selectbox("Menu",menu)
  global fileName
  
  #fileName_ind=""
  #fileName=""
  if choice=="upload_pdf":
     uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
   
      
   
     if uploaded_file is not None:
       fileName,file_ext=os.path.splitext(uploaded_file.name)
       if os.path.isdir(fileName):
        st.warning("file is already uploaded goto query...")
       else:  
        os.makedirs(fileName,mode=0o777)
        save_path = Path(os.getcwd(),fileName)
        dest_path=Path(save_path,uploaded_file.name)
        with open(dest_path, mode='wb') as w:
           w.write(uploaded_file.getbuffer())
        doc=SimpleDirectoryReader(fileName).load_data()
        index=VectorStoreIndex.from_documents(doc)
        fileName_ind=fileName+"index"
        st.session_state['name']=fileName_ind
        meta.setfilename(fileName_ind)
        st.warning(meta.getfilename())  
        st.warning(st.session_state.name)
       #with open(fileName_ind, mode='w') as w:
          # w.write(fileName_ind)
       #index.storage_context.persist(persist_dir="index_")
       index.storage_context.persist(persist_dir=st.session_state.name)
          
          
  elif choice=="query":
        st.warning(st.session_state.name)
         #storage_context=StorageContext.from_defaults(persist_dir="index_")
        storage_context_=StorageContext.from_defaults(persist_dir=st.session_state.name)
        index=load_index_from_storage(storage_context_) 
     
        global query_engine
        query_engine=index.as_query_engine() 
        user_input = st.text_input("You:")
        print(user_input)
        chat_history = get_chat_history()       
        if st.button("Send"):
         if user_input:
          if query_engine is not None:  
            response = get_chatbot_response(user_input)
            update_chat_history(chat_history, user_input, response)

        for entry in chat_history:
          st.markdown(entry, unsafe_allow_html=True)      
  
def get_chatbot_response(user_input):
     # Replace this function with your chatbot logic or API call
     # For simplicity, echo user input in this example
     response=query_engine.query(user_input)
     return f"Assistant: {response}"

if __name__ == "__main__":
    
    main()