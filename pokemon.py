import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

contador = 0

def buscar_pokemon():
    global contador
    nome_pokemon = entrada_pokemon.get().lower()
    api_url = f'https://pokeapi.co/api/v2/pokemon/{nome_pokemon}'

    try:
        resposta = requests.get(api_url)
        resposta.raise_for_status()
        dados_pokemon = resposta.json()

        nome_label.config(text=dados_pokemon['name'].capitalize())

        url_imagem = dados_pokemon['sprites']['front_shiny']
        imagem_resposta = requests.get(url_imagem)
        imagem_bytes = Image.open(BytesIO(imagem_resposta.content))

        tamanho_novo = (imagem_bytes.width * 2, imagem_bytes.height * 2)
        imagem_redimensionada = imagem_bytes.resize(tamanho_novo, Image.Resampling.LANCZOS)

        imagem_pokemon = ImageTk.PhotoImage(imagem_redimensionada)

        imagem_label.config(image=imagem_pokemon)
        imagem_label.image = imagem_pokemon

        contador = 0
        atualizar_contador()

    except requests.exceptions.HTTPError as e:
        nome_label.config(text="Erro ao buscar o Pokémon")
        print(f"Erro: {e}")

def aumentar_contador():
    global contador
    contador += 1
    atualizar_contador()

def atualizar_contador():
    contador_label.config(text=f'Encontros: {contador}')


janela = tk.Tk()
janela.title('PokeEncounter')
janela.geometry('300x450')
janela.config(bg='#ADD8E6')
janela.iconbitmap('icone.ico')

entrada_pokemon = tk.Entry(janela, font=('Arial', 14))
entrada_pokemon.pack(pady=10)

botao_buscar = tk.Button(janela, text="Buscar", command=buscar_pokemon, font=('Arial', 14), 
                          bg='#FF4500', fg='white')
botao_buscar.pack(pady=5)

nome_label = tk.Label(janela, text="", font=('Arial', 16, "bold"), bg='#ADD8E6', fg='#000000')
nome_label.pack(pady=5)

imagem_label = tk.Label(janela, bg='#ADD8E6')
imagem_label.pack(pady=10)

contador_label = tk.Label(janela, text="Encontros: 0", font=('Arial', 14), bg='#ADD8E6', fg='#000000')
contador_label.pack(pady=5)

botao_encontrado = tk.Button(janela, text="Botão", command=aumentar_contador, font=('Arial', 14), 
                             bg='#FF4500', fg='white')
botao_encontrado.pack(pady=5)

janela.mainloop()