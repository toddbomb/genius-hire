from flask import Flask, request
from langchain.schema import HumanMessage
from query_data import get_pdf_qa_chain_response

app = Flask(__name__)

app.config['CORS_ALLOWED_ORIGINS'] = ['http://localhost:3000']

@app.route('/chat', methods=['POST'])
def prompt():
    content = request.get_json()

    query = content[0][len(content[0])-1]['content']

    model_response = get_pdf_qa_chain_response(query=query)

    return model_response


if __name__ == "__main__":
  app.run(port=5000, debug=True)