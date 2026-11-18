import requests, json
from flask import Flask, request, render_template

app = Flask(__name__)

TOKEN = "f9LHodD0cOKrb1LhW6V162mTHV0veeSTjSkbWItM6pn_oXaYPVAVzSWETx_yv-6_9c0KBayeDp80cRS9aLdq"          
CHAT_ID = 955148439           
URL = "https://botapi.max.ru"
headers = {"Authorization": TOKEN}


@app.route("/")
def form_page():
        return render_template('form.html')

@app.route("/send-lead", methods=["POST"])
def send_lead():
    # Получаем данные из формы
    name = request.form.get("name", "Не указано")
    phone = request.form.get("phone", "Не указан")
    comment = request.form.get("comment", "")
    email = request.form.get("email", "Не указана")

    # Собираем сообщение
    text = f"📬 НОВАЯ ЗАЯВКА!\nИмя: {name}\nТелефон: {phone}\nПочта: {email}"
    if comment:
        text += f"\nКомментарий: {comment}"

        # --- НАЧАЛО ПОДСТРАХОВКИ ---
    try:
        with open("applications.txt", "a", encoding="utf-8") as f:
            f.write(text + "\n" + "="*30 + "\n")
    except Exception as e:
        print(f"Ошибка записи в файл: {e}")
    # --- КОНЕЦ ПОДСТРАХОВКИ ---

    # Отправляем в MAX (тот же способ, что и в bot.py)
    try:
        r = requests.post(
            f"{URL}/messages",
            params={"chat_id": CHAT_ID},
            headers=headers,
            json={"text": text},
            timeout=10
        )
        print("Сервер MAX ответил:", r.json())
    except Exception as e:
        print(f"Ошибка отправки в MAX: {e}")
        return {"status": "error"}, 500

    return {"status": "ok"}, 200

if __name__ == "__main__":
    print("Приёмник заявок запущен: http://127.0.0.1:5000/send-lead")
    app.run(port=5000)
