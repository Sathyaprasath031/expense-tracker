from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
FILE_NAME = "expenses.csv"

# Create CSV if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Amount"])

def read_expenses():
    expenses = []
    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            expenses.append(row)
    return expenses

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        amount = request.form["amount"]

        with open(FILE_NAME, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date, category, amount])

        return redirect("/")

    expenses = read_expenses()
    total = sum(float(e[2]) for e in expenses)
    return render_template("index.html", expenses=expenses, total=total)

if __name__ == "__main__":
    app.run(debug=True)
