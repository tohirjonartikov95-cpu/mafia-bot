import telebot
from telebot import types
import random

# 1. BOT TOKENINGIZ TAYYOR
BOT_TOKEN = "8867209550:AAGU54ELxJDK9jwdil2uvITuqem2cZLjGjY"

# 2. ADMIN ID RAQAMINGIZ TO'G'RI JOYLASHDI ✅
ADMIN_ID = 7662509798  

bot = telebot.TeleBot(BOT_TOKEN)

# Foydalanuvchilar ma'lumotlar bazasi
user_data = {}

# O'yin holati va ishtirokchilar
game_players = []
player_roles = {}
game_started = False

# Do'kondagi buyumlar va ularning narxlari
SHOP_ITEMS = {
    "himoya": {"name": "🛡 Himoya", "price": 100, "currency": "money"},
    "hujjat": {"name": "📄 Hujjat", "price": 190, "currency": "money"},
    "ovoz_himoya": {"name": "⚖️ Ovozdan himoya", "price": 1, "currency": "diamonds"},
    "miltiq": {"name": "🔫 Miltiq", "price": 1, "currency": "diamonds"},
    "doridan_himoya": {"name": "💊 Doridan himoya", "price": 100, "currency": "money"},
    "maska": {"name": "🎭 Maska", "price": 100, "currency": "money"},
    "qotildan_himoya": {"name": "➕ Qotildan himoya", "price": 2, "currency": "diamonds"},
    "sirpanish_himoya": {"name": "🛹 Sirpanishdan himoya", "price": 300, "currency": "money"},
    "geroy_himoya": {"name": "🔰 Geroydan himoya", "price": 5, "currency": "diamonds"},
    "profil_almashish": {"name": "🔄 Profil almashish", "price": 5, "currency": "diamonds"},
    "geroy": {"name": "🌟 Geroy", "price": 90, "currency": "diamonds"}
}

# Rollar ro'yxati
ROLES_POOL = ["Minior 💎", "Joker 🃏", "Kimyogar 🧪", "Don 👑", "Komissar 🕵️‍♂️", "Shifokor ⛑", "Tinch aholi 🧑‍🌾"]

# Foydalanuvchini bazada tekshirish va yaratish
def check_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            "money": 1000, "diamonds": 10, "gold": 0,
            "himoya": 0, "hujjat": 1, "ovoz_himoya": 1, "miltiq": 1,
            "doridan_himoya": 0, "maska": 0, "qotildan_himoya": 0,
            "sirpanish_himoya": 4, "geroy_himoya": 0, "profil_almashish": 0, "geroy": 0,
            "wins": 80, "total_games": 696, "bought_role": None
        }

# Botga kirganda /start bosilganda
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    check_user(user_id)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_profile = types.KeyboardButton("👤 Profil")
    btn_shop = types.KeyboardButton("🛒 Do'kon")
    markup.add(btn_profile, btn_shop)
    
    bot.send_message(message.chat.id, "🔥 Elita Mafia uslubidagi botga xush kelibsiz! Quyidagi tugmalardan foydalaning:", reply_markup=markup)

# Profil va Do'kon tugmalari uchun xabarlarni tekshirish
@bot.message_handler(func=lambda message: message.text in ["👤 Profil", "🛒 Do'kon"])
def handle_text(message):
    user_id = message.from_user.id
    check_user(user_id)
    
    if message.text == "👤 Profil":
        u = user_data[user_id]
        if user_id == ADMIN_ID:
            money_txt, diam_txt, gold_txt = "♾ Cheksiz", "♾ Cheksiz", "♾ Cheksiz"
        else:
            money_txt, diam_txt, gold_txt = f"{u['money']}", f"{u['diamonds']}", f"{u['gold']}"
            
        role_txt = u['bought_role'] if u['bought_role'] else "Suidsid"
        
        profile_msg = (
            f"🕵️‍♂️ **Elita Mafia Bot**\n"
            f"👤 **{message.from_user.first_name}** {'(VIP BOSS)' if user_id == ADMIN_ID else ''}\n\n"
            f"💵 Dollar: {money_txt}\n"
            f"💎 Olmos: {diam_txt}\n"
            f"🪙 Oltin: {gold_txt}\n\n"
            f"🛡 Himoya: {u['himoya'] if user_id != ADMIN_ID else '♾'}\n"
            f"📄 Hujjat: {u['hujjat'] if user_id != ADMIN_ID else '♾'}\n"
            f"⚖️ Osishdan himoya qilinishi: {u['ovoz_himoya'] if user_id != ADMIN_ID else '♾'}\n"
            f"➕ Qotildan himoya: {u['qotildan_himoya'] if user_id != ADMIN_ID else '♾'}\n"
            f"🔫 Miltiq: {u['miltiq'] if user_id != ADMIN_ID else '♾'}\n"
            f"🪓 Doridan himoya: {u['doridan_himoya'] if user_id != ADMIN_ID else '♾'}\n"
            f"🎭 Maska: {u['maska'] if user_id != ADMIN_ID else '♾'}\n"
            f"🛹 Sirpanishdan himoya: {u['sirpanish_himoya'] if user_id != ADMIN_ID else '♾'}\n"
            f"🔰 Geroydan himoya: {u['geroy_himoya'] if user_id != ADMIN_ID else '♾'}\n\n"
            f"🎯 G'alaba: {u['wins'] if user_id != ADMIN_ID else '9999'}\n"
            f"🎲 Barcha o'yinlar: {u['total_games'] if user_id != ADMIN_ID else '9999'}\n\n"
            f"🎭 **Faol rollar:**\n1. {role_txt}\n2. {role_txt}"
        )
        bot.send_message(message.chat.id, profile_msg, parse_mode="Markdown")
        
    elif message.text == "🛒 Do'kon":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, item in SHOP_ITEMS.items():
            sym = "💵" if item['currency'] == "money" else "💎"
            btn = types.InlineKeyboardButton(f"{item['name']} - {item['price']}{sym}", callback_data=f"buy_{key}")
            markup.add(btn)
            
        bot.send_message(message.chat.id, "🛒 **DO'KON MENYUSI**\nSotib olmoqchi bo'lgan buyumingizni tanlang:", reply_markup=markup)

