try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

from pdf2image import convert_from_path
import os
import cv2
import re

import pandas as pd

from fuzzysearch import find_near_matches
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class Extract_data_from_pdf:
    
    def __init__(self, pdf_path, keywords_path):

        print('Extraction en cours...')
        
        # Config software path (OCR, POPPLER) and catch length
        self.pytesseract_path = r'/usr/local/bin/tesseract'
        self.poppler_path = r'/usr/local/Cellar/poppler/21.09.0/bin'
        self.catch_length = 20
        self.txt = ""
        self.image_file_path = r'img_files/'
        
        # Create list of images after converting pdf in image 
        self.list_jpg = self.pdf_to_img(pdf_path)
        
        
        self.df = pd.read_excel(keywords_path)
        self.banks = self.df.columns[1:]
        self.extract_basic()
        self.choose_bank()
        self.keywords = self.df[self.bank].tolist()
        self.export_data = pd.DataFrame([self.export_result()], columns = self.df['variables'].tolist()).assign(banque=self.bank)
        print('Extraction terminée')
    
    #--------------------------------------------------------------------------------------------#  
    def extract_basic(self):
        """
        Extract string with basic scan of each pages from pdf
        @print string
        @return none
        """
        final_txt=''
        for item_jpg in self.list_jpg:
            add_string = self.img_to_string(item_jpg)
            final_txt = final_txt+f'\n page_{self.list_jpg.index(item_jpg)+1}\n'+add_string
            
        self.txt = final_txt
        #print(self.txt)
        
    #--------------------------------------------------------------------------------------------#
    def choose_bank(self):
        """
        Select bank name in string file
        @return none
        """
        for i in self.banks:
            if i in self.txt:
                self.bank = i
                break
    
    #--------------------------------------------------------------------------------------------#
    def img_to_string(self, img_path):
        """
        Scan element to string
        @return string with all scan
        """
        pytesseract.pytesseract.tesseract_cmd = self.pytesseract_path
        return pytesseract.image_to_string(Image.open(img_path))
    
    #--------------------------------------------------------------------------------------------#
    def pdf_to_img(self, pdf_path):
        """
        Convert and save all pdf pages in jpeg files
        @return list of jpeg files
        """
       
        pages = convert_from_path(pdf_path, 350,
                                  
                                  #xxxxx delete this line on linux distribution xxxxxxx
                                  poppler_path = self.poppler_path
                                  #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                 )
        
        i = 1
        name = os.path.basename(pdf_path).split('.')[0]
        tab_jpg = []
        
        for page in pages:
            image_name = self.image_file_path + name + str(i) + ".jpg"  
            page.save(image_name, "JPEG")
            i = i+1
            tab_jpg.append(image_name)
        
        return tab_jpg
    
    #--------------------------------------------------------------------------------------------#
    def catch_result(self, key_word):
        """
        Select on scan best keyword matches compare to knowledge_base and extract numerical value associated
        @return numerical value or "Not found"
        """
    
        results = find_near_matches( key_word, self.txt, max_l_dist = 1)
        if len(results) != 0:
            results_score = [fuzz.token_sort_ratio(key_word, i.matched) for i in results]

            start = results[results_score.index(max(results_score))].end
            final_list = re.findall('\d+[\d\s,.]\d+|[\d\s,.]\d+|\d', self.txt[start:start + self.catch_length].replace(' ',''))
            if len(final_list) == 0:
                return "Not found"

            else:
                return final_list[0]
        else:
            return "Not found"
        
    #--------------------------------------------------------------------------------------------#
    def export_result(self):
        """
        Create a list of catched results
        @return list
        """
        return [self.catch_result(i) for i in self.keywords]

