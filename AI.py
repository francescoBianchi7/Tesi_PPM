import matplotlib.pyplot as plt
import PIL.Image
import time
import functools
import tensorflow_hub as hub
import numpy as np
import tensorflow as tf



#@markdown Specify the weights directory to use (leave blank for latest)
WEIGHTS_DIR = "/content/drive/MyDrive/stable_diffusion_weights/800" #@param {type:"string"}
if WEIGHTS_DIR == "":
    from natsort import natsorted
    from glob import glob
    import os
    WEIGHTS_DIR = natsorted(glob(OUTPUT_DIR + os.sep + "*"))[-1]
print(f"[*] WEIGHTS_DIR={WEIGHTS_DIR}")

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, DDIMScheduler


model_path = WEIGHTS_DIR             # If you want to use previously trained model saved in gdrive, replace this with the full path of model in gdrive

pipe = StableDiffusionPipeline.from_pretrained(model_path, safety_checker=None, torch_dtype=torch.float16).to("cuda")
pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
pipe.enable_xformers_memory_efficient_attention()
g_cuda = None


#@markdown Can set random seed here for reproducibility.
g_cuda = torch.Generator(device='cuda')
seed = -1 #@param {type:"number"}
#seed=-1 per non dare lo stesso numero di seed a ogni immagine
g_cuda.manual_seed(seed)


#@title Run for generating images.

prompt = "photo of ldv gioconda" #@param {type:"string"}
negative_prompt = "painting of a woman looking straight on a swimming poll" #@param {type:"string"}
num_samples = 2 #@param {type:"number"}
guidance_scale = 5 #@param {type:"number"}
num_inference_steps = 50 #@param {type:"number"}
height = 512 #@param {type:"number"}
width = 512 #@param {type:"number"}

with autocast("cuda"), torch.inference_mode():
    images = pipe(
        prompt,
        height=height,
        width=width,
        negative_prompt=negative_prompt,
        num_images_per_prompt=num_samples,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=g_cuda
    ).images

for img in images:
    #display(img)
    plt.imshow(img)
    plt.axis("off")
    plt.savefig('generated_image.jpg')

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
    path = dir+name+str(i)+".jpg"
    final_image.save(path)
    return path




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


