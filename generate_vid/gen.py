from utils.retrieve import vector_store


def generate_video_internal(text: str):
    """
    Get a video from a text
    :param text: text
    :return: video file
    """
    # Get the most similar video
    results_with_scores = vector_store.similarity_search_with_score(text)
    if len(results_with_scores) == 0:
        raise ValueError("No video found")
    doc, score = results_with_scores[0]
    print(f"Content: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")
    return doc.metadata["video_file"]
