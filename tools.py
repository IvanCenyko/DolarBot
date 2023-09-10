import json, requests
from bs4 import BeautifulSoup

def txt_lector(direction:str):
    file = open(direction, "r+")
    file_read = file.read()

    line = ""
    lines = []
    letters = list(file_read)

    for digit in letters:
        if not digit == "\n":
            line += digit
        if digit == "\n":
            lines.append(line)
            line = ""
    return lines

def txt_escritor(direction:str, information):
    file = open(direction, "a")
    file.write(f"{information}\n")

def json_escritor(**kwargs):

    with open(kwargs['direction'], 'w') as js:
        json.dump(kwargs['dict'], js)

def json_borrador(direction:str):
    with open(r'./dolar.json', 'w') as js:
        js.truncate()

def json_lector(direction:str):
    with open(direction, 'r') as js:
        return json.load(js)
    
def blue(save_dir):
    # request
    dolar = requests.get('https://apiweb-ivancenyko.vercel.app/dolar-blue').json()
    try:
        json_borrador(save_dir)
    except:
        pass
    compra = dolar["compra"]
    venta =  dolar["venta"]
    json_escritor(direction=save_dir, dict={"venta": venta, "compra": compra})
    return {"venta": venta, "compra": compra}



