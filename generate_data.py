from openai import OpenAI
from dotenv import load_dotenv


template = """{
    "buglist": [
    {
        "title": "新手机号段注册提示手机号码格式不正确",
        "severity"："高"
        "module": "登录模块"
        "description": "用194开始的手机号码注册用户，页面提示号码不正确。",
        "solution": "这是因为很多前端开发都是从网上找来的代码做验证手机号，但是那些代码已经不适用于今天新出的手机号码。"
        "修改JS代码的正则匹配，扩大号码范围。"
    }
    ]}"""


def get_llm(module):
    client = OpenAI()
    prompt = f"""我在做一个分享bug的平台，这能让工程师精准测试，需要统计软件中常出现的bug。
    请你列出{module}常见的bug，给出解决方法，越详细越好。请用JSON格式输出，示例如下：{template}
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个软件专家"},
            {"role": "user", "content": prompt},
        ],
        response_format={
            'type': 'json_object'
        },
        stream=False
    )
    data = response.choices[0].message.content
    return data


if __name__ == "__main__":
    bugs = get_llm("商品功能")
    print(type(bugs), bugs)
