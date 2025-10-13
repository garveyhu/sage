from sage.complex.config.inventory import user_id
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
from langgraph.prebuilt import tools_condition, ToolNode

# Graph
builder = StateGraph(MessagesState)
# Nodes
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Edges
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")  ## 从 tools 节点返回 assistant 节点，形成闭环
# Memory
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
react_graph_memory = builder.compile(checkpointer=memory)

# Context
config = {"configurable": {"thread_id": user_id()}}
# Prompt - user
messages = [HumanMessage(content="Add 3 and 4.")]
# Action 1
messages = react_graph_memory.invoke({"messages": messages}, config)
for m in messages["messages"]:
    m.pretty_print()
# Action 2
messages = [HumanMessage(content="Multiply that by 2.")]
messages = react_graph_memory.invoke({"messages": messages}, config)
for m in messages["messages"]:
    m.pretty_print()
