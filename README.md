# Introduction
* POC utilisant pytesseract et fuzzy match 
* Transforme en string les données du PDF
* On capte les données à travers des mots clés
* Fonctionnement limité sur des lignes et ne capte pas les données en colonnes 
* **Certaines variables d'environnement sont à modifier dans l'init de la classe Extract_data_from_pdf.** Celles ci doivent correspondre à l'OS utilisé : cf.installations (Poppler et Tesseract OCR)
* Poppler path non nécessaire pour utilisateur linux
* Fonctionnement limité sur un crédit parmi les crédits présents dans le document.

# Prochaines étapes :
* Capturer les tableaux directement avec l'OCR
* Retraiter les valeurs spécifiques à chaque banque (revenus annuels pour BNP vs. revenus mensuels etc...)
* Capturer plusieurs crédits par document

# Fonctionnement :
1. Chargement de deux fichiers : 
    * fichier pdf de données bancaires 
    * fichier excel de base de connaissance: Associe les noms des variables attendues au nom de ces variables dans les fichiers bancaires
2. Transformation des données pdf en image (.JPG) et enregistrement de ces images dans un dossier 
3. Extraction depuis les images des données textuelles 
4. Analyse des données textuelles avec fuzyymatch : 
    * Recherche dans la string de tous les mots clés matchant le mot clé contenu dans la base de connaissance 
    * Calcul d'un score par match (Levenshtein distance) 
    * Récupération du meilleur match 
5. Capture de la données associée à ce mot clé
6. Enregistrement de ces données dans une table 
  
# Installations sur le systeme
* poppler
* tesseract OCR

# Dependencies 
Python==3.8
Fuzzy==1.2.2
fuzzysearch==0.7.3
fuzzywuzzy==0.18.0
ImageHash==4.2.1
opencv-python==4.5.3.56
pandas==1.3.2
pdf2image==1.16.0
Pillow==8.3.1
pytesseract==0.3.8
tesseract-ocr==0.0.1
