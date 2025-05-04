import tkinter as tk
from tkinter import PhotoImage, messagebox
import pandas as pd
import random
import os
import sys

# Constantes
BACKGROUND_COLOR = "#B1DDC6"
ORIGINAL_CSV_PATH = "data/mots_portugaisBR.csv"
WORDS_TO_LEARN_FILENAME = "words_to_learn.csv"
FLIP_DELAY = 2000

def resource_path(relative_path):
    """Obtenir le chemin absolu d'un fichier, fonctionne pour le script et l'exécutable."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def get_user_data_path(filename):
    """Obtenir un chemin dans le dossier utilisateur pour sauvegarder les données."""
    appdata = os.getenv('APPDATA') or os.path.expanduser('~')
    app_dir = os.path.join(appdata, "FlashcardGameBRFR")
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, filename)

# Charger les données
words_list = []
initial_word_count = 0

try:
    user_words_path = get_user_data_path(WORDS_TO_LEARN_FILENAME)
    if os.path.exists(user_words_path):
        try:
            data = pd.read_csv(user_words_path, encoding="utf-8")
        except UnicodeDecodeError:
            data = pd.read_csv(user_words_path, encoding="latin1")
    else:
        csv_path = resource_path(ORIGINAL_CSV_PATH)
        try:
            data = pd.read_csv(csv_path, encoding="utf-8")
        except UnicodeDecodeError:
            data = pd.read_csv(csv_path, encoding="latin1")
        except FileNotFoundError:
            messagebox.showerror("Erreur", f"Le fichier {ORIGINAL_CSV_PATH} n'a pas été trouvé.")
            raise FileNotFoundError

    # Vérifier les colonnes
    expected_columns = ["portugais", "français"]
    if not all(col in data.columns for col in expected_columns):
        messagebox.showerror("Erreur", f"Les colonnes {expected_columns} ne sont pas toutes présentes.\nColonnes trouvées : {list(data.columns)}")
        raise ValueError
    words_list = data.to_dict(orient="records")
    initial_word_count = len(words_list)
except Exception as e:
    window = tk.Tk()
    window.withdraw()  # Cacher la fenêtre principale
    messagebox.showerror("Erreur", f"Erreur lors du chargement des données : {str(e)}")
    window.destroy()
    sys.exit(1)

# Variables globales
current_word = None
flip_timer = None

# Fenêtre principale
window = tk.Tk()
window.title("1000 mots en Portugais Brésilien")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Charger les images
try:
    card_front = PhotoImage(file=resource_path("images/card_front.png"))
    card_back = PhotoImage(file=resource_path("images/card_back.png"))
    wrong_image = PhotoImage(file=resource_path("images/wrong.png"))
    right_image = PhotoImage(file=resource_path("images/right.png"))
except tk.TclError as e:
    messagebox.showerror("Erreur", f"Impossible de charger les images. Vérifiez les chemins.\n{str(e)}")
    window.destroy()
    sys.exit(1)

# Fonction pour retourner la carte
def flip_card(*args):
    global flip_timer
    if current_word is None:
        messagebox.showerror("Erreur", "Aucun mot sélectionné.")
        return
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(title_text, text="Français", fill="white")
    canvas.itemconfig(word_text, text=current_word["français"], fill="white")

# Fonction pour sauvegarder les mots restants
def save_words_to_learn():
    if words_list:
        df = pd.DataFrame(words_list)
        user_words_path = get_user_data_path(WORDS_TO_LEARN_FILENAME)
        try:
            df.to_csv(user_words_path, index=False, encoding="utf-8")
        except Exception as e:
            messagebox.showwarning("Avertissement", f"Impossible de sauvegarder words_to_learn.csv : {str(e)}")
    else:
        user_words_path = get_user_data_path(WORDS_TO_LEARN_FILENAME)
        if os.path.exists(user_words_path):
            try:
                os.remove(user_words_path)
            except Exception:
                pass

# Fonction pour choisir un mot aléatoire
def next_word():
    global current_word, flip_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)
    if not words_list:
        canvas.itemconfig(title_text, text="Félicitations !", fill="black")
        canvas.itemconfig(word_text, text="Tous les mots appris !", fill="black")
        canvas.itemconfig(card_image, image=card_front)
        learned_count = initial_word_count - len(words_list)
        counter_label.config(text=f"Mots appris : {learned_count}")
        return
    current_word = random.choice(words_list)
    portuguese_word = current_word["portugais"]
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(title_text, text="Portugais BR", fill="black")
    canvas.itemconfig(word_text, text=portuguese_word, fill="black")
    learned_count = initial_word_count - len(words_list)
    counter_label.config(text=f"Mots appris : {learned_count}")
    flip_timer = window.after(FLIP_DELAY, flip_card)

# Fonction pour gérer le clic sur ✅
def know_word():
    global current_word
    if current_word in words_list:
        words_list.remove(current_word)
        save_words_to_learn()
    next_word()

# Grille 2x2
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=0)

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

counter_label = tk.Label(window, text="Mots appris : 0", font=("Arial", 16), bg=BACKGROUND_COLOR)
counter_label.grid(row=2, column=0, columnspan=2, pady=(5, 5))

right_button = tk.Button(window, image=right_image, highlightthickness=0, bd=0, command=know_word)
right_button.grid(row=1, column=1, padx=20, pady=(20, 0))

# Afficher un mot au démarrage
next_word()

# Boucle principale
window.mainloop()