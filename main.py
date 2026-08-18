import telebot
import random

# 1. BOT TOKENINGIZ TAYYOR TURIBDI
BOT_TOKEN = "8867209550:AAGU54ELxJDK9jwdil2uvITuqem2cZLjGjY"

# 2. BU YERGA O'ZINGIZNING TELEGRAM ID RAQAMINGIZNI YOZING
ADMIN_ID = 7662509798  # <--- Shuni o'zingizniki bilan almashtiring

bot = telebot.TeleBot(BOT_TOKEN)

# Foydalanuvchilar ma'lumotlari (balans va sotib olingan faol rol)
user_data = {}

# O'yin holati va ishtirokchilar
game_players = []
player_roles = {}
game_started = False

# Rollar va ularning mukofotlari tizimi
ROLES_REWARDS = {
    "Minior 💎": {"type": "diamonds", "amount": 6, "price": 3000},
    "Joker 🃏": {"type": "diamonds", "amount": 6, "price": 3000},
    "Kimyogar 🧪": {"type": "diamonds", "amount": 6, "price": 3000},
    "Yollanma qotil 🎯": {"type": "diamonds", "amount": 5, "price": 2500},
    "Konchi ⛏": {"type": "diamonds", "amount": 5, "price": 2500},
    "Admiral 🎖": {"type": "diamonds", "amount": 4, "price": 2000},
    "Sotqin 🎭": {"type": "diamonds", "amount": 4, "price": 2000},
    "Qorbobo ❄️": {"type": "diamonds", "amount": 4, "price": 2000},
    "Janob 🎩": {"type": "diamonds", "amount": 3, "price": 1500},
    "Sehrgar 🔮": {"type": "diamonds", "amount": 3, "price": 1500},
    "Komissar Katani 🕵️‍♂️": {"type": "diamonds", "amount": 2, "price": 1000},
    "Don 👑": {"type": "diamonds", "amount": 2, "price": 2000},
    "Qotil ⚔️": {"type": "diamonds", "amount": 2, "price": 1000},
    "Laborant 🥼": {"type": "diamonds", "amount": 2, "price": 1000},
    "Qaroqchi 🏴‍☠️": {"type": "diamonds", "amount": 2, "price": 1000},
    "G'azabkor 😡": {"type": "diamonds", "amount": 1, "price": 500},
    "Mafia 🕶": {"type": "diamonds", "amount": 1, "price": 500},
    "Serjant 👮‍♂️": {"type": "diamonds", "amount": 1, "price": 500},
    "Aferist 🦊": {"type": "diamonds", "amount": 1, "price": 500},
    "Tulki 🦧": {"type": "diamonds", "amount": 1, "price": 500},
    "Fotoparatchi 📸": {"type": "diamonds", "amount": 1, "price": 500},
    "Zombi 🧟‍♂️": {"type": "money", "amount": 1000, "price": 1200},
    "Robin Gud 🏹": {"type": "money", "amount": 1000, "price": 1200},
    "Doktor ⛑": {"type": "money", "amount": 1000, "price": 1200},
    "Kezuvchi 🚶‍♂️": {"type": "money", "amount": 500, "price": 700},
    "Advokat 💼": {"type": "money", "amount": 500, "price": 700},
    "Jurnalist 📰": {"type": "money", "amount": 500, "price": 700},
    "Afsungar 🧙‍♂️": {"type": "money", "amount": 500, "price": 700},
    "Bo'ri 🐺": {"type": "money", "amount": 500, "price": 700},
    "Oshpaz 👨‍🍳": {"type": "money", "amount": 500, "price": 700},
    "Hamshira 👩‍⚕️": {"type": "money", "amount": 400, "price": 500},
    "Rais 👔": {"type": "money", "amount": 400, "price": 500},
    "Daydi 🏕": {"type": "money", "amount": 400, "price": 500},
    "Suidsid 💀": {"type": "money", "amount": 300, "price": 400},
    "Ayg'oqchi 👁": {"type": "money", "amount": 300, "price": 400},
    "Omadli 🍀": {"type": "money", "amount": 250, "price": 300},
    "Tinch aholi 🧑‍🌾": {"type": "money", "amount": 100, "price": 150}
}

