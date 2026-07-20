import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)


BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-v4-flash"
CHAT_LOG_DIR = Path("chat_logs")


def create_client() -> OpenAI:
    """创建并返回DeepSeek API客户端。"""
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise RuntimeError(
            "没有读取到DEEPSEEK_API_KEY，请检查.env文件。"
        )

    return OpenAI(
        api_key=api_key,
        base_url=BASE_URL,
    )


def ask_model(
    client: OpenAI,
    messages: list[dict[str, str]],
) -> str:
    """把聊天消息发送给模型，并返回回答文本。"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        stream=False,
        extra_body={
            "thinking": {
                "type": "disabled",
            }
        },
    )

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("模型没有返回文本内容。")

    return answer


def create_log_path() -> Path:
    """为本次聊天创建一个JSON日志文件路径。"""
    CHAT_LOG_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return CHAT_LOG_DIR / f"chat_{timestamp}.json"


def save_messages(
    log_path: Path,
    messages: list[dict[str, str]],
) -> None:
    """把当前聊天记录保存到JSON文件。"""
    data = {
        "model": MODEL_NAME,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "messages": messages,
    }

    json_text = json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
    )

    log_path.write_text(
        json_text,
        encoding="utf-8",
    )


def print_api_error(error: Exception) -> None:
    """根据错误类型显示容易理解的提示。"""
    if isinstance(error, AuthenticationError):
        print(
            "\nAPI Key认证失败，请检查.env中的密钥是否正确。"
        )
        return

    if isinstance(error, RateLimitError):
        print(
            "\n请求过于频繁，请稍等一会儿再试。"
        )
        return

    if isinstance(error, APIConnectionError):
        print(
            "\n无法连接到API服务器，请检查网络后重试。"
        )
        return

    if isinstance(error, APIStatusError):
        if error.status_code == 402:
            print(
                "\nAPI账户余额不足，请检查开放平台余额。"
            )
        else:
            print(
                f"\nAPI请求失败，状态码：{error.status_code}"
            )
        return

    print(f"\n发生未知错误：{error}")


def main() -> None:
    try:
        client = create_client()
    except RuntimeError as error:
        print(error)
        return

    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "你是一名耐心、准确的计算机课程助教。"
                "回答时优先使用清晰的中文，并适当举例。"
            ),
        }
    ]

    log_path = create_log_path()

    print("Campus RAG AI聊天程序")
    print("输入 exit、quit 或 退出，可以结束聊天。")

    while True:
        user_input = input("\n你：").strip()

        if not user_input:
            print("请输入具体问题。")
            continue

        if user_input.lower() in {"exit", "quit", "退出"}:
            save_messages(log_path, messages)
            print(f"\n聊天记录已经保存到：{log_path}")
            print("聊天结束。")
            break

        request_messages = messages + [
            {
                "role": "user",
                "content": user_input,
            }
        ]

        try:
            answer = ask_model(
                client=client,
                messages=request_messages,
            )
        except (
            AuthenticationError,
            RateLimitError,
            APIConnectionError,
            APIStatusError,
            RuntimeError,
        ) as error:
            print_api_error(error)
            continue
        except Exception as error:
            print_api_error(error)
            continue

        messages = request_messages
        messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        save_messages(log_path, messages)

        print(f"\nAI：{answer}")


if __name__ == "__main__":
    main()