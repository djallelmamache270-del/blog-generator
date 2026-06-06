from flask import Flask, render_template, request
import google.generativeai as genai
import os

app = Flask(__name__)

# جلب مفتاح جيميناي بأمان من السيرفر
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        print("✅ Gemini API Key configured successfully!")
    except Exception as e:
        print(f"❌ Error configuring Gemini API: {str(e)}")
else:
    print("⚠️ WARNING: GOOGLE_API_KEY is missing!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form.get('topic')
    if not topic:
        return "من فضلك أدخل عنواناً للمقال", 400
        
    if not GOOGLE_API_KEY:
        return """
        <div style="direction: rtl; font-family: sans-serif; padding: 40px; max-width: 800px; margin: auto; background: #121212; color: #ff3333; border-radius: 10px; border: 1px solid #ff3333;">
            <h2>❌ عذراً، لم يتم تفعيل مفتاح الذكاء الاصطناعي!</h2>
            <p>يرجى التأكد من إضافة متغير البيئة <b>GOOGLE_API_KEY</b> داخل تبويب Variables في لوحة تحكم Railway.</p>
            <br>
            <a href="/" style="color: #00ffcc; text-decoration: none; font-weight: bold;">⬅️ العودة للموقع</a>
        </div>
        """, 500
        
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"اكتب مقالاً احترافياً وحصرياً باللغة العربية متوافقاً مع السيو (SEO) عن موضوع: {topic}. يجب أن يحتوي المقال على مقدمة، عناوين فرعية، وخاتمة."
        response = model.generate_content(prompt)
        article_text = response.text
        
        return f"""
        <div style="direction: rtl; font-family: sans-serif; padding: 40px; max-width: 800px; margin: auto; background: #121212; color: white; border-radius: 10px;">
            <h1 style="color: #00ffcc;">المقال المولد:</h1>
            <hr style="border-color: #333;">
            <div style="line-height: 1.8; font-size: 18px;">{article_text.replace('\n', '<br>')}</div>
            <br>
            <a href="/" style="color: #00ffcc; text-decoration: none; font-weight: bold;">⬅️ العودة للموقع وتوليد مقال آخر</a>
        </div>
        """
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(e)}", 500
