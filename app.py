from flask import Flask, request, render_template, jsonify
import openai

app = Flask(__name__)

# ضع مفتاح API الخاص بك من OpenAI هنا
openai.api_key = 'YOUR_OPENAI_API_KEY'

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/create_ad', methods=['POST'])
def create_ad():
    project_type = request.form['project_type']
    features = request.form['features']
    target_audience = request.form['target_audience']
    languages = request.form['languages']
    platforms = request.form['platforms']
    payment_methods = request.form['payment_methods']
    additional_info = request.form['additional_info']

    # إعداد الموجه مع النص المخصص
    system_prompt = """You are a professional copywriter with more than 15 years of experience in crafting compelling ad copies for buying and selling platforms. You specialize in writing ad copies in Arabic. Use the information provided to create ad copies using different sales tactics such as AIDA. Ensure that the ad copy is engaging and tailored to the Arabic-speaking audience.

    Write ad copy following the best sales copywriter tactics, you should return only the ad copy without expalnation , the ad copy be ready to copy and past in the platform with out any human help and do not add any call to action ، and provide the feature as bullit points with emoji
    
    """

    user_prompt = f""" I want sell my business , please create ad to past it in buy and sell platform , here is the info about my ad , please only use arabic language 
    نوع المشروع: {project_type}
    ميزات المشروع: {features}
    الجمهور المستهدف: {target_audience}
    اللغات المدعومة: {languages}
    المنصات المدعومة: {platforms}
    طرق الدفع المدعومة: {payment_methods}
    معلومات إضافية: {additional_info}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000
    )

    ad_copy = response.choices[0].message['content'].strip()

    return jsonify({'ad_copy': ad_copy})

if __name__ == '__main__':
    app.run(debug=True)
