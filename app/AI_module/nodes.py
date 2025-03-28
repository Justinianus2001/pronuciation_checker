from langchain_core.messages import HumanMessage, SystemMessage
from .llm import structured_output_llm
from .state import State

def analyze_pronunciation_errors_node(state: State) -> State:
    reference_text = state['reference_text']
    system_message = """
You are an English pronunciation assistant. Based on text passage (reference_text)
and an audio recording of them reading the text (user_input), analyze the audio based on the text.
Identify any words in the reference_text that are mispronounced or omitted.
For example, if the user provides the sentence 'I have a dog,' determine whether there are pronunciation errors for the words 'I,' 'have,' 'a,' or 'dog' based on the given audio.\n
Output: The required output is a JSON containing error details in the following format:
{
  "errors": [
    {
      "word": "",                  // The mispronounced or omitted word.
      "position": 0,               // The position (index) of the word in the sentence, starting from 0.
      "error_type": "",            // Type of error (e.g., phát âm sai, bị bỏ qua) only in Vietnamese.
      "correct_pronunciation": "", // The correct pronunciation of the word.
      "your_pronunciation": "",    // How the word was pronounced by the user.
      "explanation": ""            // Explanation of the error only in Vietnamese.
    }
  ]
}
Note: Words that are correctly pronounced do not need to be listed in the output.
Begin: \n
""" + f"reference_text: {reference_text}"
    message = [
        SystemMessage(content=system_message),
        HumanMessage(
        content=[
            {"type": "text", "text": f"reference_text: {reference_text}"},
            {"type": "media", "mime_type": "audio/mp3", "data": state["base64_audio"]},
        ])
    ]

    response = structured_output_llm.invoke(message)
    return {"errors": response["errors"]}


def evaluate_speech_metrics_node(state: State) -> State:
    reference_text = state['reference_text']
    system_message = """
You are an English pronunciation assistant. Based on text passage (reference_text)
and an audio recording of them reading the text (user_input), evaluate the user's speaking performance
using the IELTS speaking band descriptors. Provide a band score (1–9) for each of the following criteria:
- Fluency and Coherence
- Lexical Resource
- Grammatical Range and Accuracy
- Pronunciation
Output: The required output is a JSON containing scores and feedback for each criterion in the following format:
{
  "fluency_and_coherence": {
    "score": ,                // Band score (1–9)
    "feedback": ""            // Detailed feedback in Vietnamese
  },
  "lexical_resource": {
    "score": ,                // Band score (1–9)
    "feedback": ""            // Detailed feedback in Vietnamese
  },
  "grammatical_range_and_accuracy": {
    "score": ,                // Band score (1–9)
    "feedback": ""            // Detailed feedback in Vietnamese
  },
  "pronunciation": {
    "score": ,                // Band score (1–9)
    "feedback": ""            // Detailed feedback in Vietnamese
  }
}
Begin:
""" + f"reference_text: {reference_text}"
    message = [
        SystemMessage(content=system_message),
        HumanMessage(
        content=[
            {"type": "text", "text": f"reference_text: {reference_text}"},
            {"type": "media", "mime_type": "audio/mp3", "data": state["base64_audio"]},
        ])
    ]
    response = structured_output_llm.invoke(message)
    state["measures"] = response
    return {"measures": response}


def render_highlighted_html_node(state: State) -> State:
    sentence = state["reference_text"]
    errors = state["errors"]
    sentence_list = sentence.split()
    for error in errors:
        sentence_list[error["position"]] = f"<span style='color:red'>{sentence_list[error['position']]}</span>"
    result = " ".join(sentence_list)
    state["html_output"] = f"<span style='color: green'>{result}</span>"
    return state


def generate_speaking_report_node(test_results):
    system_message = """
Bạn là chuyên gia giáo dục tiếng Anh, chuyên đánh giá kỹ năng nói và phát âm. Nhiệm vụ của bạn là phân tích dữ liệu bài kiểm tra nói của người dùng và tạo báo cáo ngắn gọn, sử dụng ít từ.

Báo cáo cần bao gồm:
- Nhận xét tổng quan: Đánh giá chung mức độ nói tiếng Anh của người dùng (không cần theo dõi tiến triển qua các bài kiểm tra).
- Lỗi phổ biến: Liệt kê các lỗi thường gặp (ví dụ: thiếu âm cuối, sai nguyên âm,...).
- Giải pháp cải thiện: Đề xuất các cách khắc phục ngắn gọn.

Yêu cầu: Đầu ra trình bày dưới dạng JSON.
Ví dụ:
{
  "overall_assessment": "Khả năng nói tiếng Anh ở mức trung bình khá. Cần cải thiện phát âm một số âm cơ bản và ngữ điệu.",
  "common_errors": [
    "Thiếu âm cuối (ví dụ: 'went' phát âm thành 'wen')",
    "Sai nguyên âm (ví dụ: 'beach' phát âm sai)",
    "Ngữ điệu đơn điệu"
  ],
  "improvement_suggestions": [
    "Luyện tập phát âm các âm cuối thường bị bỏ qua.",
    "Học và luyện tập phát âm các nguyên âm cơ bản.",
    "Luyện tập ngữ điệu bằng cách nghe và bắt chước người bản xứ.",
    "Tập trung vào việc liên kết các từ để tạo sự trôi chảy."
  ]
}
"""
    message = [
        SystemMessage(content=system_message),
        HumanMessage(content=[{"type": "text", "text": f"{test_results}"}])
    ]
    response = structured_output_llm.invoke(message)
    return response