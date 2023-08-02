import os
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

import keras_cv
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub



import PIL.Image

""" avvio"""

os.environ["SM_FRAMEWORK"] = "tf.keras"
""" avvio"""
#mpl.rcParams['figure.figsize'] = (12, 12) #avvio
""" avvio"""
#mpl.rcParams['axes.grid'] = False #avvio


"""una volta che l'utente ha selezionato l'opera, dato che poi avremmo più di un possibile autore"""
weights_path = '/content/drive/MyDrive/finetuned_stable_diffusion.h5' #dopo che l'utente ha selezionato l'opera
img_height = img_width = 512
paintings_model = keras_cv.models.StableDiffusion(
    img_width=img_width, img_height=img_height
)  # definizione del modello, prende in input la dimensione dell'immagine, sono funzioni di keras, librerie da importare
paintings_model.diffusion_model.load_weights(weights_path)  # carica il file .h5


"""prompts verrà sostituito con input dell'utente"""
prompts = ["Gioconda"]  # input dato dall'utente

images_to_generate = 1  # il numero di immagini da generare
outputs = {}  # qui vengono messe le immagini generate dall'algoritmo

""" inizio generazione """
for prompt in prompts:
    generated_images = paintings_model.text_to_image(
        prompt, batch_size=images_to_generate, unconditional_guidance_scale=40
    )
    # questo for applica l'algoritmo di text to image, prendendo l'input(prompt), il n di immagini da generare, dimensioni. mette il risultato in outputs
    outputs.update({prompt: generated_images})


"""generazione """
def plot_images(images):
    # funzione che usa matplotlib per disegnare/stampare l'immagine e salvarla come file
    # prende in ingresso l'immagine da stampare(contenuta in outputs)
    plt.figure(figsize=(30, 30))
    for i in range(len(images)):
        ax = plt.subplot(1, len(images), i + 1)
        plt.imshow(images[i])
        plt.axis("off")
        plt.savefig('generated_image.jpg')


for prompt in outputs:  # esegue la funzione sopra sull'array outputs
    plot_images(outputs[prompt])

"""generazione """
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

"""generazione """
def tensor_to_image(tensor):
    # effettua una conversione di stylized_image nell'ultima riga di codice, per averla in formato stampabile e visibile
    # riceve in input stylized_image, che è il risultato finale, ma non in formato jpg
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)

"""avvio"""
hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
# caricamente del modello per il style transfer, è già fatto e va scaricato

"""style transfer post generazione, dato che all'utente 
verrà mostrata tutte le righe sono eseguite a fine della generazione, ma prima di mostrarla a schermo"""
content_path = '/content/generated_image.jpg'
style_path = '/content/drive/MyDrive/originale.jpeg'
content_image = load_img(content_path)
style_image = load_img(style_path)
""" generazione"""
stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
# utilizza il modello caricato sopra, gli passa le 2 immagini e genera il risultato finale
""" fine generazione"""
final_image = tensor_to_image(stylized_image)
final_image = final_image.save('finale.jpg')  # salva immagine come file

"""
non penso che seriviranno,
 le immagini saranno mostrate nella pagina html e quindi penso basti inviare il path dell'immagine 
 """
# im=PIL.Image.open("finale.jpg")
# im.show()
# im #su colab im.show() non funziona e va messo solo il nome della variabile per mostrare l'immagine
