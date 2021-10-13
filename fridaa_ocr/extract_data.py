import pandas as pd
from fridaa_pkg.Extract_data_from_pdf import Extract_data_from_pdf

knowledge_base = 'knowledge_base/alim_keywords.xlsx'
pdf_file = 'pdf_files/CIC.pdf'
results_path = 'results/'

#Extract Data and save in xlsx file
results = Extract_data_from_pdf(pdf_file, knowledge_base)
results.export_data.to_excel(f"{results_path}{results.bank}.xlsx", sheet_name='Sheet1', index = False)

