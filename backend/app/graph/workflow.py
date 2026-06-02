from langgraph.graph import StateGraph

from app.graph.states import GraphState

from app.graph.nodes import (
    retrieve_node,
    answer_node
)


graph = StateGraph(
    GraphState
)

graph.add_node(
    "retrieve",
    retrieve_node
)

graph.add_node(
    "answer",
    answer_node
)

graph.add_edge(
    "retrieve",
    "answer"
)

graph.set_entry_point(
    "retrieve"
)

workflow = graph.compile()