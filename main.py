import telebot
from telebot import types
import random
import threading

BOT_TOKEN = "8867209550:AAGU54ELxJDK9jwdil2uvITuqem2cZLjGjY"
BOSS_ID = 7662509798  # ASOSIY BOSS (FAQAT SIZDA TEKIN PUL BERISH HUQUQI BOR) 👑

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}
game_players = []     
player_roles = {}     
player_names = {}     
game_chat_id = None
game_started = False
game_phase = "NIGHT"  

mafia_votes = {}      
mafia_voted = set()   
day_votes = {}        
day_voted = set()     

SHOP_ITEMS = {
    "himoya": {"name": "🛡 Himoya", "price": 100, "currency": "money"},
    "hujjat": {"name": "📄 Hujjat", "price": 190, "currency": "money"},
    "ovoz_himoya": {"name": "⚖️ Ovozdan himoya", "price": 1, "currency": "diamonds"},
    "miltiq": {"name": "🔫 Miltiq", "price": 1, "currency": "diamonds"},
    "dori": {"name": "💊 Doridan himoya", "price": 100, "currency": "money"},
    "maska": {"name": "🎭 Maska", "price": 100, "currency": "money"},
    "qotil_himoya": {"name": "➕ Qotildan himoya", "price": 2, "currency": "diamonds"},
    "sirpanish": {"name": "🛹 Sirpanishdan himoya", "price": 300, "currency": "money"},
    "geroy": {"name": "🔰 Geroydan himoya", "price": 5, "currency": "diamonds"}
}

MAFIA_TEAM = ["Don 👑", "Mafia 🕶", "Qotil ⚔️", "Yollanma qotil 🎯"]
CIVIL_TEAM = ["Komissar 🕵️‍♂️", "Shifokor ⛑", "Tinch aholi 🧑‍🌾", "Minior 💎", "Joker 🃏", "Kimyogar 🧪"]
ROLES_POOL = ["Minior 💎", "Joker 🃏", "Kimyogar 🧪", "Don 👑", "Komissar 🕵️‍♂️", "Shifokor ⛑", "Tinch aholi 🧑‍🌾"]

def check_user(user_id, username="O'yinchi"):
    if user_id not in user_data:
        user_data[user_id] = {
            "name": username, "money": 1000, "diamonds": 10, "gold": 0,
            "himoya": 0, "hujjat": 1, "ovoz_himoya": 1, "miltiq": 1,
            "dori": 0, "maska": 0, "qotil_himoya": 0, "sirpanish": 4, "geroy": 0,
            "wins": 80, "total_games": 696, "bought_role": None
        }
    else:
        if username != "O'yinchi": user_data[user_id]["name"] = username

def is_chat_admin(chat_id, user_id):
    if user_id == BOSS_ID: return True
    try:
        admins = bot.get_chat_administrators(chat_id)
        for admin in admins:
            if admin.user.id == user_id: return True
        return False
    except: return False

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("👤 Profil"), types.KeyboardButton("🛒 Do'kon"))
    bot.send_message(message.chat.id, "🔥 Avtomatlashtirilgan Meystrik Mafia botiga xush kelibsiz!\n\n💡 Pul o'tkazish uchun do'stingiz xabariga REPLI (javob) qilib /perevod [MIQDOR] deb yozing!", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "👤 Profil")
