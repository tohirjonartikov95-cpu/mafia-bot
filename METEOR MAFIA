import telebot

# 1. BU YERGA BOTFATHER BERGAN TOKENNI QO'YING
BOT_TOKEN = "BU_YERGA_TOKENNI_QOYING"

# 2. BU YERGA @userinfobot BERGAN ID RAQAMINGIZNI QO'YING
ADMIN_ID = 123456789  

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start_game(message):
  user_id = message.from_user.id
  username = message.from_user.first_name

  if user_id not in user_data:
    user_data[user_id] = {"money": 0, "diamonds": 0}

  if user_id == ADMIN_ID:
    text = (f"Salom, Boss ({username})!\n"
            f"Siz bot adminisiz.\n"
            f"Sizning balansingiz: ♾ Cheksiz Pul va 💎 Cheksiz Olmos!")
  else:
    text = (f"Salom, {username}! O'yinga xush kelibsiz.\n"
            f"Sizning balansingiz:\n"
            f"💰 Pul: {user_data[user_id]['money']} so'm\n"
            f"💎 Olmos: {user_data[user_id]['diamonds']} ta")

  bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['oyun_tugadi'])
def end_game_reward(message):
  user_id = message.from_user.id

  if user_id != ADMIN_ID:
    bot.reply_to(message, "Siz admin emassiz, bu buyruqni bera olmaysiz!")
    return

  if not user_data:
    bot.reply_to(message, "Botda hali hech kim ro'yxatdan o'tmagan.")
    return

  for player_id in user_data.keys():
    if player_id != ADMIN_ID:
      user_data[player_id]['money'] += 5000
      user_data[player_id]['diamonds'] += 5
      try:
        bot.send_message(player_id, "🎉 O'yin tugadi! Admin tomonidan sizga 💰 5000 pul va 💎 5 olmos berildi!")
      except:
        pass

  bot.reply_to(message, "O'yin tugadi! Hammaga pullar tarqatildi. ✅")

print("Bot muvaffaqiyatli ishga tushdi...")
bot.infinity_polling()
