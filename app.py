from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# 🔑 Add your API key here
genai.configure(api_key="API_KEY")

model = genai.GenerativeModel("gemma-3n-e2b-it")

def generate_minutes(transcript):
    prompt = f"""
    You are a professional meeting assistant.

    Generate clean and formal meeting minutes.

    STRICT FORMAT:
    - No markdown symbols like ** or *
    - Use proper headings
    - Use bullet points where needed
    - Format action items as a clean table

    Sections:
    1. Summary
    2. Key Discussion Points
    3. Decisions Made
    4. Action Items (table with Person, Task, Deadline)

    Transcript:
    {transcript}
    """

    response = model.generate_content(prompt)
    return response.text

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""

    if request.method == "POST":
        transcript = request.form["transcript"]
        output = generate_minutes(transcript)

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True, port=5001)