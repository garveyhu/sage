from typing_extensions import TypedDict


class State(TypedDict):
    graph_state: str


state: State = {"graph_state": "active"}


def node_1(state: State) -> State:
    print("---Node 1---")
    print(f"state[graph_state]: {state['graph_state']}")
    return {"graph_state": state["graph_state"] + "I am"}


def node_2(state: State) -> State:
    print("---Node 2---")
    print(f"state[graph_state]: {state['graph_state']}")
    return {"graph_state": state["graph_state"] + " happy!"}


def node_3(state: State) -> State:
    print("---Node 3---")
    print(f"state[graph_state]: {state['graph_state']}")
    return {"graph_state": state["graph_state"] + " sad!)"}


import random
from typing import Literal


def decide_mood(state: State) -> Literal["node2", "node3"]:
    return random.choice(["node2", "node3"])


from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("node1", node_1)
builder.add_node("node2", node_2)
builder.add_node("node3", node_3)

builder.add_edge(START, "node1")
builder.add_conditional_edges("node1", decide_mood)
builder.add_edge("node2", END)
builder.add_edge("node3", END)

graph = builder.compile()

# with open("graph.png", "wb") as f:
#     f.write(graph.get_graph().draw_mermaid_png())

print(graph.invoke({"graph_state": "Hi, this is Lance. "}))