# Foydalanuvchini tekshirish funksiyasi
def check_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"money": 500, "diamonds": 0, "bought_role": None}

# Botga /start bosilganda
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    check_user(user_id)
        
    if user_id == ADMIN_ID:
        text = (f"Salom, Boss ({username})! 😎\n"
                f"Siz bot egasisiz. Sizda resurslar cheksiz!\n\n"
                f"💰 Pulingiz: ♾ CHEKSIZ\n"
                f"💎 Olmoslaringiz: ♾ CHEKSIZ\n\n"
                f"O'yin buyruqlari: /start_mafia , /oyun_tugadi\n"
                f"Admin buyruqlari: `/plus_pul ID MIQDOR` , `/plus_olmos ID MIQDOR`")
    else:
        bought = user_data[user_id]['bought_role'] if user_data[user_id]['bought_role'] else "Yo'q"
        text = (f"Salom, {username}! Meteor Mafia o'yiniga xush kelibsiz. 🔥\n\n"
                f"Sizning balansingiz:\n"
                f"💰 Pul: {user_data[user_id]['money']}💵\n"
                f"💎 Olmos: {user_data[user_id]['diamonds']}💎\n"
                f"🛒 Sotib olingan rol: **{bought}**\n\n"
                f"Buyruqlar:\n"
                f"🛍 Rollar do'koni: /magazin\n"
                f"💸 O'yinchiga pul o'tkazish: `/perevod ID MIQDOR`")
    
    bot.send_message(message.chat.id, text)

# ---- 💸 O'YINCHILAR BIR-BIRIGA PUL O'TKAZISH TIZIMI ----
@bot.message_handler(commands=['perevod'])
def transfer_money(message):
    user_id = message.from_user.id
    check_user(user_id)
    try:
        args = message.text.split()
        target_id = int(args[1])
        amount = int(args[2])
        
        if amount <= 0:
            bot.reply_to(message, "❌ Noto'g'ri miqdor!")
            return
            
        if user_id != ADMIN_ID and user_data[user_id]['money'] < amount:
            bot.reply_to(message, "❌ Balansingizda yetarli pul yo'q!")
            return
            
        check_user(target_id)
        
        if user_id != ADMIN_ID:
            user_data[user_id]['money'] -= amount
            
        user_data[target_id]['money'] += amount
        
        bot.reply_to(message, f"✅ ID: {target_id} foydalanuvchiga {amount}💵 muvaffaqiyatli o'tkazildi!")
        bot.send_message(target_id, f"💰 Guruhdoshingizdan hisobingizga {amount}💵 pul kelib tushdi!")
    except:
        bot.reply_to(message, "❌ Noto'g'ri format! `/perevod [ID] [MIQDOR]` deb yozing.")

# ---- 🛍 ROLLAR DO'KONI (MAGAZIN) ----
@bot.message_handler(commands=['magazin'])
def show_shop(message):
    text = "🛒 **METEOR MAFIA ROLLAR DO'KONI** 🛒\n\nSotib olish uchun `/sotib_ol ROL_NOMI` deb yozing. (Masalan: `/sotib_ol Don 👑`)\n\n**Rollar va narxlari:**\n"
    for role, info in ROLES_REWARDS.items():
        text += f"• {role} — {info['price']}💵\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['sotib_ol'])
