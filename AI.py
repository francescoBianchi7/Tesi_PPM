import matplotlib.pyplot as plt
import PIL.Image
import time
import functools
import tensorflow_hub as hub
import numpy as np
import tensorflow as tf
from natsort import natsorted
from glob import glob
import os


#@markdown Specify the weights directory to use (leave blank for latest)
def select_weight_directory(weight_dir):
    WEIGHTS_DIR = weight_dir #@param {type:"string"}
    model_path = WEIGHTS_DIR
    return model_path

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, DDIMScheduler


 # If you want to use previously trained model saved in gdrive, replace this with the full path of model in gdrive
def activate_generator(weights_dir):
    model_path = weights_dir
    pipe = StableDiffusionPipeline.from_pretrained(model_path, safety_checker=None, torch_dtype=torch.float16).to("cuda")
    pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
    pipe.enable_xformers_memory_efficient_attention()
    g_cuda = None
    #@markdown Can set random seed here for reproducibility.
    g_cuda = torch.Generator(device='cuda')
    seed = -1 #@param {type:"number"}
    #seed=-1 per non dare lo stesso numero di seed a ogni immagine
    g_cuda.manual_seed(seed)
    return g_cuda, pipe

#@title Run for generating images.
def generate(user_prompt, training_prompt, g_cuda, pipe):
    prompt = "photo of ldv gioconda" #@param {type:"string"}
    negative_prompt = "painting of a woman looking straight on a swimming poll" #@param {type:"string"}
    num_samples = 1 #@param {type:"number"}
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
    print(images)
    for img in images:
        #display(img)
        plt.imshow(img)
        plt.axis("off")
        plt.savefig('generated_image.jpg')
    return images


"""OLD GENERATION
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
"""

def style_transfer(original, generated): # original e generated sono path
    print("starting style transfer with", original)
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
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


def commit_image(final_image, dir, name,i):
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
