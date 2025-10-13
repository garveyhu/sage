from sage.components.llms.llm_factory import LLMFactory
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition


def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


llm = LLMFactory.create_llm()
llm_with_tools = llm.bind_tools([multiply])


# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)  ## 工具调用节点
builder.add_node("tools", ToolNode([multiply]))  # 工具节点
builder.add_edge(START, "tool_calling_llm")  # 开始节点 --> 工具调用节点
builder.add_conditional_edges(  # 工具调用节点 -条件边-> 工具节点
    "tool_calling_llm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", END)
graph = builder.compile()

with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())

## 运行图
from langchain_core.messages import HumanMessage

messages = [HumanMessage(content="Hello world.")]
messages = graph.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()

## 提出一个乘法相关的题目
messages = [HumanMessage(content="What is 2 multiply by 3?.")]
messages = graph.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()
