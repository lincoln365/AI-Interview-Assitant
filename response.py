from flask import Flask, request, jsonify
from flask_cors import CORS
import openai  # 修改为正确的导入方式

# 使用环境变量或其他安全方式来存储和读取您的 API 密钥
client = openai.OpenAI(api_key="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")

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/api/interview', methods=['POST'])
def interview():
    # 解析 JSON 请求体
    data = request.get_json()  # 使用 get_json 方法安全地解析 JSON 数据
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # 提取请求数据
    job = data.get('job')
    jobDescription = data.get('jobDescription')
    cv = data.get('cv')
    userAnswer = data.get('userAnswer')
    questions = data.get('questions')
    
    print("get ok")

    # 验证所有必需的字段是否都已提供
    if None in (job, jobDescription, cv, userAnswer):
        print("missing")
        return jsonify({"error": "Missing data for the interview process"}), 400

    try:
        # 根据提供的信息生成提示文本
        prompt = f"Based on the following CV: {cv}, job: {job}, job description: {jobDescription}, and the candidate's previous answers: {userAnswer}, evaluate the response, highlighting areas for improvement and how it could better combine with the CV to handle the question:{questions}(Limiedt in 100 words). "
        print("get ok 11")

        # 调用 OpenAI API 生成回答
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",  # 根据需要调整模型
            prompt=prompt,
            temperature=0.5,
            max_tokens=500
        )
        print("get ok 2")

        # 提取生成的文本
        generated_text = response.choices[0].text.strip()
        print(generated_text)

        return jsonify({"response": generated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/generate_question', methods=['POST'])
def generate_question():
    data = request.get_json()
    cv = data.get('cv')
    job = data.get('job')
    job_description = data.get('jobDescription')
    user_answers = data.get('userans')

    # Combine user answers into a single text
    answers_text = ' '.join(user_answers)

    # Create a prompt for GPT-3 to generate a new question
    prompt = f"Based on the following CV: {cv}, job: {job}, job description: {job_description}, and the candidate's previous answers: {answers_text}, generate a relevant interview question in 30 word, here is an example How long did it take you to complete this coding task (in months)? something like this."

    print(prompt)

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.5,
        max_tokens=500
    )
    print("ok to get response")

    next_question = response.choices[0].text.strip()

    print(next_question+"ok to get response")

    return jsonify({"nextQuestion": next_question})

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    data = request.get_json()
    cv = data.get('cv')
    job = data.get('job')
    job_description = data.get('jobDescription')
    user_answers = data.get('userAnswers')
    questions = data.get('questions')

    # Combine user answers and questions into a single text
    interview_text = ' '.join([f"Q: {q} A: {a}" for q, a in zip(questions, user_answers)])

    # Create a prompt for GPT-3 to generate a report blog
    prompt = f"HTML Code and CSS code Implemetation:Based on the following CV: {cv}, job: {job}, job description: {job_description}, and the interview Q&A: {interview_text}, generate a well-written blog in HTML and css code (Not plain text)in one files use <style> which need to be colored and beautiful that analyzes the interview with clear points and suggestions.You need to split the point. The exact structure is 1. background of the interview 2. strengths of the interview answers 3. areas for improvement 4. suggestions for the formal interview. It needs to have subheadings and be divided into h1 h2 like this. Then there needs to be typography. limited in 150 words"
    print(prompt)

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.5,
        max_tokens=500
    )

    report_blog = response.choices[0].text.strip()

    return jsonify({"report": report_blog})





if __name__ == '__main__':
    app.run(debug=True, port=5000)
