from flask import Flask, render_template, request
import requests
import os
app = Flask(__name__)

def generate_summary(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
    }

    prompt_text = f"「{prompt}」という記事を1000トークンで収まる内容で日本語で要約してください。"

    data = {
        "model": "text-davinci-003",
        "prompt": prompt_text,
        "max_tokens": 1000,
    }

    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    response_json = response.json()
    summary = response_json["choices"][0]["text"].strip()

    return summary

@app.route('/index', methods=['GET', 'POST'])
def index():
    name = 'nanami'
    if request.method == 'POST':
        title = request.form['textbox']
        summary = generate_summary(f"title and summarize {title}")
        return f"Summary: {summary}"
    return render_template('index.html', name=name)

@app.route('/sub')
def sub():
    return "This is Sub Page!"

if __name__ == "__main__":
    app.run()