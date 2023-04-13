from flask import Flask, render_template, request
from database import initialize_database, save_news_summary, DB_FILEPATH
import requests
import os
import sqlite3
app = Flask(__name__)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
}
data_template = {
    "model": "text-davinci-003",
    "max_tokens": 1000,
}

def generate_summary(prompt):
    prompt_text = f"「{prompt}」という記事を1000トークンで収まる内容で日本語で要約してください。"
    data = {**data_template, "prompt": prompt_text}

    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    response_json = response.json()
    summary = response_json["choices"][0]["text"].strip()

    return summary

def generate_question(prompt):
    prompt_text1 = f"「{prompt}」という記事に関する簡単な質問を1つ日本語で作って下さい。1000トークンで収まる内容でお願いします。"
    data1 = {**data_template, "prompt": prompt_text1}

    response1 = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data1)
    response_json1 = response1.json()
    question = response_json1["choices"][0]["text"].strip()

    prompt_text2 = f"「{question}」を英語に直して下さい。1000トークンで収まる内容でお願いします。"
    data2 = {**data_template, "prompt": prompt_text2}

    response2 = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data2)
    response_json2 = response2.json()
    question_en = response_json2["choices"][0]["text"].strip()

    return question, question_en

@app.route('/index', methods=['GET', 'POST'])
def index():
    name = 'nanami'
    if request.method == 'POST':
        title = request.form['textbox']
        summary = generate_summary(title)
        question, question_en = generate_question(title)
        save_news_summary(title, summary, question, question_en )
        return render_template('article.html', summary=summary, question=question, question_en=question_en)
    return render_template('index.html', name=name)

@app.route('/list')
def list():
    conn = sqlite3.connect(DB_FILEPATH)
    cursor = conn.cursor()
    select_sql = """
        SELECT title, summary, question, question_en FROM news_summary
    """
    cursor.execute(select_sql)
    rows = cursor.fetchall()
    conn.close()
    return render_template('list.html', rows=rows)

if __name__ == "__main__":
    app.run()
    initialize_database()