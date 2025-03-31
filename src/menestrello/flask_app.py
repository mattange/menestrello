from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        text = request.form.get("text")
        words = request.form.get("words")
        
        # Process the words into a list
        word_list = [word.strip() for word in words.split(",") if word.strip()]
        
        # Render the results page
        return render_template("results.html", text=text, words=word_list)
    
    # Render the form page
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
