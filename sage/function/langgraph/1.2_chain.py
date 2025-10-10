from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage

from sage.components.llms.llm_factory import LLMFactory

messages = [
    AIMessage(content="So you said you were researching ocean mammals?", name="Model"),
]
messages.append(HumanMessage(content="Yes, thats's right.", name="Lance"))
messages.append(
    AIMessage(content="Great, what would you like to learn about.", name="Model")
)
messages.append(
    HumanMessage(
        content=f"I want to learn about the best place to see Orcas in the US.",
        name="Lance",
    )
)

for m in messages:
    m.pretty_print()

llm = LLMFactory.create_llm()


def multipy(a: int, b: int) -> int:
    return a * b


llm_with_tools = llm.bind_tools([multipy])

tool_call = llm_with_tools.invoke(
    [HumanMessage(content="what is 3 multiplied by 3", name="Lance")]
)

print(tool_call.additional_kwargs["tool_calls"])

from typing_extensions import TypedDict
from typing import Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END


class MessageState(MessagesState):
    pass


def tool_calling_llm(state: MessagesState):
    return {"messages": llm_with_tools.invoke(state["messages"])}


builder = StateGraph(MessagesState)

builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)
graph = builder.compile()

with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())

messages = graph.invoke(
    {"messages": HumanMessage(content="Multiply 2 and 3", name="Lance")}
)

for m in messages["messages"]:
    m.pretty_print()
