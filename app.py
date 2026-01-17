from flask import Flask, render_template_string, request

app = Flask(__name__)

DATA_FILE = "votes.txt"

def load_national_ids():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

def save_national_id(national_id):
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(national_id + "\n")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>نظام التصويت الإلكتروني</title>
</head>
<body style="font-family: Arial; text-align:center; direction:rtl">

    <h2>نظام التصويت الإلكتروني</h2>

    <form method="post">
        <input type="text" name="national_id" placeholder="الرقم القومي"><br><br>
        <input type="text" name="image_name" placeholder="اسم صورة البطاقة"><br><br>

        <p>اختر المرشح:</p>
        <input type="radio" name="candidate" value="أحمد"> أحمد<br>
        <input type="radio" name="candidate" value="محمود"> محمود<br>
        <input type="radio" name="candidate" value="منى"> منى<br><br>

        <button type="submit">تصويت</button>
    </form>

    <p style="color:red;">{{ error }}</p>
    <p style="color:green;">{{ success }}</p>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    error = ""
    success = ""

    if request.method == "POST":
        national_id = request.form.get("national_id", "").strip()
        image_name = request.form.get("image_name", "").strip()
        choice = request.form.get("candidate", "")

        if national_id == "" or image_name == "":
            error = "من فضلك املأ كل البيانات"
        else:
            national_ids = load_national_ids()

            if national_id in national_ids:
                error = "لا يمكن إدخال الرقم القومي مرة أخرى ❌"
            elif choice not in ["أحمد", "محمود", "منى"]:
                error = "اختر مرشح"
            else:
                save_national_id(national_id)
                success = "تم التصويت بنجاح ✅ شكراً لمشاركتك 🤍"

    return render_template_string(HTML_PAGE, error=error, success=success)

if __name__ == "__main__":
    app.run(debug=True)
