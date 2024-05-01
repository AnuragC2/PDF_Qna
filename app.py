from flask import Flask, render_template, request
import fitz  # PyMuPDF
import requests

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": "Bearer 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"}

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/get_answers', methods=['POST'])
def get_answers():
    if request.method == 'POST':
        if 'pdfFile' not in request.files:
            return "No PDF file uploaded"
        
        pdf_file = request.files['pdfFile']
        pdf_content = pdf_file.read()

        question = request.form['question']
        answer = query_answers(question, pdf_content)
        return answer

def query_answers(question, pdf_content):
    doc_text = extract_text_from_pdf(pdf_content)
    prompt =  f'''<|system|>
 You are a chatbot who gives one sentence answers, straight to the point.</s>
 <|user|>
 Here is the text from a document : {doc_text}, now based on this text, answer this: {question} </s>
 <|assistant|>'''
 
	
    output = query_model({
        "inputs": prompt,
    })
    print(output[0]['generated_text'].split('<|assistant|>')[1])
    return output[0]['generated_text'].split('<|assistant|>')[1]

def extract_text_from_pdf(pdf_content):
    doc = fitz.open(stream=pdf_content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def query_model(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    app.run(debug=False)
