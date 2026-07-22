from pathlib import Path


def load_text_document(file_path: str) -> dict:
    """读取一个UTF-8编码的TXT文件。"""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")

    if path.suffix.lower() != ".txt":
        raise ValueError("当前版本只支持TXT文件。")

    text = path.read_text(encoding="utf-8").strip()

    if not text:
        raise ValueError(f"文件内容为空：{file_path}")

    return {
        "source": path.name,
        "content": text,
    }