# Do'kondagi tugmalar bosilganda ishlaydigan qism
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def callback_buy(call):
    user_id = call.from_user.id
    check_user(user_id)
    item_key = call.data.replace("buy_", "")
    
    if item_key in SHOP_ITEMS:
        item = SHOP_ITEMS[item_key]
        price = item['price']
        currency = item['currency']
        
        if user_id != ADMIN_ID:
            if currency == "money" and user_data[user_id]['money'] < price:
                bot.answer_callback_query(call.id, "❌ Mablag'ingiz yetarli emas (Dollar kam)!")
                return
            elif currency == "diamonds" and user_data[user_id]['diamonds'] < price:
                bot.answer_callback_query(call.id, "❌ Olmoslaringiz yetarli emas!")
                return
            
            if currency == "money":
                user_data[user_id]['money'] -= price
            else:
                user_data[user_id]['diamonds'] -= price
        
        user_data[user_id][item_key] += 1
        bot.answer_callback_query(call.id, f"🎉 Muvaffaqiyatli sotib olindi: {item['name']}!")
        bot.send_message(call.message.chat.id, f"✅ Siz **{item['name']}** sotib oldingiz! Profilingizga qo'shildi.")

# ---- ⚙️ ADMIN BUYRUQLARI ----

@bot.message_handler(commands=['plus_pul'])
def add_money(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        target_id = int(args[1])
        amount = int(args[2])
        check_user(target_id)
        user_data[target_id]['money'] += amount
        bot.reply_to(message, f"✅ ID {target_id} hisobiga {amount}💵 muvaffaqiyatli qo'shildi!")
        bot.send_message(target_id, f"💰 Admin hisobingizga {amount}💵 dollar o'tkazdi!")
    except:
        bot.reply_to(message, "Format xato! `/plus_pul ID MIQDOR` deb yozing.")

@bot.message_handler(commands=['plus_olmos'])
def add_diamonds(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        target_id = int(args[1])
        amount = int(args[2])
        check_user(target_id)
        user_data[target_id]['diamonds'] += amount
        bot.reply_to(message, f"✅ ID {target_id} hisobiga {amount}💎 olmos muvaffaqiyatli qo'shildi!")
        bot.send_message(target_id, f"💎 Admin hisobingizga {amount}💎 olmos o'tkazdi!")
    except:
        bot.reply_to(message, "Format xato! `/plus_olmos ID MIQDOR` deb yozing.")

@bot.message_handler(commands=['plus_buyum'])
def add_item_admin(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        target_id = int(args[1])
        item_name = args[2].strip().lower()
        amount = int(args[3])
        
        if item_name in SHOP_ITEMS:
            check_user(target_id)
            user_data[target_id][item_name] += amount
            item_real_name = SHOP_ITEMS[item_name]['name']
            bot.reply_to(message, f"✅ ID {target_id} ga {amount} ta {item_real_name} muvaffaqiyatli tashlab berildi!")
            bot.send_message(target_id, f"🎁 Admin sizga {amount} ta **{item_real_name}** sovg'a qildi!", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Bunday buyum nomi do'konda yo'q!")
    except:
        bot.reply_to(message, "Format xato! `/plus_buyum ID BUYUM_NOMI MIQDOR` deb yozing.")

# O'yinchilar o'z pullarini o'tkazishi
@bot.message_handler(commands=['perevod'])
def transfer_money(message):
    user_id = message.from_user.id
    check_user(user_id)
    try:
        args = message.text.split()
        target_id = int(args[1])
        amount = int(args[2])
        if amount <= 0: return
        
        if user_id != ADMIN_ID and user_data[user_id]['money'] < amount:
            bot.reply_to(message, "❌ Balansingizda yetarli dollar yo'q!")
            return
            
        check_user(target_id)
        if user_id != ADMIN_ID: user_data[user_id]['money'] -= amount
        user_data[target_id]['money'] += amount
        bot.reply_to(message, f"✅ ID {target_id} ga {amount}💵 muvaffaqiyatli o'tkazildi!")
    except:
        bot.reply_to(message, "Format: `/perevod ID MIQDOR` ko'rinishida yozing.")

# O'yinni boshlash buyruqlari
@bot.message_handler(commands=['join'])
def join_game(message):
    global game_started
    user_id = message.from_user.id
    if game_started: return
    if user_id not in game_players:
        game_players.append(user_id)
        check_user(user_id)
        bot.reply_to(message, f"✅ O'yinga qo'shildingiz! (Jami: {len(game_players)} ta)")

@bot.message_handler(commands=['start_mafia'])
def start_mafia(message):
    global game_started, player_roles
    if message.from_user.id != ADMIN_ID: return
    if len(game_players) < 2: 
        bot.reply_to(message, "❌ O'yinni boshlash uchun kamida 2 ta odam /join orqali qo'shilishi kerak!")
        return
    
    game_started = True
  