def buy_role(message):
    user_id = message.from_user.id
    check_user(user_id)
    role_name = message.text.replace("/sotib_ol ", "").strip()
    
    if role_name not in ROLES_REWARDS:
        bot.reply_to(message, "❌ Bunday rol do'konda topilmadi! Nomini aniq yozing.")
        return
        
    price = ROLES_REWARDS[role_name]['price']
    
    if user_id != ADMIN_ID and user_data[user_id]['money'] < price:
        bot.reply_to(message, f"❌ Sizda yetarli pul yo'q! Bu rol {price}💵 turadi.")
        return
        
    if user_id != ADMIN_ID:
        user_data[user_id]['money'] -= price
        
    user_data[user_id]['bought_role'] = role_name
    bot.reply_to(message, f"🎉 Tabriklaymiz! Siz **{role_name}** rolini sotib oldingiz. Keyingi o'yinda ushbu rol sizga aniq tushadi! ✅")

# ---- ADMIN UCHUN TEKIN PUL/OLMOS BERISH BUYRUQLARI ----
@bot.message_handler(commands=['plus_pul'])
def add_money_admin(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        target_id, amount = int(args[1]), int(args[2])
        check_user(target_id)
        user_data[target_id]['money'] += amount
        bot.reply_to(message, f"✅ ID: {target_id} ga {amount}💵 berildi!")
    except: bot.reply_to(message, "Format: `/plus_pul ID MIQDOR`")

@bot.message_handler(commands=['plus_olmos'])
def add_diamonds_admin(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        target_id, amount = int(args[1]), int(args[2])
        check_user(target_id)
        user_data[target_id]['diamonds'] += amount
        bot.reply_to(message, f"✅ ID: {target_id} ga {amount}💎 berildi!")
    except: bot.reply_to(message, "Format: `/plus_olmos ID MIQDOR`")

# Guruhda o'yinga qo'shilish
@bot.message_handler(commands=['join'])
def join_game(message):
    global game_started
    user_id = message.from_user.id
    username = message.from_user.first_name
    if game_started: return
    if user_id not in game_players:
        game_players.append(user_id)
        check_user(user_id)
        bot.reply_to(message, f"✅ {username} qo'shildi! (Jami: {len(game_players)} ta)")

# O'yinni boshlash va rollarni tarqatish
@bot.message_handler(commands=['start_mafia'])
def start_mafia(message):
    global game_started, player_roles
    if message.from_user.id != ADMIN_ID: return
    if len(game_players) < 2:
        bot.reply_to(message, "❌ Kamida 2 ta o'yinchi kerak!")
        return
        
    game_started = True
    bot.send_message(message.chat.id, "🎲 Rollar lichkalarga yuborilmoqda...")
    
    # Do'kondan rol sotib olganlarni birinchi joylashtiramiz
    all_roles = list(ROLES_REWARDS.keys())
    random.shuffle(all_roles)
    
    for p_id in game_players:
        # Agar odam rol sotib olgan bo'lsa, o'sha rolni beramiz
        if user_data[p_id]['bought_role'] and user_data[p_id]['bought_role'] in all_roles:
            chosen_role = user_data[p_id]['bought_role']
            player_roles[p_id] = chosen_role
            all_roles.remove(chosen_role)
            user_data[p_id]['bought_role'] = None # Ishlatilingandan keyin do'kon rolini o'chiramiz
        else:
            player_roles[p_id] = None

    # Rol sotib olmaganlarga tasodifiy qolgan rollarni beramiz
    for p_id in game_players:
        if player_roles[p_id] is None:
            chosen_role = all_roles.pop(0)
            player_roles[p_id] = chosen_role
            
        try:
            bot.send_message(p_id, f"🎭 **METEOR MAFIA**\n\nSizning rolingiz: **{player_roles[p_id]}**")
        except: pass

# O'yin tugaganda mukofotlash
@bot.message_handler(commands=['oyun_tugadi'])
def end_game_reward(message):
    global game_started, game_players, player_roles
    if message.from_user.id != ADMIN_ID or not game_started: return
        
    for p_id in game_players:
        if p_id != ADMIN_ID:
            role = player_roles.get(p_id)
            if role in ROLES_REWARDS:
