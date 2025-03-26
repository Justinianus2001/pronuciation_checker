from langgraph.graph import StateGraph, START, END
from .nodes import (
    analyze_pronunciation_errors_node,
    evaluate_speech_metrics_node,
    generate_speaking_report_node,
    render_highlighted_html_node,
)
from .state import State

# Workflow 1: Pronunciation Error Workflow
pronunciation_error_workflow = StateGraph(State)

pronunciation_error_workflow.add_node("analyze_pronunciation_errors_node", analyze_pronunciation_errors_node)
pronunciation_error_workflow.add_node("render_highlighted_html_node", render_highlighted_html_node)

pronunciation_error_workflow.add_edge(START, "analyze_pronunciation_errors_node")
pronunciation_error_workflow.add_edge("analyze_pronunciation_errors_node", "render_highlighted_html_node")
pronunciation_error_workflow.add_edge("render_highlighted_html_node", END)

pronunciation_error_workflow = pronunciation_error_workflow.compile()

# Workflow 2: Speech Metrics Workflow
speech_metrics_workflow = StateGraph(State)

speech_metrics_workflow.add_node("evaluate_speech_metrics_node", evaluate_speech_metrics_node)

speech_metrics_workflow.add_edge(START, "evaluate_speech_metrics_node")
speech_metrics_workflow.add_edge("evaluate_speech_metrics_node", END)

speech_metrics_workflow = speech_metrics_workflow.compile()


# Self-define Workflow
class SummaryWorkflow:

    def invoke(self, test_results: str):
        return generate_speaking_report_node(test_results)

summary_workflow = SummaryWorkflow()
