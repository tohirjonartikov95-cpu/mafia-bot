import telebot
from telebot import types
import random
import threading

BOT_TOKEN = "8867209550:AAGU54ELxJDK9jwdil2uvITuqem2cZLjGjY"
BOSS_ID = 7662509798  

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# O'yin o'zgaruvchilari
game_players = []     
player_roles = {}     
player_names = {}     
game_chat_id = None
game_started = False
game_mode = "NORMAL"  # "NORMAL", "ZOMBIE", "NOMZOD"
game_phase = "NIGHT"  

mafia_votes, mafia_voted = {}, set()
day_votes, day_voted = {}, set()

GOLD_PRICE = 5000  

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

# 38 TA REGLAMENT ROLLAR RO'YXATI
ROLES_REWARDS = {
    "Minior 💎": {"type": "diamonds", "amount": 6, "team": "CIVIL"},
    "Joker 🃏": {"type": "diamonds", "amount": 6, "team": "MAFIA"},
    "Kimyogar 🧪": {"type": "diamonds", "amount": 6, "team": "CIVIL"},
    "Yollanma qotil 🎯": {"type": "diamonds", "amount": 5, "team": "MAFIA"},
    "Konchi ⛏": {"type": "diamonds", "amount": 5, "team": "CIVIL"},
    "Admiral 🎖": {"type": "diamonds", "amount": 4, "team": "CIVIL"},
    "Sotqin 🎭": {"type": "diamonds", "amount": 4, "team": "MAFIA"},
    "Qorbobo ❄️": {"type": "diamonds", "amount": 4, "team": "CIVIL"},
    "Janob 🎩": {"type": "diamonds", "amount": 3, "team": "CIVIL"},
    "Sehrgar 🔮": {"type": "diamonds", "amount": 3, "team": "CIVIL"},
    "Komissar Katani 🕵️‍♂️": {"type": "diamonds", "amount": 2, "team": "CIVIL"},
    "Don 👑": {"type": "diamonds", "amount": 2, "team": "MAFIA"},
    "Qotil ⚔️": {"type": "diamonds", "amount": 2, "team": "MAFIA"},
    "Laborant 🥼": {"type": "diamonds", "amount": 2, "team": "CIVIL"},
    "Qaroqchi 🏴‍☠️": {"type": "diamonds", "amount": 2, "team": "MAFIA"},
    "G'azabkor 😡": {"type": "diamonds", "amount": 1, "team": "MAFIA"},
    "Mafia 🕶": {"type": "diamonds", "amount": 1, "team": "MAFIA"},
    "Serjant 👮‍♂️": {"type": "diamonds", "amount": 1, "team": "CIVIL"},
    "Aferist 🦊": {"type": "diamonds", "amount": 1, "team": "MAFIA"},
    "Tulki 🦧": {"type": "diamonds", "amount": 1, "team": "CIVIL"},
    "Fotoparatchi 📸": {"type": "diamonds", "amount": 1, "team": "CIVIL"},
    "Zombi 🧟‍♂️": {"type": "money", "amount": 1000, "team": "MAFIA"},
    "Robin Gud 🏹": {"type": "money", "amount": 1000, "team": "CIVIL"},
    "Doktor ⛑": {"type": "money", "amount": 1000, "team": "CIVIL"},
    "Kezuvchi 🚶‍♂️": {"type": "money", "amount": 500, "team": "CIVIL"},
    "Advokat 💼": {"type": "money", "amount": 500, "team": "CIVIL"},
    "Jurnalist 📰": {"type": "money", "amount": 500, "team": "CIVIL"},
    "Afsungar 🧙‍♂️": {"type": "money", "amount": 500, "team": "CIVIL"},
    "Bo'ri 🐺": {"type": "money", "amount": 500, "team": "MAFIA"},
    "Oshpaz 👨‍🍳": {"type": "money", "amount": 500, "team": "CIVIL"},
    "Hamshira 👩‍⚕️": {"type": "money", "amount": 400, "team": "CIVIL"},
    "Rais 👔": {"type": "money", "amount": 400, "team": "CIVIL"},
    "Daydi 🏕": {"type": "money", "amount": 400, "team": "CIVIL"},
    "Suidsid 💀": {"type": "money", "amount": 300, "team": "MAFIA"},
    "Ayg'oqchi 👁": {"type": "money", "amount": 300, "team": "MAFIA"},
    "Omadli 🍀": {"type": "money", "amount": 250, "team": "CIVIL"},
    "Tinch aholi 🧑‍🌾": {"type": "money", "amount": 100, "team": "CIVIL"},
    "Faol rolni o'chirish ❌": {"type": "money", "amount": 100, "team": "CIVIL"}
}

# Nomzod rejimi uchun maxfiy ismlar paketi
ANONYMOUS_NAMES = ["Agent X", "Niqobli Qotil", "Yashirin Soya", "Arvoh", "Tungi Ritsor", "Mantiqchi", "Detektiv", "Kiber Jangchi"]

def update_gold_course():
    global GOLD_PRICE
    GOLD_PRICE = random.randint(4600, 6009)

def check_user(user_id, username="O'yinchi"):
    if user_id not in user_data:
        user_data[user_id] = {
            "name": username, "money": 1000, "diamonds": 10, "gold": 0, "vip_days": 0,
            "himoya": 0, "hujjat": 1, "ovoz_himoya": 1, "miltiq": 1,
            "dori": 0, "maska": 0, "qotil_himoya": 0, "sirpanish": 4, "geroy": 0,
            "wins": 80, "total_games": 696, "bought_role": None
        }

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
    update_gold_course()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("👤 Profil"), types.KeyboardButton("🛒 Do'kon"))
    bot.send_message(message.chat.id, "🔥 Meystrik Mafia botiga xush kelibsiz!\n🎮 3 xil o'yin rejimi yoqildi! Faqat guruh adminlari start bera oladi.", reply_markup=markup)

