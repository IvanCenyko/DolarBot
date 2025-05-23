import requests, queue, threading, time, random, telebot
from bs4 import BeautifulSoup
import tools
from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables

load_dotenv()

key = os.getenv("TELEGRAM_KEY")
#bot token
bot = telebot.TeleBot(key)
#multithreading init
q = queue.Queue()
#save DIRs
users_subs = r"./users.txt"
frases_peronistas = r"./frases.txt"
dolar_registrado = r"./dolar.json"



# thread del bot
def telegram_bot():
    # init response
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, text=f'''
Hola soy InzaBot, usá /help para lista de comandos ✌️
CFK 2025!
''')

    # comando help
    @bot.message_handler(commands=['help'])
    def help(message):
        bot.reply_to(message, text= """
Comandos:
/bluenow: el dolar ahora
/addme: te añade a la lista de aviso de subida de dolar
/peron, peronismo, frase, fraseperoncha, fraseperonista: Frase random de Perón
""")

    # comando valor blue actual
    @bot.message_handler(commands=['bluenow'])
    def bluenow(message):
        # responde al usuario con el valor actual de compra y venta
        bot.reply_to(message, text=f'''
El dólar está {tools.json_lector(dolar_registrado)["venta"]} en venta y {tools.json_lector(dolar_registrado)["compra"]} en compra.
VLLC 🦁
''')

    #añadir a lista de usuarios que se avisa cuando sube el dolar
    @bot.message_handler(commands=['addme'])
    def blueadv(message):

        # si no está en la lista
        if not str(message.chat.id) in tools.txt_lector(users_subs):
            # lo añado
            tools.txt_escritor(users_subs, message.chat.id)
            bot.reply_to(message, text='Añadido')

        # si está en la lista, le aviso
        else:
            bot.reply_to(message, text='Ya estás añadido')

    # comando ver lista de usuarios a avisar
    @bot.message_handler(commands=["advlist"])
    def advlist(message):
        bot.reply_to(message, text= str(tools.txt_lector(users_subs)))

    # comando frase de peron
    @bot.message_handler(commands=["peron", "peronismo", "frase", "fraseperoncha", "fraseperonista"])
    def frase_peronista(message):
        bot.reply_to(message, f"""
{random.choice(tools.txt_lector(frases_peronistas))}
- Juan Domingo Perón
""")

    # respuesta a comandos desconocidos
    @bot.message_handler(func=lambda message: True)
    def unknown_command(message):
        bot.reply_to(message, "No te entendí, usá /help para ver la lista de comandos!")


    bot.infinity_polling()


# thread de aviso de subida del dolar
def message_send():
    # valor de inicio referencial
    referencia = tools.json_lector(dolar_registrado)["venta"]

    while 1:
        dolar_now = tools.blue(dolar_registrado)

        # si el valor es mayor en 10 pesos desde la referencia
        if dolar_now['venta'] >= referencia + 10 and tools.txt_lector(users_subs):
            # pongo una nueva referencia
            referencia = tools.json_lector(dolar_registrado)["venta"]
            # aviso
            for user in tools.txt_lector(users_subs):
                bot.send_message(chat_id = user, text= f'El dolar subió a {referencia} VLLC 🦁. Está {dolar_now["venta"]}')

        # si el valor es menor en 10 pesos desde la referencia
        elif dolar_now['venta'] <= referencia - 10 and tools.txt_lector(users_subs):
            # pongo una nueva referencia
            referencia = tools.json_lector(dolar_registrado)["venta"]
            # aviso
            for user in tools.txt_lector(users_subs):
                bot.send_message(chat_id = user, text= f'El dolar bajó a {referencia} VLLC 🦁. Está {dolar_now["venta"]}')


        # sleep para sobrecargar menos las revisiones
        time.sleep(1)

# defino threads
t1 = threading.Thread(target=telegram_bot)
t2 = threading.Thread(target=message_send)
# inicio threads
t1.start()
t2.start()
