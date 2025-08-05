from langchain_core.runnables import RunnableLambda

def format_response(state):
    if state.get("memory_response"):
        return {"output": state["memory_response"]}
    
    elif state.get("explanation"):
        return {"output": state["explanation"]}
    
    elif state.get("result"):
        if isinstance(state["result"], list):
            if not state["result"]:
                return {"output": "Üzgünüm, uygun ürün bulamadım."}
            return {"output": f"{len(state['result'])} ürün bulundu."}
        else:
            return {"output": state["result"]}
    
    return {"output": "Bir sonuç oluşturulamadı."}

formatter_node = RunnableLambda(format_response)
