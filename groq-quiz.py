import os
from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='./', static_url_path='')
client = Groq()

@app.route('/quiz')
def groq():
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "你是开放原始码项目的贡献者 or 开发者 or 支持开放原始码的企业，会产生 JSON 格式的回答，用简体中文回答，输出只要给 json ，不要其他的东西"
            },
            {
                "role": "user",
                "content": "请问我一个有关开放原始码 License 的问题，询问 License 的特性的选择题，请告知使用了哪一个 License，并且答案应该只有一个是正确的，或者可提供(以上皆是、以上皆不是)等选项，在json 中给定 { content: 问题, answer: 'A/B/C/D', quiz:{'A': '描述', 'B'...}} 最多4 个选项(不可重复)",
            }
        ],
        model="llama3-8b-8192",
    )
    print(chat_completion)
    return jsonify(chat_completion.choices[0].message.content)

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000), host='0.0.0.0')
