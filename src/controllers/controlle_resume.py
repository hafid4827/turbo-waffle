from gensim.summarization import summarize


def template_resume(text: str):
    """
    Esto es comentario
    """
    summary = summarize(text)
    result_filter = {
        "lenght_letter": len(summary),
        "lenght_words": len(summary.split()),
        "text": summary
    }
    print(result_filter)
    return result_filter
