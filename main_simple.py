from flask import Flask, request
import os
import json
import gspread
from google.oauth2.service_account import Credentials 
from telebot import TeleBot, types

# استخدام البوت token مباشرة
BOT_TOKEN = "8142209161:AAHP5OYE83laIzLsmB6i_XvlSkmv2zTx9QU"
bot = TeleBot(BOT_TOKEN, parse_mode="HTML")
ADMIN_ID = 1437951187

# Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# استخدام ملف JSON مباشرة
try:
    with open("my-project-bot-8163-56c4aa024bd9.json") as f:
        service_account_info = json.load(f)
    
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    client = gspread.authorize(creds)
    
    spreadsheet = client.open("BotCodes")
    codes_sheet = spreadsheet.worksheet('codes')
    user_codes_sheet = spreadsheet.worksheet("user_codes")
    
    print("✅ Google Sheets connected successfully!")
    
except Exception as e:
    print(f"❌ Google Sheets connection failed: {e}")
    print("⚠️ Bot will work without Google Sheets functionality")
    codes_sheet = None
    user_codes_sheet = None

# ids فيديوهات الشرح
IPWEB_VIDEO_ID ="BAACAgQAAxkBAAJjqWjQK8sN5cIQrLyjN2gpq7SoIWM9AAIWGAACwDqAUkXqZzQMc_wCNgQ"
UNU_VIDEO_ID="BAACAgQAAxkBAAJjsWjQN6-gp6cHUDqtoTy9eaM_eGFbAAJnGgACwDqIUvjrkxy8WenUNgQ"
VKSURF_VIDEO1_ID ="BAACAgQAAxkBAAJjwWjQPSlrXJGrDF_vuYkampvYFe3fAAJxGgACwDqIUhFRzD1SdXZ6NgQ"
VKSURF_VIDEO2_ID ="BAACAgQAAxkBAAICJmiWExCvmaj6n1tmXv5KouCmlM-5AALkGAACtASxUCKwgsEkVWRANgQ"
VKTARGET_VIDEO_ID="BAACAgQAAxkBAAIDQGiWJYziEa26A3UWuMIUIM1P7j11AAL3GAACtASxUPigHKj4jsxtNgQ"
AVISO_VIDEO1_ID="BAACAgQAAxkBAAIDZWiWM3omtWH6PorUyopZ50-OW5AuAALPHgACAVyxUM9nQkSbJYnpNgQ"
AVISO_VIDEO2_ID="BAACAgQAAxkBAAIDZ2iWNnDL-sxlAwsSg9C1m2_0CKVbAALTHgACAVyxUAo8sTdQH2I1NgQ"

# ids فيديوهات السحب
IPWEB_ID="BAACAgQAAxkBAAJjr2jQMRhPl5SKpnkU9CnA9wKdrOCVAAI3GAACwDqAUmltTXOuNuikNgQ"
UNU_ID="BAACAgQAAxkBAAJjtWjQOlBG0LT81tlojqJNS044iJxcAAJtGgACwDqIUuv03viL7exXNgQ"
VKSURF_ID1="BAACAgQAAxkBAAJjxWjQQd51QAJv8oVCWJiDesjKOcyRAAKCGgACwDqIUpitJaPPqV7PNgQ"
VKSURF_ID2="AgACAgQAAxkBAAIFW2iXLfnU6MnBIiZ6mr5EI5VRe9miAAKwzDEbAVy5UKfH3jNJ-Q-XAQADAgADeAADNgQ"
VKTARGET_ID="BAACAgQAAxkBAAIFOWiXAAHyPxby1YNK6y2nEQLojL375QACvRwAAgFcuVABVg1-_14qOTYE"
AVISO_ID1="BAACAgQAAxkBAAIFN2iXAAFJ7GsoaiKKWgbXxVvoV7FWiAACvBwAAgFcuVBjVJlZcVPe3DYE"

# ✅ القائمة الرئيسية
def main_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row("Start")
    menu.row("أكواد", "مواقع")
    menu.row("السحب", "القبض")
    return menu

