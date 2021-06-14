from telebot import types, TeleBot
from gtts import gTTS
import config
import telebot
import translatorall
users = {}
bot = TeleBot(config.token)
fulltext = "Assalomu alaykum <b>{}</b>!"
fulltext += "\nUshbu Botda siz o`z matnlaringizni \n<b>{}</b>\n tillarga tarjima qilib olishingiz mumkin."
fulltext += "\nMatnni yuboring va uni yuqoridagi tillarning biriga  tarjima qilib oling\nTilni o`zgartirish uchun  👉 /change 👈 buyrug`ini yuboring."
markup = types.InlineKeyboardMarkup(row_width = 2)
tillar = ""
for lang in config.languages.keys():
	tillar += f"{lang},"
	markup.add(types.InlineKeyboardButton(text = lang ,callback_data = config.languages[lang]))
@bot.message_handler(commands = ['start'])
def start(msg):
	id = msg.from_user.id
	users[str(id)] = 'uz'
	bot.send_message(id , fulltext.format(msg.from_user.first_name, tillar),parse_mode = 'html')
@bot.message_handler(commands = ['change'])
def change(msg):
	id = msg.from_user.id
	try:
		global first
		first = bot.send_message(id , "Tanlang👇🏻",reply_markup =markup)
	except:
		bot.send_message(id , " 👉 /start 👈 ")
@bot.message_handler(content_types = ['text'])
def text(msg):
	id = msg.from_user.id
	try:
		global configlang
		text = translatorall.translatornew(msg.text , users[str(id)])
		try:
			tts = gTTS(text, lang=users[str(id)])
		except:
			tts = gTTS(text)
		tts.save(f'@{bot.get_me().username}.mp3')
		audio = open(f'@{bot.get_me().username}.mp3' , 'rb')
		bot.send_audio(id ,audio,caption = f"\n<code>{text}</code>\n___________________________\n\n{translatorall.detect(msg.text)[1].title()} 👉 {configlang}\n___________________________\n@{bot.get_me().username}" , parse_mode = "html")
	except:
		bot.send_message(id , " 👉 /start 👈 ")
@bot.callback_query_handler(func=lambda call:True)
def calback(call):
	try:
		global first
		global configlang
		users[str(call.from_user.id)] = call.data
		for i in config.languages.keys():
			if config.languages[i] == call.data:
				configlang = i
				bot.edit_message_text(f'Tilni  <b>{i}</b>ga  o`zgartirdingiz!',chat_id = call.from_user.id , message_id = first.message_id , parse_mode ="html")
	except:
		bot.send_message(call.from_user.id , " 👉 /start 👈 ")
bot.polling()