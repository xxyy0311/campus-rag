def split_document(
    document: dict,
    chunk_size: int = 220,
    chunk_overlap: int = 40,
) -> list[dict]:
    """把文档切分成多个带重叠的文本块。"""
    if chunk_size <= 0:
        raise ValueError("chunk_size必须大于0。")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap不能小于0。")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap必须小于chunk_size。")

    text = document["content"]
    source = document["source"]

    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        chunk_content = text[start:end].strip()

        if chunk_content:
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "source": source,
                    "content": chunk_content,
                    "start": start,
                    "end": end,
                }
            )

        if end == len(text):
            break

        start = end - chunk_overlap
        chunk_id += 1

    return chunks