@bot.message_handler(func=lambda msg: game_started and game_phase == "NIGHT" and msg.chat.id == game_chat_id)
def mute_night_chat(message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    if user_id == BOSS_ID or user_data[user_id]["vip_days"] > 0: return  
    try: bot.delete_message(message.chat.id, message.message_id)
    except: pass

@bot.message_handler(func=lambda msg: msg.text == "👤 Profil")
def show_profile(message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    u = user_data[user_id]
    m, d, g = ("♾ Cheksiz", "♾ Cheksiz", "♾ Cheksiz") if user_id == BOSS_ID else (f"{u['money']}", f"{u['diamonds']}", f"{u['gold']}")
    w, t = ("9999", "9999") if user_id == BOSS_ID else (f"{u['wins']}", f"{u['total_games']}")
    v_days = "UMRBOB ✨" if user_id == BOSS_ID else f"{u['vip_days']} kun"
    r_txt = u['bought_role'] if u['bought_role'] else "Suidsid"
    txt = (
        f"🕵️‍♂️ **Meystrik Mafia Bot**\n👤 Ism: **{u['name']}** {'(BOSS 👑)' if user_id == BOSS_ID else ''}\n"
        f"👑 VIP Unvon: **{v_days}**\n\n"
        f"💵 Dollar: {m}\n💎 Olmos: {d}\n🔶 Oltin: {g}\n\n"
        f"🛡 Himoya: {u['himoya']}\n📄 Hujjat: {u['hujjat']}\n"
        f"🎯 G'alaba: {w}\n🎲 Barcha o'yinlar: {t}\n\n"
        f"🎭 Faol rol: **{r_txt}**"
    )
    bot.send_message(message.chat.id, txt, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "🛒 Do'kon")
def show_shop(message):
    update_gold_course()
    markup = types.InlineKeyboardMarkup(row_width=1)
    for k, i in SHOP_ITEMS.items():
        s = "💵" if i['currency'] == "money" else "💎"
        markup.add(types.InlineKeyboardButton(f"{i['name']} - {i['price']}{s}", callback_data=f"buy_{k}"))
    markup.add(types.InlineKeyboardButton("👑 30 Kunlik Tungi VIP unvon — 30💎", callback_data="vip_30"))
    markup.add(types.InlineKeyboardButton(f"📈 Oltin sotib olish (1 ta = {GOLD_PRICE}💵)", callback_data="gold_buy"))
    markup.add(types.InlineKeyboardButton(f"📉 Oltin sotish (1 ta = {GOLD_PRICE}💵)", callback_data="gold_sell"))
    bot.send_message(message.chat.id, f"🛒 **MEYSTRIK MAFIA DO'KONI & BIRJASI**\n\n📊 Oltin Kursi: **1 🔶 = {GOLD_PRICE}💵**", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_") or call.data.startswith("vip_") or call.data in ["gold_buy", "gold_sell"])
def handle_callbacks(call):
    user_id = call.from_user.id
    check_user(user_id, call.from_user.first_name)
    u = user_data[user_id]
    if call.data.startswith("buy_"):
        k = call.data.replace("buy_", "")
        if k in SHOP_ITEMS:
            i = SHOP_ITEMS[k]
            if user_id != BOSS_ID:
                if i['currency'] == "money" and u['money'] < i['price']: return
                if i['currency'] == "diamonds" and u['diamonds'] < i['price']: return
                if i['currency'] == "money": u['money'] -= i['price']
                else: u['diamonds'] -= i['price']
            u[k] += 1
            bot.answer_callback_query(call.id, f"🎉 {i['name']} sotib olindi!", show_alert=True)
    elif call.data == "vip_30":
        if user_id != BOSS_ID and u['diamonds'] < 30: return
        if user_id != BOSS_ID: u['diamonds'] -= 30
        u['vip_days'] += 30
        bot.answer_callback_query(call.id, "👑 VIP unvon yoqildi!", show_alert=True)
    elif call.data == "gold_buy":
        if user_id != BOSS_ID and u['money'] < GOLD_PRICE: return
        if user_id != BOSS_ID: u['money'] -= GOLD_PRICE
        u['gold'] += 1
        bot.answer_callback_query(call.id, "🔶 Oltin xarid qilindi!", show_alert=True)
    elif call.data == "gold_sell":
        if user_id != BOSS_ID and u['gold'] < 1: return
        if user_id != BOSS_ID: u['gold'] -= 1
        u['money'] += GOLD_PRICE
        bot.answer_callback_query(call.id, "💰 Oltin sotildi!", show_alert=True)

@bot.message_handler(commands=['perevod', 'perevod_olmos'])
def transfer_res(message):
    user_id = message.from_user.id
    if not message.reply_to_message: return
    try:
        target_id = message.reply_to_message.from_user.id
        target_name = player_names.get(target_id, message.reply_to_message.from_user.first_name)
        amount = int(message.text.split())
        if amount <= 0 or user_id == target_id: return
        check_user(user_id)
        check_user(target_id, target_name)
        if "olmos" in message.text:
            if user_id != BOSS_ID and user_data[user_id]['diamonds'] < amount: return
