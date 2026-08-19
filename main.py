import telebot, random

BOT_TOKEN = "8867209550:AAGU54ELxJDK9jwdil2uvITuqem2cZLjGjY"
BOSS_ID = 7662509798  

bot = telebot.TeleBot(BOT_TOKEN)
user_data, game_players, player_roles, player_names = {}, [], {}, {}
game_chat_id, game_started, game_mode, game_phase = None, False, "NORMAL", "NIGHT"
mafia_votes, mafia_voted, day_votes, day_voted = {}, set(), {}, set()
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

ROLES_REWARDS = {
    "Minior 💎": {"type": "diamonds", "amount": 6, "team": "CIVIL"},
    "Joker 🃏": {"type": "diamonds", "amount": 6, "team": "MAFIA"},
    "Kimyogar 🧪": {"type": "diamonds", "amount": 6, "team": "CIVIL"},
    "Yollanma qotil 🎯": {"type": "diamonds", "amount": 5, "team": "MAFIA"},
    "Konchi ⛏": {"type": "diamonds", "amount": 5, "team": "CIVIL"},
    "Don 👑": {"type": "diamonds", "amount": 2, "team": "MAFIA"},
    "Qotil ⚔️": {"type": "diamonds", "amount": 2, "team": "MAFIA"},
    "Laborant 🥼": {"type": "diamonds", "amount": 2, "team": "CIVIL"},
    "Mafia 🕶": {"type": "diamonds", "amount": 1, "team": "MAFIA"},
    "Zombi 🧟‍♂️": {"type": "money", "amount": 1000, "team": "MAFIA"},
    "Robin Gud 🏹": {"type": "money", "amount": 1000, "team": "CIVIL"},
    "Doktor ⛑": {"type": "money", "amount": 1000, "team": "CIVIL"},
    "Kezuvchi 🚶‍♂️": {"type": "money", "amount": 500, "team": "CIVIL"},
    "Advokat 💼": {"type": "money", "amount": 500, "team": "CIVIL"},
    "Jurnalist 📰": {"type": "money", "amount": 500, "team": "CIVIL"},
    "Hamshira 👩‍⚕️": {"type": "money", "amount": 400, "team": "CIVIL"},
    "Suidsid 💀": {"type": "money", "amount": 300, "team": "MAFIA"},
    "Tinch aholi 🧑‍🌾": {"type": "money", "amount": 100, "team": "CIVIL"}
}

ANONYMOUS_NAMES = ["Agent X", "Niqobli Qotil", "Yashirin Soya", "Arvoh", "Tungi Ritsor", "Detektiv"]

def check_user(uid, name="O'yinchi"):
    if uid not in user_data:
        user_data[uid] = {
            "name": name, "money": 1000, "diamonds": 10, "gold": 0, "vip_days": 0,
            "himoya": 0, "hujjat": 1, "ovoz_himoya": 1, "miltiq": 1,
            "dori": 0, "maska": 0, "qotil_himoya": 0, "sirpanish": 4, "geroy": 0,
            "wins": 80, "total_games": 696, "bought_role": None
        }

def is_chat_admin(cid, uid):
    if uid == BOSS_ID: return True
    try:
        for a in bot.get_chat_administrators(cid):
            if a.user.id == uid: return True
    except: pass
    return False

@bot.message_handler(commands=['start'])
def start_cmd(message):
    uid = message.from_user.id
    check_user(uid, message.from_user.first_name)
    global GOLD_PRICE
    GOLD_PRICE = random.randint(4600, 6009)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("👤 Profil"), types.KeyboardButton("🛒 Do'kon"))
    bot.send_message(message.chat.id, f"🔥 Meystrik Mafia botiga xush kelibsiz, {message.from_user.first_name}!", reply_markup=markup)

@bot.message_handler(func=lambda msg: game_started and game_phase == "NIGHT" and msg.chat.id == game_chat_id)
def mute_night_chat(message):
    uid = message.from_user.id
    check_user(uid, message.from_user.first_name)
    if uid == BOSS_ID or user_data[uid]["vip_days"] > 0: return  
    try: bot.delete_message(message.chat.id, message.message_id)
    except: pass

@bot.message_handler(func=lambda msg: msg.text == "👤 Profil")
def show_profile(message):
    uid = message.from_user.id
    check_user(uid, message.from_user.first_name)
    u = user_data[uid]
    m = "Cheksiz" if uid == BOSS_ID else f"{u['money']}"
    d = "Cheksiz" if uid == BOSS_ID else f"{u['diamonds']}"
    g = "Cheksiz" if uid == BOSS_ID else f"{u['gold']}"
    w = "9999" if uid == BOSS_ID else f"{u['wins']}"
    t = "9999" if uid == BOSS_ID else f"{u['total_games']}"
    v = "UMRBOB ✨" if uid == BOSS_ID else f"{u['vip_days']} kun"
    txt = f"🕵️‍♂️ **Meystrik Mafia Bot**\n👤 Ism: **{u['name']}**\n👑 VIP Unvon: **{v}**\n\n💵 Dollar: {m}\n💎 Olmos: {d}\n🔶 Oltin: {g}\n\n🏅 G'alaba: {w}\n🎲 Jami: {t}"
    bot.send_message(message.chat.id, txt, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "🛒 Do'kon")
