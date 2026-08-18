import telebot
import random

# 1. BU YERGA BOTFATHER BERGAN TOKENDINGIZNI QO'YING
BOT_TOKEN = "8867209550:AAGU54ELxJDK9jwdil2uvITuqem2cZLjGjY"

# 2. BU YERGA @userinfobot BERGAN O'ZINGIZNING SHAXSIY TELEGRAM ID RAQAMINGIZNI QO'YING
ADMIN_ID = 7662509798  # <--- Shu yerga o'z ID raqamingizni yozing (qo'shtirnoqsiz)

bot = telebot.TeleBot(BOT_TOKEN)

# Foydalanuvchilar ma'lumotlari (balans)
user_data = {}

# O'yin holati va ishtirokchilar
game_players = []
player_roles = {}
game_started = False

# Rollar va ularning mukofotlari tizimi
ROLES_REWARDS = {
    "Minior 💎": {"type": "diamonds", "amount": 6},
    "Joker 🃏": {"type": "diamonds", "amount": 6},
    "Kimyogar 🧪": {"type": "diamonds", "amount": 6},
    "Yollanma qotil 🎯": {"type": "diamonds", "amount": 5},
    "Konchi ⛏": {"type": "diamonds", "amount": 5},
    "Admiral 🎖": {"type": "diamonds", "amount": 4},
    "Sotqin 🎭": {"type": "diamonds", "amount": 4},
    "Qorbobo ❄️": {"type": "diamonds", "amount": 4},
    "Janob 🎩": {"type": "diamonds", "amount": 3},
    "Sehrgar 🔮": {"type": "diamonds", "amount": 3},
    "Komissar Katani 🕵️‍♂️": {"type": "diamonds", "amount": 2},
    "Don 👑": {"type": "diamonds", "amount": 2},
    "Qotil ⚔️": {"type": "diamonds", "amount": 2},
    "Laborant 🥼": {"type": "diamonds", "amount": 2},
    "Qaroqchi 🏴‍☠️": {"type": "diamonds", "amount": 2},
    "G'azabkor 😡": {"type": "diamonds", "amount": 1},
    "Mafia 🕶": {"type": "diamonds", "amount": 1},
    "Serjant 👮‍♂️": {"type": "diamonds", "amount": 1},
    "Aferist 🦊": {"type": "diamonds", "amount": 1},
    "Tulki 🦧": {"type": "diamonds", "amount": 1},
    "Fotoparatchi 📸": {"type": "diamonds", "amount": 1},
    "Zombi 🧟‍♂️": {"type": "money", "amount": 1000},
    "Robin Gud 🏹": {"type": "money", "amount": 1000},
    "Doktor ⛑": {"type": "money", "amount": 1000},
    "Kezuvchi 🚶‍♂️": {"type": "money", "amount": 500},
    "Advokat 💼": {"type": "money", "amount": 500},
    "Jurnalist 📰": {"type": "money", "amount": 500},
    "Afsungar 🧙‍♂️": {"type": "money", "amount": 500},
    "Bo'ri 🐺": {"type": "money", "amount": 500},
    "Oshpaz 👨‍🍳": {"type": "money", "amount": 500},
    "Hamshira 👩‍⚕️": {"type": "money", "amount": 400},
    "Rais 👔": {"type": "money", "amount": 400},
    "Daydi 🏕": {"type": "money", "amount": 400},
    "Suidsid 💀": {"type": "money", "amount": 300},
    "Ayg'oqchi 👁": {"type": "money", "amount": 300},
    "Omadli 🍀": {"type": "money", "amount": 250},
    "Tinch aholi 🧑‍🌾": {"type": "money", "amount": 100},
    "Faol rolni o'chirish ❌": {"type": "money", "amount": 100}
}

# Botga /start bosilganda ishlaydigan qism
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    if user_id not in user_data:
        user_data[user_id] = {"money": 0, "diamonds": 0}
        
    if user_id == ADMIN_ID:
        text = (f"Salom, Boss ({username})! 😎\n"
                f"Siz Meteor Mafia boti egasisiz.\n\n"
                f"💰 Pulingiz: ♾ CHEKSIZ\n"
                f"💎 Olmoslaringiz: ♾ CHEKSIZ\n\n"
                f"Guruhda o'yin boshlash: /start_mafia\n"
                f"O'yinni yakunlash va pullarni tarqatish: /oyun_tugadi")
    else:
        text = (f"Salom, {username}! Meteor Mafia o'yiniga xush kelibsiz. 🔥\n\n"
                f"Sizning balansingiz:\n"
                f"💰 Pul: {user_data[user_id]['money']}💵\n"
                f"💎 Olmos: {user_data[user_id]['diamonds']}💎")
    
    bot.send_message(message.chat.id, text)

