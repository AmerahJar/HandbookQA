from flask import Flask, request, render_template, session
from flask_session import Session
from main import find_relevant_paragraph, get_answer, read_handbook_paragraphs

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []
    if request.method == "POST":
        if "action" in request.form and request.form["action"] == "reset":
            session['chat_history'] = []
        else:
            question = request.form.get("question")
            handbook_paragraphs = read_handbook_paragraphs('path/to/your/handbook.txt')  
            relevant_paragraph, _ = find_relevant_paragraph(question, handbook_paragraphs)
            answer = get_answer(question, relevant_paragraph)
            session['chat_history'].append({"question": question, "answer": answer})
        session.modified = True
    return render_template("index.html", chat_history=session.get('chat_history', []))

if __name__ == "__main__":
    app.run(debug=True)
