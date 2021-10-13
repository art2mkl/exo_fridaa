# Introduction
* POC utilisant pytesseract et fuzzy match 
* Transforme en string  données du PDF
* On capte les données à travers des mots clés
* Fonctionnement limité sur des lignes et ne capte pas les données en colonnes 
* **Certaines variables d'environnement sont à modifier dans l'init de la classe Extract_data_from_pdf.** Celles ci doivent correspondre à l'OS utilisé
* Poppler path non nécessaire pour utilisateur linux  

# Prochaines étapes :
Capturer les tableaux directement avec l'OCR 
Retraiter les valeurs spécifiques à chaque banque (revenus annuels pour BNP vs. revenus mensuels etc...)

# Fonctionnement :
1. Chargmement de deux fichiers : 
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
  

# Dependencies 
### OCR dependencies
from PIL import Image       
import Image         
import pytesseract        

from pdf2image import convert_from_path      
import os      
import cv2      
import re        

### Text analysis dependencies
import pandas as pd      

from fuzzysearch import find_near_matches     
from fuzzywuzzy import fuzz    
from fuzzywuzzy import process     