# أمر إضافة أكواد (للأدمن فقط)
@bot.message_handler(commands=['addcodes'])
def add_codes(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "أرسل الأكواد (كل كود في سطر جديد):")
        bot.register_next_step_handler(message, save_codes)
    else:
        bot.send_message(message.chat.id, "❌ أنت لست الأدمن!")

def save_codes(message):
    if codes_sheet:
        codes = message.text.strip().split('\n')
        for code in codes:
            codes_sheet.append_row([code.strip()])
        bot.send_message(message.chat.id, f"✅ تم إضافة {len(codes)} الأكواد بنجاح.")
    else:
        bot.send_message(message.chat.id, "❌ Google Sheets غير متصل!")

# ✅ قائمة المواقع الفرعية
def sites_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row("🔹 IP Web", "🔹 Aviso")
    menu.row("�� VK Target", "🔹 UNU")
    menu.row("🔹 VK Surfing")
    menu.row("↩️ رجوع")
    return menu

# ✅ قائمة المواقع الفرعية (نسخة 2)
def sites_menu2():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row("🌐 IP Web", "🌐 Aviso")
    menu.row("🌐 VK Target", "🌐 UNU")
    menu.row("�� VK Surfing")
    menu.row("↩️ رجوع")
    return menu

# ✅ لما حد يعمل /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
       "👋 أهلاً بيك في بوت E' Make Money\n\nاختر من القائمة اللي تحت علشان تبدأ 💰👇",
        reply_markup=main_menu()
    )

