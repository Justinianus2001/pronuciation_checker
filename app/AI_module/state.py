from typing import TypedDict

class State(TypedDict):
    reference_text: str
    base64_audio: str
    errors: list
    measures: list
    html_output: str