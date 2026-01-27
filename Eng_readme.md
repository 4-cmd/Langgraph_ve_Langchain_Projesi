**First Steps to Get Your Project Working**
* A new file named **Information.env** must be created.
* A Mistral API key must be obtained from **https://admin.mistral.ai/organization**.
* Inside the **Information.env** file:
* MISTRAL_API_KEY = Put ​​the API key you obtained from Mistral here.
* Since the API key required for LLM to work is provided in this process, LLM can now run in our project.

- After the API key process, there is a second step you need to take:
- You must create a new virtual environment named **python -m venv venv** on your computer.
- Then you must activate the virtual environment by typing **venv\Scripts\activate**.
- Then, in your current IDE (VS Code or PyCharm), you must select the **venv** file we just created in our project by typing **Select Interpreter**.
- Then, in the terminal screen, you must install the necessary packages for our project by typing **pip install -r requirements.txt**. You need to install it.

Finally, open the terminal screen and run **streamlit run New_Full_Project.py** and you can now easily use our project without any additional steps.

📄 Smart Legal & Document Management Assistant
This project was built using LangGraph and Langchain.

🚀 Featured Features
* Can perform operations with high accuracy using the Mistral AI model (mistral-large-latest) with 41 billion active parameters and a total of 675 billion parameters.
* User-friendly chat interface developed with Streamlit.

🛠️ Technologies Used

* Language Model: Mistral AI (Large)

* Frameworks: LangChain, Langgraph

* Interface: Streamlit

* Data Validation: Pydantic (Structured Output)

🔧 How Does This Application Work?
* The user first asks a question, and the LLM analyzes the question, understands the user's intent, and acts accordingly (addition - deletion - query - listing).

How is Addition Done? * The user sends a query, for example (Note: Winter will be colder these days compared to previous years).
* If the user does not specify a title, the LLM assigns a date; if a title is specified, it saves it as the title of the note and adds it to the dictionary.

How is Deletion Done? * The user writes the name of the file they want to delete, for example (I want to delete the Judo.txt file).
* The LLM extracts this file name and deletes it if it already exists as a key in the dictionary; otherwise, it does not delete it.

How is a Question Done? * The user asks a specific question, and the LLM checks the dictionary to see if there is any information related to that question.
* For example (Who saw the Blue Cat?). If the answer is in the dictionary, it responds accordingly. If the answer is not in the dictionary, it says "I couldn't find an answer."

How is Listing Done?
* If the user says "I want to see all my notes" or "bring it to me as a list," the Note Titles and Contents found in the dictionary are presented as a list.

⚠️ WARNING
* The notes added in this project are absolutely temporary and will all disappear when the program is closed.