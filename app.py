from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    blog_content = ""
    if request.method == "POST":
        topic = request.form.get("topic")
        if topic:
            try:
                # نضع المفتاح مباشرة هنا ليقرأه الكود رغماً عن السيرفر
                client = Groq(api_key="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")
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"Write a comprehensive, professional blog post about: {topic}. Use proper HTML tags like <h2>, <p>, and <ul> for formatting.",
                        }
                    ],
                    model="llama3-8b-8192",
                )
                blog_content = chat_completion.choices[0].message.content
            except Exception as e:
                blog_content = f"Error generating blog: {str(e)}"
    
    return render_template("index.html", blog_content=blog_content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