def show_profile(message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    u = user_data[user_id]
    
    if user_id == BOSS_ID:
        m, d, g, inf = "♾ Cheksiz", "♾ Cheksiz", "♾ Cheksiz", "♾"
        w, t = "9999", "9999"
    else:
        m, d, g, inf = f"{u['money']}", f"{u['diamonds']}", f"{u['gold']}", None
        w, t = f"{u['wins']}", f"{u['total_games']}"
        
    r_txt = u['bought_role'] if u['bought_role'] else "Suidsid"
    is_admin = is_chat_admin(message.chat.id, user_id)
    status_tag = "(BOSS 👑)" if user_id == BOSS_ID else ("(ADMIN ⚙️)" if is_admin else "")
    
    txt = (
        f"🕵️‍♂️ **Meystrik Mafia Bot**\n👤 **{u['name']}** {status_tag}\n\n"
        f"💵 Dollar: {m}\n💎 Olmos: {d}\n🪙 Oltin: {g}\n\n"
        f"🛡 Himoya: {inf if inf else u['himoya']}\n📄 Hujjat: {inf if inf else u['hujjat']}\n"
        f"⚖️ Osishdan himoya: {inf if inf else u['ovoz_himoya']}\n➕ Qotildan himoya: {inf if inf else u['qotil_himoya']}\n"
        f"🔫 Miltiq: {inf if inf else u['miltiq']}\n🪓 Doridan himoya: {inf if inf else u['dori']}\n"
        f"🎭 Maska: {inf if inf else u['maska']}\n🛹 Sirpanishdan himoya: {inf if inf else u['sirpanish']}\n"
        f"🔰 Geroydan himoya: {inf if inf else u['geroy']}\n\n"
        f"🎯 G'alaba: {w}\n🎲 Barcha o'yinlar: {t}\n\n"
        f"🎭 **Faol rollar:**\n1. {r_txt}\n2. {r_txt}"
    )
    bot.send_message(message.chat.id, txt, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "🛒 Do'kon")
def show_shop(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for k, i in SHOP_ITEMS.items():
        s = "💵" if i['currency'] == "money" else "💎"
        markup.add(types.InlineKeyboardButton(f"{i['name']} - {i['price']}{s}", callback_data=f"buy_{k}"))
    bot.send_message(message.chat.id, "🛒 **MEYSTRIK MAFIA DO'KONI**\nBuyumni tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def callback_buy(call):
    user_id = call.from_user.id
    check_user(user_id, call.from_user.first_name)
    k = call.data.replace("buy_", "")
    if k in SHOP_ITEMS:
        i = SHOP_ITEMS[k]
        if user_id != BOSS_ID:
            if i['currency'] == "money" and user_data[user_id]['money'] < i['price']:
                bot.answer_callback_query(call.id, "❌ Mablag'ingiz yetarli emas!", show_alert=True)
                return
            elif i['currency'] == "diamonds" and user_data[user_id]['diamonds'] < i['price']:
                bot.answer_callback_query(call.id, "❌ Olmoslaringiz yetarli emas!", show_alert=True)
                return
            if i['currency'] == "money": user_data[user_id]['money'] -= i['price']
            else: user_data[user_id]['diamonds'] -= i['price']
        user_data[user_id][k] += 1
        bot.answer_callback_query(call.id, f"🎉 {i['name']} muvaffaqiyatli sotib olindi!", show_alert=True)

# ---- 💸 REPLI (REPLY) ORQALI ID-RAQAMSIZ PUL VA OLMOS O'TKAZISH TIZIMI ----

@bot.message_handler(commands=['perevod'])
def transfer_money(message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    
    # Agar xabarga reply qilinmagan bo'lsa ogohlantirish
    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ ID raqamsiz o'tkazish uchun do'stingizning xabariga Reply (javob) qilib yozing!")
        return
        
    try:
        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name
        amount = int(message.text.split()[1])
        
        if amount <= 0 or user_id == target_id: return
        
        if user_id != BOSS_ID and user_data[user_id]['money'] < amount:
            bot.reply_to(message, "❌ Balansingizda yetarli dollar yo'q!")
            return
            
        check_user(target_id, target_name)
        if user_id != BOSS_ID: user_data[user_id]['money'] -= amount
        user_data[target_id]['money'] += amount
        bot.reply_to(message, f"✅ {target_name} hisobiga {amount}💵 muvaffaqiyatli o'tkazildi!")
    except:
        bot.reply_to(message, "Format xato! Shunchaki `/perevod [MIQDOR]` deb yozing.")

@bot.message_handler(commands=['perevod_olmos'])
def transfer_diamonds(message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    
    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ Olmos o'tkazish uchun do'stingizning xabariga Reply (javob) qilib yozing!")
        return
        
    try:
        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name
        amount = int(message.text.split()[1])
        
        if amount <= 0 or user_id == target_id: return
        
        if user_id != BOSS_ID and user_data[user_id]['diamonds'] < amount:
            bot.reply_to(message, "❌ Balansingizda yetarli olmos yo'q!")
            return
            
        check_user(target_id, target_name)
        if user_id != BOSS_ID: user_data[user_id]['diamonds'] -= amount
        user_data[target_id]['diamonds'] += amount
        bot.reply_to(message, f"✅ {target_name} hisobiga {amount}💎 olmos muvaffaqiyatli o'tkazildi!")
    except:
        bot.reply_to(message, "Format xato! Shunchaki `/perevod_olmos [MIQDOR]` deb yozing.")

# ---- 👑 FAQAT BOSS UCHUN REPLI ORQALI TEKIN RESURS SOVG'A QILISH BUYRUQLARI ----

@bot.message_handler(commands=['plus_pul', 'plus_olmos'])
def add_res_reply(message):
    if message.from_user.id != BOSS_ID: return
    if not message.reply_to_message:
        bot.reply_to(message, "👑 Boss, tekin resurs berish uchun o'yinchining xabariga Reply qilib buyruqni bering!")
        return
    try:
        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name
        amt = int(message.text.split()[1])
        check_user(target_id, target_name)
        
        if "pul" in message.text:
            user_data[target_id]['money'] += amt
            bot.reply_to(message, f"✅ Boss tomonidan {target_name} hisobiga {amt}💵 tekin dollar sovg'a qilindi!")
        else:
            user_data[target_id]['diamonds'] += amt
            bot.reply_to(message, f"✅ Boss tomonidan {target_name} hisobiga {amt}💎 tekin olmos sovg'a qilindi!")
    except:
        bot.reply_to(message, "Format: `/plus_pul [MIQDOR]`")

# ----------------------------------------------------------------

@bot.message_handler(commands=['top'])
def show_top_rating(message):
    if not user_data: return
    sorted_users = sorted(user_data.items(), key=lambda x: x['wins'], reverse=True)[:10]
    txt = "🏆 **MEYSTRIK MAFIA - TOP REYTING** 🏆\n\n"
    for idx, (uid, data) in enumerate(sorted_users):
        txt += f"{idx+1}. 👤 {data['name']} — {data['wins']} ta g'alaba\n"
    bot.send_message(message.chat.id, txt)

@bot.message_handler(commands=['join'])
def join_game(message):
    global game_started
    if game_started: return
    p_id = message.from_user.id
    if p_id not in game_players:
      
