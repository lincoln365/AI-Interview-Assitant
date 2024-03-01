from flask import Flask, request, send_file
from flask_cors import CORS
from openai import OpenAI
from io import BytesIO

app = Flask(__name__)
CORS(app)  # 允许跨域请求

client = OpenAI(api_key="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")

print("get ok 1")

@app.route('/api/speak', methods=['POST'])
def speak():
    data = request.get_json()
    if not data or 'text' not in data:
        return {"error": "Request body must include 'text' field"}, 400
    print("get ok 2")

    try:
        # 使用OpenAI的text-to-speech模型进行转换
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=data['text']
        )
        print("get ok 3")
        print(response)

        # 将生成的音频数据转换为二进制流
        audio_data = BytesIO(response.content)
        print("get ok 4")

        return send_file(audio_data, mimetype='audio/mp3', as_attachment=True, download_name="speech.wav")
       
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
