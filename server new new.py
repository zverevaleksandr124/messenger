import socketio
import uvicorn
import os
from fastapi import FastAPI

# 1. Создаем сервер Socket.IO
# 'asgi' — здесь всегда маленькими буквами в кавычках
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# 2. Создаем приложение FastAPI
app = FastAPI()

# Хелсчек для Render (чтобы он видел, что сервер жив)
@app.get("/")
async def health_check():
    return {"status": "ok"}

# 3. Объединяем их
# ASGIApp — здесь ПЕРВЫЕ ЧЕТЫРЕ буквы БОЛЬШИЕ, потом App с большой. Это название класса.
socket_app = socketio.ASGIApp(sio, app)

# СОБЫТИЯ
@sio.event
async def connect(sid, environ):
    print(f"✅ Подключен: {sid}")

@sio.event
async def send_chat_message(sid, data):
    print(f"📩 Сообщение от {sid}: {data}")
    await sio.emit('receive_message', {
        "text": data.get("text"),
        "sender": sid
    })

@sio.event
async def disconnect(sid):
    print(f"❌ Отключен: {sid}")

# ТОЧКА ВХОДА
if __name__ == "__main__":
    # Берем порт из настроек Render
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(socket_app, host='0.0.0.0', port=port)