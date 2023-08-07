from textwrap import wrap
import os

os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

import keras_cv
import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd
import tensorflow as tf
# import tensorflow.experimental.numpy as tnp
from keras_cv.models.stable_diffusion.clip_tokenizer import SimpleTokenizer
from keras_cv.models.stable_diffusion.diffusion_model import DiffusionModel
from keras_cv.models.stable_diffusion.image_encoder import ImageEncoder
from keras_cv.models.stable_diffusion.noise_scheduler import NoiseScheduler
from keras_cv.models.stable_diffusion.text_encoder import TextEncoder
from tensorflow import keras

import PIL.Image
import time
import functools
import tensorflow_hub as hub


# prompts verrà sostituito con input dell'utente
prompts = ["Gioconda"]  # input dato dall'utente

images_to_generate = 1  # il numero di immagini da generare
outputs = {}  # qui vengono messe le immagini generate dall'algoritmo

def start_AI():  # chiamato all'avvio
    os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'
    #mpl.rcParams['figure.figsize'] = (12, 12)  # avvio
    #mpl.rcParams['axes.grid'] = False  # avvio
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    print("Ai started")
    return hub_model


def select_weight(stable_diff_path):  # author servirà per selezionare il finetuning
    # una volta che l'utente ha selezionato l'opera, dato che poi avremmo più di un possibile autore
    #weights_path = '/content/drive/MyDrive/finetuned_stable_diffusion.h5'  # dopo che l'utente ha selezionato l'opera
    weights_path = stable_diff_path
    # da cambiare, verrà preso tramite database
    # will be changed to the right path
    img_height = img_width = 512
    # definizione del modello, prende in input la dimensione dell'immagine, sono funzioni di keras, librerie da importare
    paintings_model = keras_cv.models.StableDiffusion(
        img_width=img_width, img_height=img_height)
    paintings_model.diffusion_model.load_weights(weights_path)  # carica il file .h5
    return paintings_model


def generate_image(user_prompt, paintings_model):
    prompts = [user_prompt]
    for prompt in prompts:
        generated_images = paintings_model.text_to_image(
            prompt, batch_size=images_to_generate, unconditional_guidance_scale=40
        )
        # questo for applica l'algoritmo di text to image, prendendo l'input(prompt), il n di immagini da generare, dimensioni. mette il risultato in outputs
        outputs.update({prompt: generated_images})
    print("generated")
    for prompt in outputs:  # esegue la funzione plot sull'array outputs
        path = plot_images(outputs[prompt])
    print("plotted")
    return path, outputs

def style_transfer(original, generated, hub_model):  # original e generated sono path
    print("starting style transfer with", original)
    content_path = generated
    print("generated", content_path)
    print("model", hub_model)
    style_path = original
    content_image = load_img(content_path)
    style_image = load_img(style_path)
    # generazione
    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
    print("stylized image done")
    # utilizza il modello caricato sopra, gli passa le 2 immagini e genera il risultato finale
    # fine generazione
    final_image = tensor_to_image(stylized_image)
    print("converted")
    #final_image = final_image.save('finale.jpg')  # salva immagine come file, dovrò trovare il modo
    print("saved")
    # per salvarle in un path unico, e nel database
    # probabilmente verrà fatto solo una volta che l'utente switcha pagina
    # almeno evito di salvare l'immagine mille volte
    return final_image

def commit_image(final_image,dir, name,i):
    # verrà ulteriormente inserita in una tabella del database.
    print("inserting num:", i)
    path=dir+name+str(i)+".jpg"
    final_image.save(path)
    return path



"""



os.environ["SM_FRAMEWORK"] = "tf.keras"

#mpl.rcParams['figure.figsize'] = (12, 12) #avvio
#mpl.rcParams['axes.grid'] = False #avvio
"""

"""una volta che l'utente ha selezionato l'opera, dato che poi avremmo più di un possibile autore
weights_path = 'static/images/Leonardo da vinci/finetuned_stable_diffusion.h5' #dopo che l'utente ha selezionato l'opera
img_height = img_width = 512
paintings_model = keras_cv.models.StableDiffusion(
    img_width=img_width, img_height=img_height
)  # definizione del modello, prende in input la dimensione dell'immagine, sono funzioni di keras, librerie da importare
paintings_model.diffusion_model.load_weights(weights_path)  # carica il file .h5

"""


""" inizio generazione 
for prompt in prompts:
    generated_images = paintings_model.text_to_image(
        prompt, batch_size=images_to_generate, unconditional_guidance_scale=40
    )
    # questo for applica l'algoritmo di text to image, prendendo l'input(prompt), il n di immagini da generare, dimensioni. mette il risultato in outputs
    outputs.update({prompt: generated_images})
"""


def plot_images(images):
    # funzione che usa matplotlib per disegnare/stampare l'immagine e salvarla come file
    # prende in ingresso l'immagine da stampare(contenuta in outputs)
    plt.figure(figsize=(30, 30))
    print("plotting")
    for i in range(len(images)):
        ax = plt.subplot(1, len(images), i + 1)
        plt.imshow(images[i])
        plt.axis("off")
        plt.savefig('generated_image.jpg')
    temp = PIL.Image.open("generated_image.jpg")
    temp.show()
    path = 'generated_image.jpg'
    return path
# for prompt in outputs:  # esegue la funzione sopra sull'array outputs
# plot_images(outputs[prompt])


def load_img(path_to_img):
    # serve per la conversione dell'immagine in un formato accettato dal modello hub_model
    # prende in input la directory dove è salvata l'immagine
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


def tensor_to_image(tensor):
    # effettua una conversione di stylized_image nell'ultima riga di codice, per averla in formato stampabile e visibile
    # riceve in input stylized_image, che è il risultato finale, ma non in formato jpg
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)


"""style transfer post generazione, dato che all'utente 
verrà mostrata tutte le righe sono eseguite a fine della generazione, ma prima di mostrarla a schermo"""
"""
content_path = '/content/generated_image.jpg'
style_path = '/content/drive/MyDrive/originale.jpeg'
content_image = load_img(content_path)
style_image = load_img(style_path)
"""
""" generazione
stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
# utilizza il modello caricato sopra, gli passa le 2 immagini e genera il risultato finale
"""
""" fine generazione
final_image = tensor_to_image(stylized_image)
final_image = final_image.save('finale.jpg')  # salva immagine come file
"""
"""
non penso che seriviranno,
 le immagini saranno mostrate nella pagina html e quindi penso basti inviare il path dell'immagine 
 """
# im=PIL.Image.open("finale.jpg")
# im.show()
# im #su colab im.show() non funziona e va messo solo il nome della variabile per mostrare l'immagine
