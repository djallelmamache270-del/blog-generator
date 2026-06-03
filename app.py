import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_blog():
    try:
        data = request.json
        topic = data.get('topic', '')

        if not topic:
            return jsonify({'error': 'Topic is required'}), 400

        completion = client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=[
                {
                    "role": "user",
                    "content": f"Write a professional, SEO-optimized blog post about: {topic}. Use professional HTML tags for formatting."
                }
            ],
            temperature=0.7,
            max_tokens=2048
        )

        blog_content = completion.choices[0].message.content
        return jsonify({'blog': blog_content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
