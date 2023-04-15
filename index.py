from flask import Flask, render_template, request, redirect, url_for
from database import initialize_database, save_news_summary, DB_FILEPATH
from prompt_texts import GET_SUMARRY, GET_QUESTION, GET_QUESTION_EN
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

def request_openai_api(prompt_text):
    data = {**data_template, "prompt": prompt_text}

    try:
        response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
        response.raise_for_status()  # ステータスコードが200以外の場合は例外を発生させる

        response_json = response.json()
        result = response_json["choices"][0]["text"].strip()

    except (BaseException, Exception) as e:
        raise ValueError("Invalid response from API: {}".format(str(e)))

    return result

def generate_summary(title):
    prompt_text = GET_SUMARRY.format(title=title)
    summary = request_openai_api(prompt_text)
    return summary

def generate_question(title):
    prompt_text1 = GET_QUESTION.format(title=title)
    question = request_openai_api(prompt_text1)

    prompt_text2 = GET_QUESTION_EN.format(question=question)
    question_en = request_openai_api(prompt_text2)

    return question, question_en

@app.route('/')
def root():
    return redirect(url_for('index'))

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