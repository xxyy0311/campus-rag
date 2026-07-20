import os

from dotenv import load_dotenv
from openai import OpenAI


# 读取项目根目录下的.env文件
load_dotenv()

# 从环境变量中获取API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise RuntimeError(
        "没有读取到DEEPSEEK_API_KEY，请检查.env文件。"
    )

# 创建API客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)

# 向模型发送一次请求
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {
            "role": "system",
            "content": "你是一名耐心的计算机课程助教。",
        },
        {
            "role": "user",
            "content": "请用三句话解释什么是RAG。",
        },
    ],
    stream=False,
    extra_body={
        "thinking": {
            "type": "disabled",
        }
    },
)

# 取出并输出模型回答
answer = response.choices[0].message.content
print(answer)