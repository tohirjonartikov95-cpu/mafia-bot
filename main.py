import telebot
from telebot import types
import random
import threading

BOT_TOKEN = "8867209550:AAGU54ELxJDK9jwdil2uvITuqem2cZLjGjY"

# 👑 FAQAT SIZ - ASOSIY YARATUVCHI (FAQAT SIZDA PUL BERISH HUQUQI VA CHEKSIZ BALANS BOR)
BOSS_ID = 7662509798  

# ⚙️ BU YERGA FAQAT O'YINNI BOSHLAY OLADIGAN DO'STLARINGIZ ID RAQAMLARINI VERGUL BILAN YOZING
ADMIN_LIST = [BOSS_ID] # Misol: [BOSS_ID, 1234567, 8910111] (boshida BOSS_ID tursin)

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# O'yin o'zgaruvchilari
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

MAFIA_TEAM = ["Don 👑", "Mafia 🕶", "Qotil ⚔️", "Yollanma qotil 🎯"]
CIVIL_TEAM = ["Komissar 🕵️‍♂️", "Shifokor ⛑", "Tinch aholi 🧑‍🌾", "Minior 💎", "Joker 🃏", "Kimyogar 🧪"]

def check_user(user_id, username="O'yinchi"):
    if user_id not in user_data:
        user_data[user_id] = {
            "name": username, "money": 1000, "diamonds": 10, "gold": 0,
            "wins": 0, "total_games": 0, "daily_wins": 0
        }
    else:
        if username != "O'yinchi": user_data[user_id]["name"] = username

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("👤 Profil"), types.KeyboardButton("🛒 Do'kon"))
    bot.send_message(message.chat.id, "🔥 Avtomatlashtirilgan Tun/Kun tizimli Elita Mafia botiga xush kelibsiz!\nReytinglar: /top yoki /kunlik_top", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "👤 Profil")
