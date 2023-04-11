from flask import Flask, render_template, request
from database import initialize_database, save_news_summary, DB_FILEPATH
import requests
import os
import sqlite3
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
        save_news_summary(title, summary)
        return render_template('article.html', summary=summary)
    return render_template('index.html', name=name)

@app.route('/sub')
def sub():
    return "This is Sub Page!"

@app.route('/list')
def list():
    conn = sqlite3.connect(DB_FILEPATH)
    cursor = conn.cursor()
    select_sql = """
        SELECT title, summary FROM news_summary
    """
    cursor.execute(select_sql)
    rows = cursor.fetchall()
    conn.close()
    return render_template('list.html', rows=rows)

if __name__ == "__main__":
    app.run()
    initialize_database()