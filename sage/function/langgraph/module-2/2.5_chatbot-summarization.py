# 如何使用 LLM 生成对话的实时总结 summary
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage

from sage.complex.config.inventory import user_id
from sage.components.inventory import llm

from langgraph.graph import MessagesState


# State
class State(MessagesState):
    summary: str


# LLM
llm = llm()


# Node
def call_model(state: State):

    # Get summary if it exists
    summary = state.get("summary", "")

    # If there is summary, then we add it
    if summary:

        # Add summary to system message
        system_message = f"Summary of conversation earlier: {summary}"

        # Append summary to any newer messages
        messages = [SystemMessage(content=system_message)] + state["messages"]

    else:
        messages = state["messages"]

    response = llm.invoke(messages)
    return {"messages": response}


# Node
def summarize_conversation(state: State):

    # First, we get any existing summary
    summary = state.get("summary", "")

    # Create our summarization prompt
    if summary:

        # A summary already exists
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )

    else:
        summary_message = "Create a summary of the conversation above:"

    # Add prompt to our history
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = llm.invoke(messages)

    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}


# Determine whether to end or summarize the conversation
from langgraph.graph import END


# Node
def should_continue(state: State):
    """Return the next node to execute."""

    messages = state["messages"]

    # If there are more than six messages, then we summarize the conversation
    if len(messages) > 6:
        return "summarize_conversation"

    # Otherwise we can just end
    return END


from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START

# Graph
workflow = StateGraph(State)
# Nodes
workflow.add_node("conversation", call_model)
workflow.add_node(summarize_conversation)

# Edges
# Set the entrypoint as conversation
workflow.add_edge(START, "conversation")
workflow.add_conditional_edges("conversation", should_continue)
workflow.add_edge("summarize_conversation", END)

# Memory
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
# with open("graph.png", "wb") as f:
#     f.write(graph.get_graph().draw_mermaid_png())
# Context
config = {"configurable": {"thread_id": user_id()}}

# Action1
input_message = HumanMessage(content="hi! I'm Lance")
output = graph.invoke({"messages": [input_message]}, config)
for m in output["messages"][-1:]:
    m.pretty_print()
# Action2
input_message = HumanMessage(content="what's my name?")
output = graph.invoke({"messages": [input_message]}, config)
for m in output["messages"][-1:]:
    m.pretty_print()
# Action3
input_message = HumanMessage(content="i like the 49ers!")
output = graph.invoke({"messages": [input_message]}, config)
for m in output["messages"][-1:]:
    m.pretty_print()

# Event
print(graph.get_state(config).values.get("summary", ""))

# Action4
input_message = HumanMessage(
    content="i like Nick Bosa, isn't he the highest paid defensive player?"
)
output = graph.invoke({"messages": [input_message]}, config)
for m in output["messages"][-1:]:
    m.pretty_print()

# Event
print(graph.get_state(config).values.get("summary", ""))
