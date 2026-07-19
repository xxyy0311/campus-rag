from pathlib import Path


def read_text_file(file_path: str) -> str:
    """读取UTF-8文本文件。"""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")

    text = path.read_text(encoding="utf-8")
    return text