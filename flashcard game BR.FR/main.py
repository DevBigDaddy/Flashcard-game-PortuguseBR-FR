import tkinter as tk
from tkinter import PhotoImage
import pandas as pd
import random
import os

# Constantes
BACKGROUND_COLOR = "#B1DDC6"
ORIGINAL_CSV_PATH = "C:/programmation/Python/PythonProject/flashcard game/data/mots portugaisBR.csv"
WORDS_TO_LEARN_PATH = "C:/programmation/Python/PythonProject/flashcard game/data/words_to_learn.csv"
FLIP_DELAY = 3000

# Charger les données (vérifier words_to_learn.csv en premier)
if os.path.exists(WORDS_TO_LEARN_PATH):
    try:
        data = pd.read_csv(WORDS_TO_LEARN_PATH, encoding="utf-8")
    except UnicodeDecodeError:
        data = pd.read_csv(WORDS_TO_LEARN_PATH, encoding="latin1")
    except Exception as e:
        print(f"Erreur lors de la lecture de {WORDS_TO_LEARN_PATH} : {e}")
        exit()
else:
    try:
        data = pd.read_csv(ORIGINAL_CSV_PATH, encoding="utf-8")
    except UnicodeDecodeError:
        data = pd.read_csv(ORIGINAL_CSV_PATH, encoding="latin1")
    except FileNotFoundError:
        print(f"Erreur : Le fichier {ORIGINAL_CSV_PATH} n'a pas été trouvé. Vérifiez le chemin.")
        exit()

# Vérifier les colonnes
expected_columns = ["portugais", "français"]
if not all(col in data.columns for col in expected_columns):
    print(f"Erreur : Les colonnes {expected_columns} ne sont pas toutes présentes dans le CSV.")
    print("Colonnes trouvées :", list(data.columns))
    exit()

words_list = data.to_dict(orient="records")
initial_word_count = len(words_list)  # Nombre initial de mots

# Variables globales
current_word = None
flip_timer = None

# Fenêtre principale
window = tk.Tk()
window.title("1000 mots en Portugais Brésilien")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Charger les images
try:
    card_front = PhotoImage(file="C:/programmation/Python/PythonProject/flashcard game/images/card_front.png")
    card_back = PhotoImage(file="C:/programmation/Python/PythonProject/flashcard game/images/card_back.png")
    wrong_image = PhotoImage(file="C:/programmation/Python/PythonProject/flashcard game/images/wrong.png")
    right_image = PhotoImage(file="C:/programmation/Python/PythonProject/flashcard game/images/right.png")
except tk.TclError as e:
    print(f"Erreur : Impossible de charger les images. Vérifiez les chemins. ({e})")
    exit()


# Fonction pour retourner la carte après 3 secondes
def flip_card(*args):
    global flip_timer
    if current_word is None:
        print("Erreur : Aucun mot sélectionné.")
        return

    # Changer l'image et le titre
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(title_text, text="Français")
    # Changer la couleur des textes
    canvas.itemconfig(title_text, fill="white")
    canvas.itemconfig(word_text, fill="white")
    # Afficher la traduction française
    canvas.itemconfig(word_text, text=current_word["français"])  # type: ignore


# Fonction pour sauvegarder les mots restants dans words_to_learn.csv
def save_words_to_learn():
    if words_list:  # Sauvegarder uniquement si la liste n'est pas vide
        df = pd.DataFrame(words_list)
        df.to_csv(WORDS_TO_LEARN_PATH, index=False, encoding="utf-8")
    else:
        # Si la liste est vide, supprimer le fichier s'il existe
        if os.path.exists(WORDS_TO_LEARN_PATH):
            os.remove(WORDS_TO_LEARN_PATH)


# Fonction pour choisir un mot aléatoire et réinitialiser la carte
def next_word():
    global current_word, flip_timer

    # Annuler le timer précédent si existant
    if flip_timer is not None:
        window.after_cancel(flip_timer)

    # Vérifier si la liste est vide
    if not words_list:
        canvas.itemconfig(title_text, text="Félicitations !", fill="black")
        canvas.itemconfig(word_text, text="Tous les mots appris !", fill="black")
        canvas.itemconfig(card_image, image=card_front)
        # Mettre à jour le compteur
        learned_count = initial_word_count - len(words_list)
        counter_label.config(text=f"Mot appris : {learned_count}")
        return

    # Choisir un mot aléatoire
    current_word = random.choice(words_list)
    portuguese_word = current_word["portugais"]  # type: ignore

    # Réinitialiser la carte à la face avant (portugais)
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(title_text, text="Portugais BR", fill="black")
    canvas.itemconfig(word_text, text=portuguese_word, fill="black")

    # Mettre à jour le compteur
    learned_count = initial_word_count - len(words_list)
    counter_label.config(text=f"Mot appris : {learned_count}")

    # Programmer le flip après 3 secondes
    flip_timer = window.after(FLIP_DELAY, flip_card, ())  # type: ignore


# Fonction pour gérer le clic sur ✅ (mot connu)
def know_word():
    global current_word
    if current_word in words_list:
        words_list.remove(current_word)  # Retirer le mot de la liste
        save_words_to_learn()  # Sauvegarder les mots restants
    next_word()  # Passer au mot suivant


# Grille 2x2
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=0)  # Nouvelle ligne pour le compteur

# Canvas pour la carte
canvas = tk.Canvas(window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Image de la carte
card_image = canvas.create_image(400, 263, image=card_front)

# Textes sur le Canvas
title_text = canvas.create_text(400, 150, text="Portugais BR", font=("Arial", 40, "italic"), fill="black")
word_text = canvas.create_text(400, 326, text="", font=("Arial", 60, "bold"), fill="black")

# Boutons et compteur
wrong_button = tk.Button(window, image=wrong_image, highlightthickness=0, bd=0, command=next_word)
wrong_button.grid(row=1, column=0, padx=20, pady=(20, 0))

# Compteur entre les boutons
counter_label = tk.Label(window, text="Mot appris : 0", font=("Arial", 16), bg=BACKGROUND_COLOR)
counter_label.grid(row=2, column=0, columnspan=2, pady=(5, 5))

right_button = tk.Button(window, image=right_image, highlightthickness=0, bd=0, command=know_word)
right_button.grid(row=1, column=1, padx=20, pady=(20, 0))

# Afficher un mot au démarrage
next_word()

# Boucle principale
window.mainloop()
