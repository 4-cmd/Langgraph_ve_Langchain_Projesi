from typing_extensions import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from os import getenv
from langchain_mistralai.chat_models import ChatMistralAI
from BaseModel import Adding_to_Document_Database,Removing_from_Document_Database,Route
from Adding_system_message import adding_system_message_function
from all_system_messages import removing_system_message_function,llm_call_router_system_message_function,ask_document_tool_system_message_function,list_documents_system_message_function
from streamlit_işlemleri import adding_the_state_message,printing_the_message
from graph_çizdirme import graph_cizdirme

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





router = llm.with_structured_output(Route)

printing_the_message()

try:

    def llm_call_router(state: State):

        """Route the user input to the appropriate node"""
        # Run the augmented LLM with structured output to serve as routing logic
        system_message = llm_call_router_system_message_function()
        human_message = HumanMessage(content=state["input"])
        messages = [system_message,human_message]
        decision = router.invoke(messages)
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
        
        system_message = ask_document_tool_system_message_function()

        human_message = HumanMessage(content=user_query)

        prompt = [system_message,human_message]

        output = llm.invoke(prompt)
        content = output.content
        print("Databaseden gelen içerik : ",content)
        return {"output" : f"{content}"}

    def list_documents(state : State):
        
        user_query = state["input"]

        

        if len(st.session_state.document_database) > 0:
            system_message = list_documents_system_message_function()
            description = f"Veritabanında belge bulunmuştur 🥳🥳🥳\nDatabase infos from list_documents {st.session_state.document_database} \n\n Length of Database {len(st.session_state.document_database)}"
            print(description)

            system_message = SystemMessage(content=system_message)
            human_message = HumanMessage(content=user_query)
            messages = [system_message,human_message]

            output = llm.invoke(messages)
            content = output.content
            return {"output" : content}
            
        else:
            return {"output" : "Any Documents can not be found in the Database"}    
        



        
        
        



    


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

    koşul_kararı_sözlük =  {  # Name returned by route_decision : Name of next node to visit
            "add_document_to_dictionary_tool": "add_document_to_dictionary_tool",
            "delete_document_from_database_tool": "delete_document_from_database_tool",
            "ask_document_tool": "ask_document_tool",
            "list_documents" : "list_documents"
        }

    router_builder.add_conditional_edges(
        "llm_call_router",
        route_decision,
       koşul_kararı_sözlük
    )

    router_builder.add_edge("add_document_to_dictionary_tool", END)
    router_builder.add_edge("delete_document_from_database_tool", END)
    router_builder.add_edge("ask_document_tool", END)
    router_builder.add_edge("list_documents",END)




    # Compile workflow
    memory = InMemorySaver()
    router_workflow = router_builder.compile(checkpointer=memory)
    png_data = router_workflow.get_graph().draw_mermaid_png()
    graph_cizdirme(png_data)
    sayaç = 0
    config = {"configurable": {"thread_id": "1"}}

    prompt = st.chat_input("How are you")

    if prompt:
        # beginner
        adding_the_state_message(prompt)
        
        response = router_workflow.invoke({"input" : prompt},config=config)

        content = response["output"]

        adding_the_state_message(icerik=content,is_human=False)

          

except Exception as Hata:
    print("Hata : ",Hata)

  # py -m streamlit run New_Full_Project.py