def show_shop(message):
    global GOLD_PRICE
    GOLD_PRICE = random.randint(4600, 6009)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for k, i in SHOP_ITEMS.items():
        s = "💵" if i['currency'] == "money" else "💎"
        markup.add(types.InlineKeyboardButton(f"{i['name']} - {i['price']}{s}", callback_data=f"buy_{k}"))
    markup.add(types.InlineKeyboardButton("👑 Tungi VIP unvon — 30💎", callback_data="vip_30"))
    markup.add(types.InlineKeyboardButton(f"📈 Oltin sotib olish ({GOLD_PRICE}💵)", callback_data="gold_buy"))
    markup.add(types.InlineKeyboardButton(f"📉 Oltin sotish ({GOLD_PRICE}💵)", callback_data="gold_sell"))
    bot.send_message(message.chat.id, f"🛒 **DO'KON & BIRJA**\n\n📊 Oltin Kursi: **1 🔶 = {GOLD_PRICE}💵**", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_") or call.data.startswith("vip_") or call.data in ["gold_buy", "gold_sell"])
def handle_callbacks(call):
    uid = call.from_user.id
    check_user(uid, call.from_user.first_name)
    u = user_data[uid]
    if call.data.startswith("buy_"):
        k = call.data.replace("buy_", "")
        if k in SHOP_ITEMS:
            i = SHOP_ITEMS[k]
            if uid != BOSS_ID:
                if i['currency'] == "money" and u['money'] < i['price']: return
                if i['currency'] == "diamonds" and u['diamonds'] < i['price']: return
                if i['currency'] == "money": u['money'] -= i['price']
                else: u['diamonds'] -= i['price']
            u[k] += 1
            bot.answer_callback_query(call.id, "🎉 Sotib olindi!")
    elif call.data == "vip_30":
        if uid != BOSS_ID and u['diamonds'] < 30: return
        if uid != BOSS_ID: u['diamonds'] -= 30
        u['vip_days'] += 30
        bot.answer_callback_query(call.id, "👑 VIP yoqildi!")
    elif call.data == "gold_buy":
        if uid != BOSS_ID and u['money'] < GOLD_PRICE: return
        if uid != BOSS_ID: u['money'] -= GOLD_PRICE
        u['gold'] += 1
        bot.answer_callback_query(call.id, "🔶 Oltin olindi!")
    elif call.data == "gold_sell":
        if uid != BOSS_ID and u['gold'] < 1: return
        if uid != BOSS_ID: u['gold'] -= 1
        u['money'] += GOLD_PRICE
        bot.answer_callback_query(call.id, "💰 Oltin sotildi!")

@bot.message_handler(commands=['perevod', 'perevod_olmos'])
def transfer_res(message):
    uid = message.from_user.id
    if not message.reply_to_message: return
    try:
        tid = message.reply_to_message.from_user.id
        tname = player_names.get(tid, message.reply_to_message.from_user.first_name)
        amt = int(message.text.split()[1])
        if amt <= 0 or uid == tid: return
        check_user(uid)
        check_user(tid, tname)
        if "olmos" in message.text:
            if uid != BOSS_ID and user_data[uid]['diamonds'] < amt: return
            if uid != BOSS_ID: user_data[uid]['diamonds'] -= amt
            user_data[tid]['diamonds'] += amt
        else:
            if uid != BOSS_ID and user_data[uid]['money'] < amt: return
            if uid != BOSS_ID: user_data[uid]['money'] -= amt
            user_data[tid]['money'] += amt
        bot.reply_to(message, f"✅ {amt} o'tkazildi!")
    except: pass

@bot.message_handler(commands=['plus_pul', 'plus_olmos'])
def add_res_reply(message):
    if message.from_user.id != BOSS_ID or not message.reply_to_message: return
    try:
        tid = message.reply_to_message.from_user.id
        tname = player_names.get(tid, message.reply_to_message.from_user.first_name)
        amt = int(message.text.split()[1])
        check_user(tid, tname)
        if "pul" in message.text: user_data[tid]['money'] += amt
        else: user_data[tid]['diamonds'] += amt
        bot.reply_to(message, f"✅ {amt} berildi!")
    except: pass

@bot.message_handler(commands=['top'])
def show_top(message):
    if not user_data: return
    su = sorted(user_data.items(), key=lambda x: x['wins'], reverse=True)[:10]
    txt = "🏆 **TOP REYTING** 🏆\n\n"
    for idx, (uid, data) in enumerate(su): txt += f"{idx+1}. 👤 {data['name']} — {data['wins']} ta\n"
    bot.send_message(message.chat.id, txt)

@bot.message_handler(commands=['join'])
def join_game(message):
    if game_started: return
    pid = message.from_user.id
    check_user(pid, message.from_user.first_name)
    if pid not in game_players:
        game_players.append(pid)
        player_names[pid] = user_data[pid]['name']
        bot.reply_to(message, f"✅ Qo'shildi! (Jami: {len(game_players)})")

def setup_and_start_game(message, mode):
    global game_started, player_roles, game_chat_id, game_mode, player_names
    if not is_chat_admin(message.chat.id, message.from_user.id) or len(game_players) < 3: return
    game_started, game_mode, game_chat_id = True, mode, message.chat.id
    if game_mode == "NOMZOD":
        for i, pid in enumerate(game_players):
            if i < len(ANONYMOUS_NAMES): player_names[pid] = ANONYMOUS_NAMES[i]
    if game_mode != "NOMZOD":
        for pid in game_players: player_names[pid] = user_data[pid]['name']
    if game_mode == "ZOMBIE":
        
