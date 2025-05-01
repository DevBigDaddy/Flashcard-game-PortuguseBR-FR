# Flashcard-game-PortuguseBR-FR

# Jeu de Flashcards Portugais-Français

## 📖 Description
Ce projet est un jeu de flashcards interactif qui aide les utilisateurs à apprendre des mots en portugais brésilien avec leurs traductions en français. L'application est construite avec **Python** et utilise **Tkinter** pour l'interface graphique. Les mots sont chargés depuis un fichier CSV, et les progrès sont sauvegardés pour permettre à l'utilisateur de se concentrer sur les mots qu'il ne connaît pas encore.

### Fonctionnalités
- Affiche un mot portugais, puis sa traduction française après 3 secondes.
- Permet de marquer un mot comme "connu" (✅) ou de passer au suivant (❌).
- Sauvegarde les mots restants à apprendre dans `words_to_learn.csv`.
- Charge les mots depuis `words_to_learn.csv` au démarrage si disponible.
- Affiche un compteur de mots appris entre les boutons.

## 📷 Aperçu

![gamecard BR](https://github.com/user-attachments/assets/aa9d024e-5dd4-4291-9df6-6f3ce26e8d9a)
![gamecard FR](https://github.com/user-attachments/assets/8ac28a6c-7691-406a-b569-4b63f439acb6)

## 🚀 Installation
1. Clone ce dépôt :

2. Navigue dans le dossier du projet :

3. Installe les dépendances :
   pip install -r requirements.txt

4. Assure-toi que les fichiers CSV et les images sont dans les dossiers `data/` et `images/`.
   
5. Lance l'application :
   
## 📋 Prérequis
- Python 3.x
- Bibliothèques : `tkinter` (inclus avec Python), `pandas`

## 📂 Structure du projet
- `data/mots portugaisBR.csv` : Fichier CSV initial contenant les mots portugais et leurs traductions françaises.
- `data/words_to_learn.csv` : Fichier généré pour stocker les mots restants à apprendre.
- `images/` : Contient les images pour les cartes et les boutons.
- `main.py` : Code principal de l'application.
- `requirements.txt` : Liste des dépendances.

## 🎮 Utilisation
1. Lance le programme avec `python main.py`.
2. Une carte affiche un mot portugais. Après 3 secondes, elle se retourne pour montrer la traduction française.
3. Clique sur ✅ si tu connais le mot (il sera retiré de la liste), ou sur ❌ pour passer au suivant.
4. Le compteur "Mot appris : n" indique combien de mots tu as appris.
5. Lorsque tous les mots sont appris, un message de félicitations s’affiche.

## 💡 Améliorations futures
- Ajouter un bouton pour réinitialiser la liste des mots.
- Inclure un timer pour chaque carte.
- Ajouter des statistiques sur les progrès (ex. : pourcentage de mots appris).

## 🤝 Contributions
Les contributions sont les bienvenues ! Si tu veux améliorer ce projet, ouvre une *issue* ou soumets une *pull request*.

## 📜 Licence
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements
Merci à [xAI](https://x.ai/) pour leur assistance via Grok dans le développement de ce projet !
