from utils.file_utils import read_text_file


def split_text(text: str, chunk_size: int = 500) -> list[str]:
    """把长文本按照固定字符数切分成多个文本块。"""
    if chunk_size <= 0:
        raise ValueError("chunk_size必须大于0")

    chunks = []

    for start in range(0, len(text), chunk_size):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)

    return chunks


def search_chunks(chunks: list[str], keyword: str) -> list[str]:
    """找出包含指定关键词的文本块。"""
    keyword = keyword.strip()

    if not keyword:
        return []

    results = []

    for chunk in chunks:
        if keyword.lower() in chunk.lower():
            results.append(chunk)

    return results


def main() -> None:
    try:
        text = read_text_file("data/network.txt")
        chunks = split_text(text, chunk_size=200)

        print(f"资料读取成功，共生成{len(chunks)}个文本块。")

        keyword = input("请输入搜索关键词：").strip()
        results = search_chunks(chunks, keyword)

        if not results:
            print("没有找到相关内容。")
            return

        print(f"\n共找到{len(results)}个相关文本块。")

        for index, result in enumerate(results, start=1):
            print(f"\n========== 结果{index} ==========")
            print(result)

    except FileNotFoundError as error:
        print(error)
    except UnicodeDecodeError:
        print("文件编码错误，请将文件保存为UTF-8编码。")
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()