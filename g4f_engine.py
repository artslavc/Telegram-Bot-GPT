from g4f.client import Client
from googletrans import Translator

def neiro_zapros(message_text, style):
    print("! Идет Генерация...")

    client = Client()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message_text + f"\n (Общайся как {style})"}],
    )
    return response.choices[0].message.content

def image_zapros(message_text):
    print("! Идет Генерация Картинки...")
    translator = Translator()
    client = Client()
    print(translator.translate(message_text).text)
    response = client.images.generate(
        model="flux",
        prompt=f"{translator.translate(message_text).text}",
        response_format="url"
    )

    return response.data[0].url