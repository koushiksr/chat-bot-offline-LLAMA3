from flask import Flask, request ,jsonify
import os
from langchain_community.llms import Ollama
from pdfminer.high_level import extract_text
import uuid
app = Flask(__name__)
llama = Ollama(model="llama3")

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        if 'pdf' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        pdf_file = request.files['pdf']
        if pdf_file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        filename = str(uuid.uuid4()) + '.pdf'
        pdf_file.save(filename)
        if os.path.exists('pdf.pdf'):
            os.remove('pdf.pdf')
        os.rename(filename, 'pdf.pdf')
        return jsonify({"message": "PDF file uploaded successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_json(text):
    return text[text.find("```") + 3:text.rfind("```")].strip()

import logging

@app.route('/pd', methods=['POST'])
def process_pdf():
    try:
        prompt = extract_text('pdf.pdf') + " here is my data for a chat bot you should respond like chatbot, i need " + request.json['query'] + " if you don't know say don't know don't try to answer and i don't want any extra sentence, I need just a main content response and respond only the data we asked, we don't want other data."
        return {"answer": llama.invoke(prompt).replace("\n", " , ")}
    
    except FileNotFoundError:
        return jsonify({"error": "PDF file not found."}), 404
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
