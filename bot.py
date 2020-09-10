import telebot

bot = telebot.TeleBot('token')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в TravelBot! Удачных путешествий!')
    bot.send_message(message.chat.id, 'Выберите страну:\r\n' \
    + 'Доступные страны:\r\nИталия\r\nTODO...')


@bot.message_handler(content_types=['text'])
def send_text(message):
<<<<<<< Updated upstream
    if message.text == 'Италия':
        bot.send_message(message.chat.id, 'Не советуем вам сейчас путешествовать в италию monkaS')
=======
    countries, users = globals()['countries'], globals()['users']
    db = sqlite3.connect("zabase.db")
    cursor = db.cursor()

    text = message.text.strip().capitalize()
    iden = str(message.from_user.id)

    markup0 = telebot.types.ReplyKeyboardMarkup()
    markup0.row('Вернуться к выбору страны')

    markup1 = telebot.types.ReplyKeyboardMarkup()
    markup1.row('Вернуться к выбору страны')
    markup1.row('Вернуться к выбору города')

    if iden not in users:
        cursor.execute("INSERT INTO userinfo(user_id) VALUES(?)", [(iden)])
        db.commit()
        globals()['users'][iden] = users[iden] = {"country": None, "city": None}

    if users[iden]["country"] and text == "Вернуться к выбору страны":
        globals()["users"][iden]["country"] = None
        cursor.execute("UPDATE userinfo SET country=NULL WHERE user_id=?", [(iden)])
        s = ""
        for i in countries:
            s += i + '\r\n'
        bot.send_message(message.chat.id, 'Выберите страну:\r\nДоступные страны:\r\n' + s[:-2], 
        reply_markup=telebot.types.ReplyKeyboardRemove())
        db.commit()
        return

    if not users[iden]["country"] and text not in countries:
        bot.send_message(message.chat.id, 'Страны {} не существует или не внесена в нашу базу('.format(message.text))
    elif not users[iden]["country"]:
        globals()['users'][iden] = {"country": text, "city": None}
        cursor.execute("UPDATE userinfo SET country=? WHERE user_id=?", [(text), (iden)])
        s = ""
        for row in cursor.execute('''SELECT city.name FROM city JOIN country c ON ctr_id = c.id
        WHERE c.name=?''', [(text)]):
            s += row[0] + '\r\n'
        bot.send_message(message.chat.id, 'Выбрана страна {}\r\nВыберите город:\r\n{}'.format(text, s[:-2]), reply_markup=markup0)
        db.commit()
        return

    if users[iden]["city"] and text == "Вернуться к выбору города":
        globals()["users"][iden]["city"] = None
        cursor.execute("UPDATE userinfo SET city=NULL WHERE user_id=?", [(iden)])
        s = ""
        for row in cursor.execute('''SELECT city.name FROM city JOIN country c ON ctr_id = c.id
        WHERE c.name=?''', [(users[iden]["country"])]):
            s += row[0] + '\r\n'
        bot.send_message(message.chat.id,
        'Выбрана страна {}\r\nВыберите город:\r\n{}'.format(users[iden]["country"], s[:-2]), reply_markup=markup0)
        db.commit()
        return
    
    if users[iden]["country"] and not users[iden]["city"]:
        city = cursor.execute('''SELECT city.name FROM city JOIN country c ON ctr_id = c.id
        WHERE city.name=? AND c.name=?''', [(text), (users[iden]["country"])]).fetchone()
        if not city:
            bot.send_message(message.chat.id, 'Города {} не существует или он не внесен в нашу базу('.format(message.text))
        else:
            globals()["users"][iden]["city"] = text
            cursor.execute("UPDATE userinfo SET city=? WHERE user_id=?", [(text), (iden)])
            bot.send_message(message.chat.id, 'Выбран город {}\r\nСписок достопримечательностей:\r\n'.format(text), reply_markup=markup1)
            db.commit()
        return

    if users[iden]["city"]:
        unit = {}
        for row in cursor.execute(
                '''SELECT id, name, description, location, photo FROM Unit WHERE Unit.city_id = (SELECT City.id FROM City JOIN userinfo on City.name = userinfo.city)'''):
            unit[row[0]] = {"name": row[1], "description": row[2], "location": row[3], "photo": row[4]}
        choosen = unit[random.randint(0, len(unit) - 1)]
        text = str(choosen["name"]) + ":\r\n" + str(choosen["description"]) + "\r\n" + str(choosen["location"])
        bot.send_message(message.chat.id, text)
        pass
>>>>>>> Stashed changes

bot.polling()