# ✅ التعامل مع الرسائل النصية
@bot.message_handler(func=lambda m: m.content_type == 'text')
def handle_message(message):
    text = message.text

    if text == "Start":
        bot.send_message(
            message.chat.id,
            "👋 أهلاً بيك في بوت E' Make Money\n\nاختر من القائمة اللي تحت علشان تبدأ 💰👇",
            reply_markup=main_menu()
        )

    elif text == "القبض":
        bot.send_message(
            message.chat.id,
            """📸 لضمان قبول الشغل، يُرجى اتباع الخطوات التالية بدقة:

1️⃣ بعد الانتهاء من فديوهات السحب، لازم تبعت سكرين شوت يوضح إن النقاط اتحسبت (مكتوب فيها إن العملية مقبولة "مدفوعه")

2️⃣ ابعت السكرين مع رسالة فيها:
🔹 اسم الموقع اللي اشتغلت عليه  
🔹 الكود الخاص بيك  
🔹 الكاش اللي هتستلم عليه الفلوس  

3️⃣ ابعت كل ده على واتساب على الرقم ده 👇  
📱 <a href='https://wa.me/201040311607'>راسل Eslam على WhatsApp</a>

📌 أقل عدد نقاط مسموح بتسليمه حسب الموقع:

🌐 موقع VK Surfing: أقل عدد تسليم 106 نقطة  
🌐 مواقع IP Web - Aviso - VK Target - UNU: أقل عدد تسليم 50 نقطة  

⛔ أي تسليم أقل من الأرقام دي مش هيتحسب، فـ تأكد قبل ما تبعت.

🕒 التسليم متاح من يوم الجمعة لحد السبت، وبيوصلك سكرين إن الفلوس وصلت خلال 24 ساعة كحد أقصى.
""",
            reply_markup=main_menu(),
            disable_web_page_preview=True
        )
    
    elif message.text.strip() == "أكواد":
        if not codes_sheet:
            bot.send_message(message.chat.id, "❌ Google Sheets غير متصل!")
            return
            
        user_id = str(message.from_user.id)

        # نبحث عن اليوزر في شيت user_codes
        user_codes_data = user_codes_sheet.get_all_values()
        existing_user = None
        for row in user_codes_data:
            if row[0] == user_id:
                existing_user = row[1]
                break

        if existing_user:
            bot.send_message(message.chat.id, f"📌 لقد حصلت على الكود من قبل: {existing_user}")

        elif len(codes_sheet.get_all_values()) == 0:
            bot.send_message(message.chat.id, "❌ لا توجد أكواد متاحة الآن.")

        else:
            codes_data = codes_sheet.get_all_values()
            code = codes_data[0][0]

            bot.send_message(message.chat.id, f"🎁 كودك هو: {code}")
            user_codes_sheet.append_row([user_id, code])
            codes_sheet.delete_rows(1)

    elif text == "السحب":
       bot.send_message(
        message.chat.id,
        "🌐 فيديوهات السحب :",
        reply_markup=sites_menu2()
    )
    elif text == "مواقع":
        bot.send_message(
            message.chat.id,
            "🌐 اختار الموقع اللي اشتغلت عليه:",
            reply_markup=sites_menu()
        )

    elif text == "↩️ رجوع":
        bot.send_message(
            message.chat.id,
            "✅ رجعتك للقائمة الرئيسية 💡",
            reply_markup=main_menu()
        )
    elif text == "🔹 IP Web":
     if IPWEB_VIDEO_ID:
        bot.send_video(
            message.chat.id,
            IPWEB_VIDEO_ID,
            caption=(
                "شغل موقع ipweb 👇🏼\n\n"
                "https://www.ipweb.pro/?Vvvvvv6556\n\n"
                "الشغل عباره عن انك بتعمل متابعه لناس / بتدخل جروب / لايك وبتبعت سكرين.\n"
                "ابعتوا لاسلام عشان تستلموا الكود و تفعلوا الاكونت وابدأو شغل لغاية ما الكود يتبعت.\n"
                "اهم حاجة وأنت بتسجل تخش من اللينك الي موجود فوق ده عشان القبض 👆\n\n"
                "ده بوت الخاص بالموقع، تقدر تشتغل عليه برضو، اهم حاجة تسجل بنفس اليوزر والباسورد بتوع الموقع 👇\n"
                "https://t.me/IPwebBot?start=bT1zbCZyPVZ2dnZ2djY1NTY\n\n"
                "🎥 الفيديو موضح كل حاجة بالتفاصيل 👆🏼"
            )
        )
        bot.send_photo(
            message.chat.id,
            "AgACAgQAAxkBAAJkNWjQRnpBnqBQnfPNGphWPkWJtsswAAJNyzEbwDqIUi6hXF123lfuAQADAgADeQADNgQ",
            caption="ده كده شكل الاسكرين اللي مفرود تبعتهالي برايفت ساعه القبض ياريت تكون مترتبه والبينات صحيحه عشان القبض ميتأخرش او يحصل مشكله ❤️"
        )

        bot.send_message(
           message.chat.id,
           "السعر:\n"
           "ال110 نقطه ب 38 جنيه\n"
           "الليدر ب 39"
        )
     else:
        bot.send_message(message.chat.id, "⚠️ لسه مفيش فيديو مضاف، ارفعيه كملف الأول.")

    # باقي الكود...
    else:
        bot.send_message(
            message.chat.id,
            "❗مش فاهم الطلب، اختار من القايمة تحت 🙏",
            reply_markup=main_menu()
        )

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/api', methods=['GET', 'HEAD'])
def api():
    return {"status": "ok", "message": "Telegram Bot API is running"}, 200

@app.route("/webhook", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# ✅ Setup for Replit environment
if __name__ == "__main__":
    # Get domain from Replit environment or fallback
    replit_domain = os.environ.get("REPLIT_DEV_DOMAIN")
    webhook_url = os.environ.get("WEBHOOK_URL")
    
    if replit_domain:
        webhook_url = f"https://{replit_domain}/webhook"
    elif webhook_url:
        webhook_url = f"{webhook_url}/webhook"
    
    if webhook_url:
        print("Setting webhook URL...")
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        print("Webhook configured successfully")
    else:
        print("No webhook URL configured - running in polling mode")
        # For development, you can use polling instead
        # bot.polling(none_stop=True)
    
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask app on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
