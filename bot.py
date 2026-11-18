import requests, time

TOKEN = "f9LHodD0cOKrb1LhW6V162mTHV0veeSTjSkbWItM6pn_oXaYPVAVzSWETx_yv-6_9c0KBayeDp80cRS9aLdq"
URL = "https://botapi.max.ru"
headers = {"Authorization": TOKEN}
marker = 0

print("Бот запущен. Жду сообщения…")

while True:
    try:
        # Запрос обновлений: marker нужен, чтобы не читать старые сообщения снова и снова
        r = requests.get(
            f"{URL}/updates",
            params={"marker": marker},
                headers=headers,
            timeout=35
        )
        data = r.json()
        print("Сервер ответил:", data)

        # Если в ответе есть ошибка от самого API (например, токен не тот)
        if not data.get("ok", True):
            print("Сервер MAX прислал ошибку:", data)
            break

        updates = data.get("updates", [])
        for u in updates:
            msg = u.get("message", {})
            if msg:
                body = msg.get("body", "")
                chat_id = msg["recipient"]["chat_id"]
                print(f"Пришло сообщение: '{body}' (chat_id={chat_id})")

                # Отправляем ответ
                resp = requests.post(
                    f"{URL}/messages",
                    params={"chat_id": chat_id},
                headers=headers,
                    json={"text": "Работает"}
                )
                print("Ответ отправлен.")

        marker = data.get("marker", marker)

    except requests.exceptions.ConnectTimeout:
        print("Таймаут: сервер не ответил за 5 секунд.")
    except requests.exceptions.ConnectionError:
        print("Нет соединения с сервером.")
    except Exception as e:
        print(f"Ошибка: {e}")

    time.sleep(2)
