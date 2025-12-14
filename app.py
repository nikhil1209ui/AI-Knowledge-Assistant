from flask import Flask, request, jsonify
from rag_pipeline import generate_answer

app = Flask(__name__)

def agent_decision(question):
    keywords = ["document", "data", "explain", "define", "what is"]
    return any(word in question.lower() for word in keywords)

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")

    if agent_decision(user_question):
        answer = generate_answer(user_question)
        path = "RAG_USED"
    else:
        answer = "This question does not require document retrieval."
        path = "DIRECT_RESPONSE"

    return jsonify({
        "answer": answer,
        "agent_path": path
    })

if __name__ == "__main__":
    app.run(debug=True)
