from sage.components.llms.llm_factory import LLMFactory


# Tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


# Tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b


# Tool
def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b


# Tools
tools = [add, multiply, divide]
# LLM
llm = LLMFactory.create_llm()
llm_with_tools = llm.bind_tools(tools)

from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

# Prompt - system
sys_msg = SystemMessage(
    content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
)


# Node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode

# Graph
builder = StateGraph(MessagesState)
# Nodes
builder.add_node("assistant", assistant)  ## 大模型助手节点，决定是否需要调用工具
builder.add_node("tools", ToolNode(tools))  ## 工具节点，运行函数工具
# Edges
builder.add_edge(START, "assistant")  # 普通边
builder.add_conditional_edges(  # 条件边
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")  # 这里加了一条返回的边，形成闭环。
react_graph = builder.compile()

## Action
messages = [
    HumanMessage(
        content="Add 3 and 4. Multiply the output by 2. Divide the output by 5"
    )
]
messages = react_graph.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()
