import os
from dotenv import load_dotenv
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from flask import Flask, jsonify, request
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Read OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY must be set in .env file")

@app.route('/predict', methods=['POST'])
def predict():
    
    file = request.files['file']

    file.save(file.filename)

    agent = create_csv_agent(OpenAI(api_key=openai_api_key, temperature=0), file.filename, verbose=True)

    print(agent.agent.llm_chain.prompt.template)

    question = request.form['question']

    result = agent.run(question)

    os.remove(file.filename)

    return jsonify({'result': result})

if __name__ == '__main__':
  app.run(debug=True)
