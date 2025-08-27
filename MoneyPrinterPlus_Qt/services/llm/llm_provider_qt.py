from services.llm.tongyi_service_qt import MyTongyiServiceQt


def get_llm_provider(llm_provider):
    if llm_provider == "Tongyi":
        return MyTongyiServiceQt()
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")