def show_profile(message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    u = user_data[user_id]
    
    # FAQAT SIZDA (BOSS_ID) BALANS CHEKSIZ KO'RINADI, DO'STLARINGIZDA ESA ODDIY BALANS BO'LADI
    if user_id == BOSS_ID:
        m, d = "♾ Cheksiz", "♾ Cheksiz"
    else:
        m, d = f"{u['money']}", f"{u['diamonds']}"
        
    status_tag = "(BOSS 👑)" if user_id == BOSS_ID else ("(ADMIN ⚙️)" if user_id in ADMIN_LIST else "")
    
    txt = f"🕵️‍♂️ Elita Mafia Bot\n👤 {u['name']} {status_tag}\n\n" \
          f"💵 Dollar: {m}\n💎 Olmos: {d}\n🏅 G'alaba: {u['wins']}\n🎲 Barcha o'yinlar: {u['total_games']}"
    bot.send_message(message.chat.id, txt, parse_mode="Markdown")

@bot.message_handler(commands=['top'])
def show_top_rating(message):
    if not user_data: return
    sorted_users = sorted(user_data.items(), key=lambda x: x['wins'], reverse=True)[:10]
    txt = "🏆 UMUMIY TOP REYTING 🏆\n\n"
    for idx, (uid, data) in enumerate(sorted_users):
        txt += f"{idx+1}. 👤 {data['name']} — {data['wins']} ta g'alaba\n"
    bot.send_message(message.chat.id, txt)

# ---- 🎲 O'YIN TIZIMI ----

@bot.message_handler(commands=['join'])
def join_game(message):
    global game_started
    if game_started: return
    p_id = message.from_user.id
    if p_id not in game_players:
        game_players.append(p_id)
        player_names[p_id] = message.from_user.first_name
        check_user(p_id, message.from_user.first_name)
        bot.reply_to(message, f"✅ O'yinga qo'shildingiz! (Jami: {len(game_players)} ta)")

# RO'YXATDAGI DO'STLARINGIZ O'YINNI BOSHLAY OLISHADI
@bot.message_handler(commands=['start_mafia'])
def start_mafia(message):
    global game_started, player_roles, game_chat_id
    if message.from_user.id not in ADMIN_LIST:
        bot.reply_to(message, "❌ Bu buyruqni faqat adminlar bera oladi!")
        return
    if len(game_players) < 3:
        bot.reply_to(message, "❌ Kamida 3 ta odam /join bosishi kerak!")
        return
    
    game_started = True
    game_chat_id = message.chat.id
    bot.send_message(game_chat_id, "🎲 O'yin boshlandi! Rollar lichkalarga yuborildi.")
    
    pool = ["Mafia 🕶", "Komissar 🕵️‍♂️"] + ["Tinch aholi 🧑‍🌾"] * (len(game_players) - 2)
    random.shuffle(pool)
    
    for i, p_id in enumerate(game_players):
        player_roles[p_id] = pool[i]
        user_data[p_id]['total_games'] += 1
        try: bot.send_message(p_id, f"🎭 Sizning yashirin rolingiz: {pool[i]}")
        except: pass
        
    start_night_phase()

def start_night_phase():
    global game_phase, mafia_votes, mafia_voted
    game_phase = "NIGHT"
    mafia_votes = {p: 0 for p in game_players}
    mafia_voted.clear()
    
    bot.send_message(game_chat_id, "🌌 SHAHARGA TUN KIRDI... 🌌\nMafiyalar uyg'onib lichkada o'z qurbonini tanlamoqda. (Vaqt: 30 soniya)")
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for p_id in game_players:
        markup.add(types.InlineKeyboardButton(f"🎯 {player_names[p_id]} ni o'ldirish", callback_data=f"kill_{p_id}"))
            
    for p_id in game_players:
        if player_roles[p_id] == "Mafia 🕶":
            try: bot.send_message(p_id, "🕶 Mafiya vaqti! Kimni o'ldirasiz?", reply_markup=markup)
            except: pass
            
    threading.Timer(30.0, end_night_and_start_day).start()

@bot.callback_query_handler(func=lambda call: call.data.startswith("kill_"))
def handle_mafia_kill(call):
    voter_id = call.from_user.id
    if player_roles.get(voter_id) != "Mafia 🕶" or voter_id in mafia_voted: return
    
    target_id = int(call.data.replace("kill_", ""))
    mafia_votes[target_id] += 1
    mafia_voted.add(voter_id)
    bot.answer_callback_query(call.id, "✅ Nishon belgilandi!")

def end_night_and_start_day():
    global game_players, game_phase
    if not game_started or game_phase != "NIGHT": return
    
    killed_id = max(mafia_votes, key=mafia_votes.get) if mafia_voted else None
    
    if killed_id and mafia_votes[killed_id] > 0:
        killed_name = player_names[killed_id]
        role = player_roles[killed_id]
        game_players.remove(killed_id)
        bot.send_message(game_chat_id, f"☀️ SHAHARGA KUN KIRDI! ☀️\n\n🌌 Kechasi o'ldirildi: {killed_name}! Uning roli {role} edi.")
    else:
        bot.send_message(game_chat_id, f"☀️ SHAHARGA KUN KIRDI! ☀️\n\n🌌 Bu tun hamma omon qoldi!")
        
    if check_game_over(): return
    start_day_voting()

def start_day_voting():
    global game_phase, day_votes, day_voted
    game_phase = "DAY"
    day_votes = {p: 0 for p in game_players}
    day_voted.clear()
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for p_id in game_players:
        markup.add(types.InlineKeyboardButton(f"🗳 {player_names[p_id]} ga ovoz berish", callback_data=f"dayvote_{p_id}"))
        
    bot.send_message(game_chat_id, "📢 KUNLIK OVOZ BERISH BOSHLANDI!\nKimni mafiya deb o'ylaysiz? (Vaqt: 30 soniya):", reply_markup=markup)
    threading.Timer(30.0, end_day_voting).start()

@bot.callback_query_handler(func=lambda call: call.data.startswith("dayvote_"))
def handle_day_vote(call):
    voter_id = call.from_user.id
    if voter_id not in game_players or voter_id in day_voted: return
    
    target_id = int(call.data.replace("dayvote_", ""))
    day_votes[target_id] += 1
    day_voted.add(voter_id)
    bot.answer_callback_query(call.id, "✅ Ovozingiz qabul qilindi!")

def end_day_voting():
    global game_players, game_phase
    if not game_started or game_phase != "DAY": return
    
    if day_voted:
        eliminated_id = max(day_votes, key=day_votes.get)
        eliminated_name = player_names[eliminated_id]
        role = player_roles[eliminated_id]
        game_players.remove(eliminated_id)
        bot.send_message(game_chat_id, f"🚨 Ovoz berish tugadi! {eliminated_name} osildi! Uning roli {role} edi.")
    else:
        bot.send_message(game_chat_id, "🚨 Ovoz berish tugadi! Hech kim osilmadi.")
        
    if check_game_over(): return
    start_night_phase()

def check_game_over():

global game_started
    mafias = [p for p in game_players if player_roles[p] == "Mafia 🕶"]
    civils = [p for p in game_players if player_roles[p] != "Mafia 🕶"]
    
    if len(mafias) == 0:
        end_game_with_rewards("CIVIL", "Tinch aholi 🧑‍🌾")
        return True
    elif len(mafias) >= len(civils):
        end_game_with_rewards("MAFIA", "Mafiya jamoasi 🕶")
        return True
    return False

def end_game_with_rewards(winner_team, team_name):
    global game_started
    winners = []
    
    for p_id in player_roles.keys():
        is_mafia = (player_roles[p_id] == "Mafia 🕶")
        if (winner_team == "CIVIL" and not is_mafia) or (winner_team == "MAFIA" and is_mafia):
            if p_id != BOSS_ID:7662509798
                user_data[p_id]['money'] += 30  # 30$ mukofot 💵
                user_data[p_id]['wins'] += 1
            winners.append(player_names[p_id])
            
    bot.send_message(game_chat_id, f"🏁 O'YIN YAKUNLANDI!\n\n🏆 G'olib jamoa: {team_name}\n🥇 30$ 💵 olganlar: {', '.join(winners)}\n\nHisoblar yangilandi! ✅")
    game_players.clear()
    player_roles.clear()
    game_started = False

# ---- 🛡 MUTLAQ INTEGRATSIYA QILINGAN FAQAT BOSS BUYRUQLARI ----
# Boshqa adminlar yoki o'yinchilar bu buyruqni yozishsa, bot ularga pul ham bermaydi, javob ham qaytarmaydi.

@bot.message_handler(commands=['plus_pul', 'plus_olmos'])
def add_res(message):
    if message.from_user.id != BOSS_ID:7662509798 return # Faqat sizga ruxsat beradi 👑
    try:
        args = message.text.split()
        tid, amt = int(args[1]), int(args[2])
        
        # O'ziga o'zi pul yozishni taqiqlash sharti (Admin do'stlaringiz va boshqalar uchun cheklov)
        if message.from_user.id != BOSS_ID:7662509798
            bot.reply_to(message, "❌ Sizda resurs tarqatish huquqi yo'q!")
            return
            
        check_user(tid)
        if "pul" in message.text:
            user_data[tid]['money'] += amt
            bot.reply_to(message, f"✅ ID {tid} ga {amt}💵 muvaffaqiyatli berildi.")
        else:
            user_data[tid]['diamonds'] += amt
