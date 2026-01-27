from datetime import datetime
from langchain_core.messages import SystemMessage
import streamlit as st


if "document_database" not in st.session_state:
    st.session_state.document_database = {}

removing_system_message = SystemMessage(f"""
Sen bir yapay zeka asistanısın ve görevlerin                                       
* Kullanıcı sana silmek istediği bir dosyanın ismini gönderecek
* Bu dosya ismini 'name_of_file_that_will_be_removed' alanına ekle
* Sadece 'name_of_file_that_will_be_removed' alanını doldur ve başka hiçbir şey ekleme.
* Yukarıdaki görevlerin haricinde başka herhangi bir şey yapmamalısın                                                        
                                        """)

def removing_system_message_function():
    return removing_system_message


llm_call_router_system_message = SystemMessage(
    content="""Kullanıcı girdisini aşağıdaki 4 niyetten birine yönlendir:
                    - 'add_document' : Kullanıcı bir şey eklemek istiyorsa, buraya yönlendir
                    - 'delete_document' : Kullanıcı bir şey silmek istiyorsa,  buraya yönlendir
                    - 'ask_document' : Kullanıcı herhangi bir soru soruyorsa,  buraya yönlendir
                    - 'list_documents' : Kullanıcı veritabanındaki bulunan notları ya da belgeleri bir liste olarak görmek istiyorsa, buraya yönlendir
                    Bu 4 değer haricinde başka bir değer döndürmemelisin
                    """
)

def llm_call_router_system_message_function():
    return llm_call_router_system_message


ask_document_tool_system_message = SystemMessage(content=f""" If the user requests information about a document, respond using this database: {st.session_state.document_database}

If you can't find the answer you're looking for in the database, you can use the "I couldn't find the answer to your question in the database" option.

""")

def ask_document_tool_system_message_function():
    return ask_document_tool_system_message


list_documents_system_message = SystemMessage(f"""
        When this question arrives, you will first show the user all the documents currently stored in the database as a list.
        
        
        Example structure:
        For Example:
        - Document Name in Database
        - Document Value or content in Database  
        - Document Name in Database
        - Document Value or content in Database 
        ..................................................................
        The document list must be generated using the current document database contents:  
        don't use any documents except this source{st.session_state.document_database}
        
        """)

def list_documents_system_message_function():
    return list_documents_system_message