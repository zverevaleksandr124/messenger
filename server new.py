import socketio
import uvicorn
import os
from fastapi import FastAPI

# 1. Создаем сервер Socket.IO (асинхронный)
# cors_allowed_origins='*' критически важен для работы через интернет
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# 2. Создаем приложение FastAPI
app = FastAPI()

# 3. Объединяем их
socket_app = socketio.ASGIApp(sio, app)

# СОБЫТИЕ: Подключение
@sio.event
async def connect(sid, environ):
    print(f"✅ Устройство подключилось! ID сессии: {sid}")

# СОБЫТИЕ: Получение сообщения
@sio.event
async def send_chat_message(sid, data):
    # Логируем в консоль хостинга (ты увидишь это в панели управления)
    print(f"📩 Новое сообщение от {sid}: {data}")
    
    # Рассылаем всем
    await sio.emit('receive_message', {
        "text": data.get("text"),
        "sender": sid,
        "time": "сейчас"
    })

# СОБЫТИЕ: Отключение
@sio.event
async def disconnect(sid):
    print(f"❌ Устройство вышло из сети: {sid}")

# ТОЧКА ВХОДА
if __name__ == "__main__":
    # Хостинг сам передает номер порта через переменную окружения PORT
    # Если её нет (запуск локально), используем 8000
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Сервер запускается на порту {port}...")
    
    # Запускаем через uvicorn
    uvicorn.run(socket_app, host='0.0.0.0', port=port)

