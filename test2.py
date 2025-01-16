import warnings
from langchain import hub
from langchain.agents import create_react_agent
from Tools import *
from langchain_ollama import ChatOllama
warnings.filterwarnings("ignore", category=UserWarning, module="langsmith")

model = ChatOllama(model="mistral:latest", temperature=0)
prompt = hub.pull("hwchase17/react-chat")
tools = [solve_quadratic] # i have only 1 tool here - solve_quadratic

llm = create_react_agent(model, tools, prompt)


input_text = "solve pls this quadratic equation: 2x^(2)+13x+6=0"
inputs = {
    "input": input_text,
    "chat_history": [],
    "messages": [],
    "intermediate_steps": [],
}

print(llm.invoke(inputs))
