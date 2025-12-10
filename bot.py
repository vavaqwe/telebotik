import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import config  
from database import *

bot = telebot.TeleBot(config.TELEGRAM_API)

@bot.message_handler(commands=['start'])
def main(message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

    bot.send_message(message.chat.id, f'Вітаю {us_name} цей бот надає послуги для замовлення фото-послуг')
    config.logging.info(f'[{us_id}] Вітаю {us_name} цей бот надає послуги для замовлення фото-послуг')

    show_main_menu(message)

def show_main_menu(message):
    us_id = message.from_user.id
    markup = ReplyKeyboardMarkup()
    itembtn1 = KeyboardButton('Замовити послугу')
    itembtn2 = KeyboardButton('Зарезервовані послуги')
    itembtn3 = KeyboardButton('Контакти')
    itembtn4 = KeyboardButton('Веб-сайт')
    itembtn5 = KeyboardButton('Підтримка')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

    bot.send_message(message.chat.id, "Головне меню:", reply_markup=markup)

def cancel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn = KeyboardButton('Відмінити')
    markup.add(itembtn)
    return markup

@bot.message_handler(content_types=['text'])
def func(message):
    us_id = message.from_user.id
    if message.text == "Замовити послугу":
        msg = bot.send_message(message.chat.id, "Введіть дату зйомки (наприклад 22.11.2025):", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(msg, step_date)

    elif message.text == "Послуги":
            # *** ОНОВЛЕНИЙ ТЕКСТ З ОПИСОМ ПОСЛУГ ***
            services_text = """
            **Наші Фотопослуги:**
            
            1. **Портретна зйомка (Індивідуальна)**
               — Створення професійних та художніх портретів. 
               — Ідеально для особистого бренду та профілів.
               — Тривалість: від 1 години.

            2. **Весільна та Репортажна зйомка**
               — Повне покриття важливих подій (весілля, корпоративи).
               — Фокус на емоціях та динаміці.
               — Формат: Пакет "Повний день" або погодинно.

            3. **Студійна зйомка**
               — Фотосесії в обладнаній студії з професійним світлом.
               — Підходить для Fashion, модельних тестів, Lookbook.

            4. **Бізнес-контент та Предметна зйомка**
               — Зйомка для каталогів, інтернет-магазинів та корпоративних потреб.
               — Створення контенту для соціальних мереж та реклами.
            
            5. **Ретуш та Обробка фотографій**
               — Професійна корекція кольору, світла та детальна ретуш.
               — Можна замовити як окрему послугу.
               
            Для **замовлення** або уточнення **цін** натисніть кнопку "Замовити послугу" або зверніться до "Підтримки".
            """
            bot.send_message(message.chat.id, text=services_text)

    elif message.text == "Контакти":
        bot.send_message(message.chat.id, text="Телефон адміністратора: +380960483935")

    elif message.text == "Веб-сайт":
        password, _ = get_password(us_id)
        if password is None:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('Так, давайте створити'),
                       KeyboardButton('Ні, мені це не потрібно'))
            bot.send_message(
                message.chat.id,
                "У вас немає паролю для сайту. Хочете його створити?",
                reply_markup=markup
            )
        else:
            bot.send_message(
                message.chat.id,
                f"""Ваші данні для входу : \nSite: http://192.168.1.114:5000/ \nLogin: {us_id}, \nPassword: {password}
                """
            )

    elif message.text == "Так, давайте створити":
        msg = bot.send_message(message.chat.id, "Введіть новий пароль для сайту:")
        bot.register_next_step_handler(msg, create_password)

    elif message.text == "Зарезервовані послуги":
        orders = db_table_orders(us_id)
        if not orders:   # это проверяет: None, [], пустота
            return None

        for order in orders:
            order_id = order[0]
            date = order[1]
            time = order[2]
            type = order[3]
            city = order[4]
            phone = order[5]
            tg_id = order[6]

            bot.send_message(message.chat.id, 
f"""У вас є зарезервована послуга:
Дата: {date}
Час: {time}
Тип: {type}
Місто: {city}
Телефон: {phone}""")

    elif message.text in ["Скасувати", "Ні, мені це не потрібно", "Відмінити"]:
        show_main_menu(message)

    elif message.text == "Підтримка":
        markup = cancel_keyboard()
        msg = bot.send_message(
            message.chat.id, 
            "🤖 Ви увійшли в режим AI-підтримки. Задайте своє питання. Бот відповість, використовуючи штучний інтелект.", 
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, ai_support_handler)

    else:
        bot.send_message(message.chat.id, text="Пробачте але я не розумію")

def ai_support_handler(message):
    if message.text in ["Скасувати", "Відмінити"]:
        show_main_menu(message)
        return

    try:
        from ai import ai_response # Забезпечуємо імпорт
        content = [{"role": "user", "parts": [{"text": message.text}]}]
        res = ai_response(content) 
        
        bot.send_message(message.chat.id, res)
    except ImportError:
        bot.send_message(message.chat.id, "Вибачте, функція AI не налаштована.")
        
    
    msg = bot.send_message(message.chat.id, "Задайте наступне питання або натисніть 'Відмінити' для повернення в Головне меню.", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, ai_support_handler)

def step_date(message):
    if message.text == 'Відмінити':
        show_main_menu(message)
        return

    date = message.text
    msg = bot.send_message(message.chat.id, "Введіть час зйомки (наприклад 10:30):", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, step_time, date)

def step_time(message, date):
    if message.text == 'Відмінити':
        show_main_menu(message)
        return

    time = message.text
    msg = bot.send_message(message.chat.id, "Тип зйомки (портрет / захід / інше):", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, step_type, date, time)

def step_type(message, date, time):
    if message.text == 'Відмінити':
        show_main_menu(message)
        return

    type_photo = message.text
    msg = bot.send_message(message.chat.id, "Місто зйомки:", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, step_city, date, time, type_photo)

def step_city(message, date, time, type_photo):
    if message.text == 'Відмінити':
        show_main_menu(message)
        return

    city = message.text
    msg = bot.send_message(message.chat.id, "Ваш телефон:", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, step_phone, date, time, type_photo, city)


def step_phone(message, date, time, type_photo, city):
    if message.text == 'Відмінити':
        show_main_menu(message)
        return
    phone = message.text
    user_id = message.from_user.id

    add_new_order(date, time, type_photo, phone, city, user_id)

    bot.send_message(message.chat.id, "Ваше замовлення прийнято! Я скоро з вами зв'яжусь", reply_markup=cancel_keyboard())
    show_main_menu(message)

def create_password(message):
    new_pass = message.text
    add_password(message.from_user.id, new_pass)
    bot.send_message(message.chat.id, "Пароль успішно створено")
    show_main_menu(message)


def run_bot():
    print('Бот запущений')
    bot.infinity_polling()