from app.AI_module.state import State
from app.AI_module.workflow import (
    pronunciation_error_workflow,
    speech_metrics_workflow,
    summary_workflow,
)


def analyze_pronunciation(reference_text: str, base64_audio: str):
    initial_state = State(
        reference_text=reference_text,
        base64_audio=base64_audio,
        errors=[],
        measures=[],
        html_output="",
    )
    
    result = pronunciation_error_workflow.invoke(initial_state)
    return {
        'errors': result['errors'],
        'measures': result['measures'],
        'html_output': result['html_output'],
    }


def evaluate_speech_metrics(reference_text: str, base64_audio: str):
    initial_state = State(
        reference_text=reference_text,
        base64_audio=base64_audio,
        errors=[],
        measures=[],
        html_output="",
    )
    
    result = speech_metrics_workflow.invoke(initial_state)
    return {
        'measures': result['measures'],
    }


def generate_speaking_report(test_results: str):
    return summary_workflow.invoke(test_results)