from typing_extensions import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from os import getenv
from langchain_mistralai.chat_models import ChatMistralAI
from BaseModel import Adding_to_Document_Database,Removing_from_Document_Database
from Adding_system_message import adding_system_message_function
from Removing_system_message import removing_system_message_function


load_dotenv("Bilgiler.env",verbose=True)
api_key = getenv("MISTRAL_API_KEY")

# openai/gpt-oss-120b

if "document_database" not in st.session_state:
    st.session_state.document_database = {}


print("Streamlit baştan çalışıyor")

if "messages" not in st.session_state:
    print("st.session_state.messages was created")
    st.session_state.messages = []

llm = ChatMistralAI(model_name="mistral-large-2512",api_key=api_key)

class State(TypedDict):
    input : str 
    decision : str | None
    output : str | None
    next : str | None



class Route(BaseModel):
    step : Literal["add_document","delete_document","ask_document","list_documents"] = Field(None,description="The next step in the routing process")

router = llm.with_structured_output(Route)

try:

    def llm_call_router(state: State):

        """Route the user input to the appropriate node"""
        # Run the augmented LLM with structured output to serve as routing logic
        decision = router.invoke(
            [
                SystemMessage(
                    content="""Kullanıcı girdisini aşağıdaki 4 niyetten birine yönlendir:
                    - 'add_document' : Kullanıcı bir şey eklemek istiyorsa, buraya yönlendir
                    - 'delete_document' : Kullanıcı bir şey silmek istiyorsa,  buraya yönlendir
                    - 'ask_document' : Kullanıcı herhangi bir soru soruyorsa,  buraya yönlendir
                    - 'list_documents' : Kullanıcı veritabanındaki bulunan notları ya da belgeleri bir liste olarak görmek istiyorsa, buraya yönlendir
                    Bu 4 değer haricinde başka bir değer döndürmemelisin
                    """
                ),
                HumanMessage(content=state["input"]),
            ]
        )
        return {"decision": decision.step}


    def route_decision(state : State): # Bu fonksiyon LLM’in kararını alır ve hangi node’a (tool’a) geçileceğini belirler.
        # Return the node name you want to visit next
        if state["decision"] == "add_document":
            return "add_document_to_dictionary_tool"
        
        elif state["decision"] == "delete_document":
            return "delete_document_from_database_tool"
        
        elif state["decision"] == "ask_document":
            return "ask_document_tool"
        
        elif state["decision"] == "list_documents":
            return "list_documents"
    # Nodes


    def add_document_to_dictionary_tool(state : State):   
            user_query = state["input"]
            date_now = datetime.now()
            extractor_llm = llm.with_structured_output(Adding_to_Document_Database)
            
            system_message = adding_system_message_function()
            human_message = HumanMessage(content=f"Not içeriği : {user_query}")
            messages = [system_message,human_message]
            try:
                output : Adding_to_Document_Database = extractor_llm.invoke(messages)
                file_name = output.file_name
                file_content = output.file_content

                print(f"Dosya adi eklendi : {file_name}\nDosya İçeriği : {file_content}")
                st.session_state.document_database[file_name] = file_content
                result_message = f"Belge Başarıyla eklendi!\n Eklenen Belgenin Adı : {file_name}\n Eklenen Belgenin İçeriği : {file_content}"
                return {"output" : result_message}
            except Exception as e:
                print("Hata Oluştu : ",e)
                return {"output" : f"Bir hata meydana geldi {e}"}
        

    def delete_document_from_database_tool(state: State):
        """Delete a document from the database. Given user query, extract the filename of the document to delete. If not provided, will not delete the document from the database."""
        user_query = state["input"]
        try:
            extractor_llm = llm.with_structured_output(Removing_from_Document_Database)
            system_message = removing_system_message_function()
            human_message = HumanMessage(f"Silinecek dosyanın ismi : {user_query}")
            messages = [system_message,human_message]
            output : Removing_from_Document_Database = extractor_llm.invoke(messages)
            filename_to_remove = output.name_of_file_that_will_be_removed
            print(f"Silinecek Dosya Adı : {filename_to_remove}")

            if filename_to_remove not in st.session_state.document_database:
                print(f"File name cant be found {filename_to_remove}")
                return {"output": f"Document {filename_to_remove} not found in database"}
            else:
                st.session_state.document_database.pop(filename_to_remove)
                print(f"Filename was removed {filename_to_remove}")
                return {"output": f"Document {filename_to_remove} was successfully deleted from database"}
            
        except Exception as e:
            print("Hata Oluştu : ",e)
            return {"output" : f"Bir hata meydana geldi {e}"}

    def ask_document_tool(state: State):
        
        """Ask a question about a document. Given user query, extract the filename and question for the document. If not provided, will not ask the question about the document."""
        user_query = state["input"]
        
        system_message = SystemMessage(content=f""" If the user requests information about a document, respond using this database: {st.session_state.document_database}

If you can't find the answer you're looking for in the database, you can use the "I couldn't find the answer to your question in the database" option.

""")
        



        human_message = HumanMessage(content=user_query)

        prompt = [system_message,human_message]

        output = llm.invoke(prompt)
        content = output.content
        print("Databaseden gelen içerik : ",content)
        return {"output" : f"{content}"}

    def list_documents(state : State):
        
        user_query = state["input"]

        

        if len(st.session_state.document_database) > 0:
            message = prompt = f"""
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
        
        """
            description = f"Veritabanında belge bulunmuştur 🥳🥳🥳\nDatabase infos from list_documents {st.session_state.document_database} \n\n Length of Database {len(st.session_state.document_database)}"
            print(description)

            system_message = SystemMessage(content=message)
            human_message = HumanMessage(content=user_query)
            prompt = [system_message,human_message]
            output = llm.invoke(prompt)
            content = output.content
            
            return {"output" : content}
            
        else:
            return {"output" : "Any Documents can not be found in the Database"}    
        



    st.title("CHATBOT")



        
        
        

    # Mesajları Yazdirir 
    for message in st.session_state.messages:
        if isinstance(message,HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message,AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)


    


    # Build workflow
    router_builder = StateGraph(State)

    

    # Add nodes
    router_builder.add_node("add_document_to_dictionary_tool", add_document_to_dictionary_tool)
    router_builder.add_node("delete_document_from_database_tool", delete_document_from_database_tool)
    router_builder.add_node("ask_document_tool", ask_document_tool)
    router_builder.add_node("llm_call_router", llm_call_router)
    router_builder.add_node("list_documents",list_documents)
    # Add edges to connect nodes
    router_builder.add_edge(START, "llm_call_router")
    router_builder.add_conditional_edges(
        "llm_call_router",
        route_decision,
        {  # Name returned by route_decision : Name of next node to visit
            "add_document_to_dictionary_tool": "add_document_to_dictionary_tool",
            "delete_document_from_database_tool": "delete_document_from_database_tool",
            "ask_document_tool": "ask_document_tool",
            "list_documents" : "list_documents"
        },
    )
    last_data = {"add_document_to_dictionary_tool" : "add_document_to_dictionary_tool","delete_document_from_database_tool" : "delete_document_from_database_tool",END : END}

    router_builder.add_edge("add_document_to_dictionary_tool", END)
    router_builder.add_edge("delete_document_from_database_tool", END)
    router_builder.add_edge("ask_document_tool", END)
    router_builder.add_edge("list_documents",END)




    # Compile workflow
    memory = InMemorySaver()
    router_workflow = router_builder.compile(checkpointer=memory)
    sayaç = 0
    config = {"configurable": {"thread_id": "1"}}

    prompt = st.chat_input("How are you")

    if prompt:
        
        with st.chat_message("human"):
            st.markdown(prompt)
            st.session_state.messages.append(HumanMessage(content=prompt))
            print("What is What User asks us : ",prompt)
        
        response = router_workflow.invoke({"input" : prompt},config=config)

        content = response["output"]

        with st.chat_message("assistant"):
            st.markdown(content)
            st.session_state.messages.append(AIMessage(content=content))
            print("What is Answer of AI : ",content)

            # py -m streamlit run New_Full_Project.py

except Exception as Hata:
    print("Hata : ",Hata)
