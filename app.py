from flask import Flask, request, jsonify, render_template_string
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Blog Generator</title>
    <style>
        body { font-family: Arial; max-width: 700px; margin: 50px auto; padding: 20px; }
        input, select { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ddd; border-radius: 6px; }
        button { width: 100%; padding: 12px; background: #4A90E2; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }
        #result { margin-top: 20px; padding: 20px; background: #f9f9f9; border-radius: 6px; white-space: pre-wrap; display: none; }
    </style>
</head>
<body>
    <h2>AI Blog Generator</h2>
    <input type="text" id="topic" placeholder="اكتب موضوع المقال..." />
    <select id="tone">
        <option value="professional">احترافي</option>
        <option value="casual">عادي وبسيط</option>
        <option value="educational">تعليمي</option>
    </select>
    <button onclick="generate()">توليد المقال</button>
    <div id="result"></div>
    <script>
        async function generate() {
            const topic = document.getElementById("topic").value;
            const tone = document.getElementById("tone").value;
            document.getElementById("result").style.display = "block";
            document.getElementById("result").innerText = "جاري الكتابة...";
            const res = await fetch("/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ topic, tone })
            });
            const data = await res.json();
            document.getElementById("result").innerText = data.result;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    topic = data['topic']
    tone = data['tone']
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"Write a complete blog post about: {topic}. Tone: {tone}. Include title, introduction, sections with subheadings, and conclusion."
        }]
    )
    
    result = response.choices[0].message.content
    return jsonify({ "result": result })

if __name__ == '__main__':
    app.run(debug=True)
