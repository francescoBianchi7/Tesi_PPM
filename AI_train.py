import json
import os

import matplotlib.pyplot as plt
import matplotlib.image as mpimg



HUGGINGFACE_TOKEN = "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" #@param {type:"string"}
MODEL_NAME = "runwayml/stable-diffusion-v1-5"
cartella = "stable_diffusion_weights/"
OUTPUT_DIR = "/content/" + cartella


def make_concept_list(author, painting):
    autore = "ldv"
    opera = "gioconda"

    concepts_list = [
        {
            "instance_prompt":      "photo of "+autore+" "+opera,
            "class_prompt":         "photo of a "+opera,
            "instance_data_dir":    "/content/"+autore,#le immagini vanno messe qui
            "class_data_dir":       "/content/"+opera
        },
    #     {
    #         "instance_prompt":      "photo of ukj person",
    #         "class_prompt":         "photo of a person",
    #         "instance_data_dir":    "/content/data/ukj",
    #         "class_data_dir":       "/content/data/person"
    #     }
    ]

    for c in concepts_list:
        os.makedirs(c["instance_data_dir"], exist_ok=True)

    with open("concepts_list.json", "w") as f:
        json.dump(concepts_list, f, indent=4)


def train_AI(author, painting):
    comando='python3 train_dreambooth.py --pretrained_model_name_or_path=MODEL_NAME --pretrained_vae_name_or_path="stabilityai/sd-vae-ft-mse" --output_dir=OUTPUT_DIR --revision="fp16" --with_prior_preservation --prior_loss_weight=1.0 --seed=1337 --resolution=512 --train_batch_size=1 --train_text_encoder --mixed_precision="fp16" --use_8bit_adam --gradient_accumulation_steps=1 --learning_rate=1e-6 --lr_scheduler="constant" --lr_warmup_steps=0 --num_class_images=50 --sample_batch_size=4 --max_train_steps=800 --save_interval=800 --save_sample_prompt="photo of autore opera" --concepts_list="concepts_list.json"'

    comando = comando.replace('MODEL_NAME', MODEL_NAME)
    comando = comando.replace('OUTPUT_DIR', OUTPUT_DIR)
    comando = comando.replace('autore', author)
    comando = comando.replace('opera', painting)

    os.system(comando)