# Guruhda o'yinga qo'shilish buyrug'i
@bot.message_handler(commands=['join'])
def join_game(message):
    global game_started
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    if game_started:
        bot.reply_to(message, "❌ O'yin allaqachon boshlanib ketgan. Keyingi o'yinni kuting.")
        return
        
    if user_id not in game_players:
        game_players.append(user_id)
        if user_id not in user_data:
            user_data[user_id] = {"money": 0, "diamonds": 0}
        bot.reply_to(message, f"✅ {username} o'yinga qo'shildi!\n👥 Jami o'yinchilar: {len(game_players)} ta")
    else:
        bot.reply_to(message, "Siz allaqachon o'yin ro'yxatidasiz.")

# O'yinni boshlash va rollarni tarqatish (Faqat ADMIN uchun)
@bot.message_handler(commands=['start_mafia'])
def start_mafia(message):
    global game_started, player_roles
    user_id = message.from_user.id
    
    if user_id != ADMIN_ID:
        bot.reply_to(message, "❌ Bu buyruqni faqat bot egasi (Admin) bera oladi!")
        return
        
    if len(game_players) < 2:
        bot.reply_to(message, "❌ O'yinni boshlash uchun kamida 2 ta odam /join orqali qo'shilishi kerak!")
        return
        
    game_started = True
    bot.send_message(message.chat.id, "🎲 Rollar barcha ishtirokchilarning shaxsiy xabariga (lichkasiga) yuborilmoqda...")
    
    # O'yinchilar soniga qarab rollar ro'yxatidan tasodifiy tanlab olish
    all_roles = list(ROLES_REWARDS.keys())
    available_roles = random.sample(all_roles, len(game_players))
    
    # Har bir o'yinchiga rolni yashirincha yuborish
    for index, p_id in enumerate(game_players):
        assigned_role = available_roles[index]
        player_roles[p_id] = assigned_role
        
        try:
            bot.send_message(p_id, f"🎭 METEOR MAFIA\n\nSizning o'yindagi yashirin rolingiz: **{assigned_role}**\n\nUni hech kimga ko'rsatmang!")
        except:
            pass

# O'yin tugaganda g'oliblarga avtomatik mukofot berish (Faqat ADMIN uchun)
@bot.message_handler(commands=['oyun_tugadi'])
def end_game_reward(message):
    global game_started, game_players, player_roles
    user_id = message.from_user.id
    
    if user_id != ADMIN_ID:
        bot.reply_to(message, "❌ Siz admin emassiz!")
        return
        
    if not game_started:
        bot.reply_to(message, "Hozir hech qanday faol o'yin ketmayapti.")
        return
        
    # Har bir o'yinchining roliga qarab pul yoki olmos o'tkazish
    for p_id in game_players:
        if p_id != ADMIN_ID:
            role = player_roles.get(p_id)
            if role in ROLES_REWARDS:
                reward_type = ROLES_REWARDS[role]["type"]
                reward_amount = ROLES_REWARDS[role]["amount"]
                
                if reward_type == "diamonds":
                    user_data[p_id]['diamonds'] += reward_amount
                    msg = f"🎉 O'yin tugadi!\n🎭 Rolingiz: {role}\nBalansingizga **{reward_amount}💎** qo'shildi!"
                else:
                    user_data[p_id]['money'] += reward_amount
                    msg = f"🎉 O'yin tugadi!\n🎭 Rolingiz: {role}\nBalansingizga **{reward_amount}💵** qo'shildi!"
                    
                try:
                    bot.send_message(p_id, msg)
                except:
                    pass

    bot.send_message(message.chat.id, "🏁 O'yin yakunlandi! Barcha ishtirokchilarning balansiga pullar va olmoslar roliga qarab avtomatik o'tkazildi. ✅")
    
    # Ma'lumotlarni tozalash
    game_players = []
    player_roles = {}
    game_started = False

print("Yangi rollar va mukofotlar tizimi yoqildi...")
bot.infinity_polling()
