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
                "content": "你是開放原始碼專案的貢獻者，會產生 JSON 格式的回答，用簡體中文回答，輸出只要給 json ，不要其他的東西"
            },
            {
                "role": "user",
                "content": "請給一段關於開源專案使用規則的問題，在 json 中給定 { content: 問題, answer: 'A/B/C/D', quiz:{'A':'描述', 'B'...}} 最多 4 個選項 (不可重複)",
            }
        ],
        model="llama3-8b-8192",
    )
    return jsonify(chat_completion.choices[0].message.content)

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 8080), host='0.0.0.0')
