from sentence_transformers import SentenceTransformer


DEFAULT_MODEL_NAME = "BAAI/bge-small-zh-v1.5"

QUERY_PREFIX = "为这个句子生成表示以用于检索相关文章："


def load_embedding_model(
    model_name: str = DEFAULT_MODEL_NAME,
) -> SentenceTransformer:
    """加载Embedding模型。"""
    print(f"正在加载Embedding模型：{model_name}")

    model = SentenceTransformer(model_name)

    print("Embedding模型加载完成。")
    return model


def embed_documents(
    model: SentenceTransformer,
    chunks: list[dict],
):
    """将所有文本块转换成向量。"""
    texts = [chunk["content"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    return embeddings


def embed_query(
    model: SentenceTransformer,
    question: str,
):
    """将用户问题转换成向量。"""
    query_text = QUERY_PREFIX + question

    embedding = model.encode(
        [query_text],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embedding