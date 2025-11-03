from langgraph.graph import StateGraph, START, END
from state import CustomerFeedbackAnalysisState
from nodes import analyse_sentiment, router, analyze_issue


def agent():
    builder = StateGraph(CustomerFeedbackAnalysisState)
    builder.add_node("analyze", analyse_sentiment)
    builder.add_node("analyze_issue", analyze_issue)

    builder.add_edge(START, "analyze")
    builder.add_conditional_edges(
        "analyze",
        router,
        {
            "analyze_issue": "analyze_issue",
            "END": END,
        },
    )

    app = builder.compile()
    png_graph = app.get_graph().draw_mermaid_png()
    with open("agent.png", "wb") as file:
        file.write(png_graph)
    return app
