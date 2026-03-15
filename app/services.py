from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate


def get_llm(api_key: str) -> ChatGroq:
    return ChatGroq(
        api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.2,
    )


def summarize_text(text: str, max_words: int, api_key: str) -> dict:
    llm = get_llm(api_key)

    prompt = PromptTemplate.from_template(
        "Summarize the following text in {max_words} words or less. "
        "Be concise and capture the key points.\n\nText: {text}\n\nSummary:"
    )

    chain = prompt | llm
    result = chain.invoke({"text": text, "max_words": max_words})
    summary = result.content.strip()

    return {
        "summary": summary,
        "word_count": len(summary.split()),
    }


def classify_text(text: str, labels: list[str], api_key: str) -> dict:
    llm = get_llm(api_key)

    prompt = PromptTemplate.from_template(
        "Classify the following text into exactly one of these categories: {labels}.\n"
        "Respond in this exact format:\n"
        "Label: <chosen label>\n"
        "Reason: <one sentence reason>\n\n"
        "Text: {text}"
    )

    chain = prompt | llm
    result = chain.invoke({"text": text, "labels": ", ".join(labels)})
    output = result.content.strip()

    label, reason = "", ""
    for line in output.splitlines():
        if line.startswith("Label:"):
            label = line.replace("Label:", "").strip()
        elif line.startswith("Reason:"):
            reason = line.replace("Reason:", "").strip()

    return {"label": label, "reason": reason}