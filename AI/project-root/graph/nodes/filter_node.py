from llm.gemini_suggester import extract_filters_from_prompt

def filter_node(state: dict):
    user_input = state["input"]
    filters = extract_filters_from_prompt(user_input)
    return {"filters": filters}
