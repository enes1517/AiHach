# explanation_node.py

from typing import Dict
from llm.gemini_suggester import explain_recommendation

def explanation_node(state: Dict) -> Dict:
    try:
        print("🧠 explanation_node çalışıyor...")
        result = state.get("result", [])
        user_input = state.get("input", "")

        explanations = explain_recommendation(result, user_input)

        return {
            **state,
            "explanation": explanations
        }
    except Exception as e:
        print(f"❌ Explanation node hatası: {e}")
        return {
            **state,
            "explanation": f"Explanation hatası: {str(e)}"
        }
