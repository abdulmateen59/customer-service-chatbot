import sys
import uuid

import google.auth
import vertexai
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages import ToolMessage
from langchain_google_vertexai import ChatVertexAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.func import entrypoint
from langgraph.func import task
from langgraph.graph.message import add_messages

from system_prompt import system_prompt
from tools.get_info_from_knowledge import get_info_from_knowledge
from tools.get_user_latest_orders import get_user_latest_orders
from tools.get_user_order_return_details import get_user_order_return_details
from tools.get_user_order_shipment_details import get_user_order_shipment_details


credentials, project = google.auth.default()
vertexai.init(project=project,
              location="europe-west1",
              credentials=credentials)
model = ChatVertexAI(model="gemini-2.0-flash-001",
                     temperature=0.2)
tools = [get_user_latest_orders,
         get_user_order_shipment_details,
         get_user_order_return_details,
         get_info_from_knowledge]
tools_by_name = {tool.name: tool for tool in tools}
llm_wit_tool = model.bind_tools(tools)


@task
def call_model(messages):
    response = llm_wit_tool.invoke([SystemMessage(content=system_prompt)] + messages)
    return response


@task
def call_tool(tool_call):
    tool = tools_by_name[tool_call["name"]]
    observation = tool.invoke(tool_call["args"])
    return ToolMessage(content=observation,
                       tool_call_id=tool_call["id"])


@entrypoint(checkpointer=MemorySaver())
def agent_workflow(messages, previous, config):
    # print(messages)
    # print("*"*90)
    if previous is not None:
        messages = add_messages(previous, messages)

    llm_response = call_model(messages).result()
    while True:
        if not llm_response.tool_calls:
            break

        tool_results = [
            call_tool(tool_call).result() for tool_call in llm_response.tool_calls
        ]

        messages = add_messages(messages, [llm_response, *tool_results])
        llm_response = call_model(messages).result()

    messages = add_messages(messages, llm_response)

    return messages


def run():
    thread_id = str(uuid.uuid4())
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    while True:
        print("*" * 100)
        user_message = HumanMessage(content=f"{input("User: ")}")
        print("*" * 100)
        user_message.pretty_print()
        if user_message.content == "stop":
            break
        for step in agent_workflow.stream([user_message], config, stream_mode="updates"):
            for task_name, message in step.items():
                if task_name == "agent_workflow":
                    continue
                print(f"\n{task_name}:")
                message.pretty_print()


if __name__ == "__main__":
    if str(sys.argv[1]).lower() == "--interactive":
        run()
