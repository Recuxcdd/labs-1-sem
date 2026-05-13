import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import json
import os

TOKEN = "8126573887:AAFvyKXDvaUyTTRZbE-fNo0iKkCgzLpHciM"
bot = telebot.TeleBot(TOKEN)

# =========================
# ====== ХРАНИЛИЩЕ ========
# =========================


USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")
ROUTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "routes")

# user_id: {shown_start: bool}
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


users = load_users()

# user state
user_state = {}


# =========================
# ====== МАРШРУТЫ =========
# =========================

def load_routes():
    routes = {}
    for file in os.listdir(ROUTES_DIR):
        if file.endswith(".json"):
            with open(os.path.join(ROUTES_DIR, file), encoding="utf-8") as f:
                route = json.load(f)
                routes[route["id"]] = route
    return routes


routes = load_routes()


# =========================
# ====== КЛАВИАТУРЫ =======
# =========================

def routes_keyboard():
    kb = InlineKeyboardMarkup()
    for r in routes.values():
        kb.add(InlineKeyboardButton(r["title"], callback_data=f"route:{r['id']}"))
    return kb


def route_screen_keyboard(route_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Начать маршрут", callback_data=f"start:{route_id}"))
    kb.add(InlineKeyboardButton("Назад", callback_data="back"))
    return kb


def point_keyboard(route_id, index):
    route = routes[route_id]
    total = len(route["points"])

    kb = InlineKeyboardMarkup()

    if index == 0:
        kb.add(InlineKeyboardButton("➡️", callback_data="next"))
        kb.add(InlineKeyboardButton("Уйти с маршрута", callback_data="exit_confirm"))

    elif index == total - 1:
        kb.add(InlineKeyboardButton("⬅️", callback_data="prev"))
        kb.add(InlineKeyboardButton("Завершить маршрут", callback_data="finish"))

    else:
        kb.row(
            InlineKeyboardButton("⬅️", callback_data="prev"),
            InlineKeyboardButton("➡️", callback_data="next")
        )
        kb.add(InlineKeyboardButton("Уйти с маршрута", callback_data="exit_confirm"))

    return kb


def exit_confirm_keyboard():
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("Нет", callback_data="exit_no"),
        InlineKeyboardButton("Да", callback_data="exit_yes")
    )
    return kb


def finish_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("К маршрутам", callback_data="to_routes"))
    return kb


# =========================
# ====== УТИЛИТЫ ==========
# =========================

def get_image_path(image: str):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", image)
    
    
def send_or_edit(call, text, keyboard=None, image=None):
    user_id = call.from_user.id
    msg_id = user_state.get(user_id, {}).get("message_id")

    try:
        if image:
            # bot.edit_message_text(
            #     text,
            #     chat_id=call.message.chat.id,
            #     message_id=msg_id,
            #     reply_markup=keyboard
            # )
            with open(get_image_path(image), 'rb') as image_file:
                bot.edit_message_media(
                    InputMediaPhoto(image_file, caption=text),
                    chat_id=call.message.chat.id,
                    message_id=msg_id,
                    reply_markup=keyboard
                )
        else:
            with open(get_image_path('one_pixel.png'), 'rb') as one_pixel:
                bot.edit_message_media(
                    InputMediaPhoto(one_pixel, caption=text),
                    chat_id=call.message.chat.id,
                    message_id=msg_id,
                    reply_markup=keyboard
                )
            # bot.edit_message_text(
            #     text,
            #     chat_id=call.message.chat.id,
            #     message_id=msg_id,
            #     reply_markup=keyboard
            # )
    except Exception as e:
        msg = bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        user_state[user_id]["message_id"] = msg.message_id
        print('SEND OR EDIT EXCEPTION')
        print(call.data, call, text)
        print(e)


# =========================
# ====== /start ===========
# =========================

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id

    if str(user_id) not in users:
        users[str(user_id)] = {"shown_start": False}

    if not users[str(user_id)]["shown_start"]:
        bot.send_message(
            message.chat.id,
            "👋 Добро пожаловать!\n\n"
            "Это интерактивный гид по историческим маршрутам.",
            parse_mode='HTML'
        )
        users[str(user_id)]["shown_start"] = True
        save_users(users)

    msg = bot.send_message(
        message.chat.id,
        "Выберите маршрут:",
        reply_markup=routes_keyboard(),
        parse_mode='HTML'
    )

    user_state[user_id] = {
        "route_id": None,
        "point_index": 0,
        "message_id": msg.message_id
    }
    print(user_state)


# =========================
# ===== CALLBACK ==========
# =========================

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    data = call.data

    if user_id not in user_state:
        return

    # ===== ВЫБОР МАРШРУТА =====
    if data.startswith("route:"):
        route_id = data.split(":")[1]
        route = routes[route_id]

        user_state[user_id]["route_id"] = route_id

        text = (
            f"<b>{route['title']}</b>\n\n"
            f"{route['description']}\n\n"
            f"⏱ Время: {route['time']}\n"
            f"📍 Точек: {len(route['points'])}"
        )

        send_or_edit(call, text, route_screen_keyboard(route_id), route.get("image"))

    # ===== НАЧАТЬ =====
    elif data.startswith("start:"):
        route_id = data.split(":")[1]
        user_state[user_id]["point_index"] = 0
        show_point(call)

    # ===== ПОКАЗ ТОЧКИ =====
    elif data in ["next", "prev"]:
        if data == "next":
            user_state[user_id]["point_index"] += 1
        else:
            user_state[user_id]["point_index"] -= 1

        show_point(call)

    # ===== ВЫХОД =====
    elif data == "exit_confirm":
        send_or_edit(call, "Точно уйти?", exit_confirm_keyboard())

    elif data == "exit_no":
        show_point(call)

    elif data == "exit_yes":
        send_or_edit(call, "Выберите маршрут:", routes_keyboard())

    # ===== ЗАВЕРШЕНИЕ =====
    elif data == "finish":
        route = routes[user_state[user_id]["route_id"]]

        try:
            bot.edit_message_reply_markup(
                call.message.chat.id,
                user_state[user_id]["message_id"],
                reply_markup=None
            )
        except:
            pass

        send_or_edit(
            call,
            f"🎉 Вы прошли маршрут {route['title']}, поздравляем!",
            finish_keyboard()
        )

    elif data == "to_routes":
        route = routes[user_state[user_id]["route_id"]]
        send_or_edit(call, f"🎉 Вы прошли маршрут {route['title']}, поздравляем!")
        msg = bot.send_message(
            call.message.chat.id,
            "Выберите маршрут:",
            reply_markup=routes_keyboard(),
            parse_mode='HTML'
        )
        user_state[user_id]["message_id"] = msg.message_id

    # ===== НАЗАД =====
    elif data == "back":
        send_or_edit(call, "Выберите маршрут:", routes_keyboard())


# =========================
# ===== ПОКАЗ ТОЧКИ =======
# =========================

def show_point(call):
    user_id = call.from_user.id
    state = user_state[user_id]

    route = routes[state["route_id"]]
    point = route["points"][state["point_index"]]

    text = f"<b>{point['title']}</b>\n\n{point['text']}"

    send_or_edit(
        call,
        text,
        point_keyboard(state["route_id"], state["point_index"]),
        point["image"]
    )


# =========================
# ===== ЗАПУСК ============
# =========================

bot.infinity_polling(timeout=10, long_polling_timeout=5)