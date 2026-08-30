import os
import PyPDF2
import re
import pandas as pd
from collections import OrderedDict

counter_dict = OrderedDict()

first_digit = 0
last_digit = 6

# Función para extraer los datos de los ganadores
def extract_winner_data(text):
    global counter_dict
    # Expresión regular para encontrar los datos de los ganadores
    pattern = re.compile(r'(\d{6})\s+(\d+)\s+\$([\d,]+)\s+([A-Z\s\.]+)\s+([A-Z\.]+)')
    matches = pattern.findall(text)
    
    winners = []
    for match in matches:
        winners.append({
            'numero_boleto': match[0],
            'numero_premio': match[1],
            'premio': match[2],
            'nombre': match[3].strip(),
            'estado': match[4]
        })
        if match[0][first_digit:last_digit] in counter_dict:
            counter_dict[match[0][first_digit:last_digit]] += 1
        else:
            counter_dict[match[0][first_digit:last_digit]] = 1
        #print('numero_boleto:', match[0], 'numero_premio:', match[1], 'premio:', match[2], 'nombre:', match[3].strip(), 'estado:', match[4])
    
    return winners, len(matches)

def extract_winner_data_02(text):
    global counter_dict
    # Expresión regular para encontrar los datos de los ganadores
    #pattern = re.compile(r'(\d{6})\s+(\d+)\s+\$([\d,]+)\s+([A-Z\s\.]+)\s+([A-Z\.]+)')
    pattern = re.compile(r'(\d{6})\s+\$([\d,]+)\s')
    matches = pattern.findall(text)
    
    winners = []
    for match in matches:
        winners.append({
            'numero_boleto': match[0],
            'premio': match[1],
        })
        if match[0][first_digit:last_digit] in counter_dict:
            counter_dict[match[0][first_digit:last_digit]] += 1
        else:
            counter_dict[match[0][first_digit:last_digit]] = 1
        #print('numero_boleto:', match[0], 'numero_premio:', match[1], 'premio:', match[2], 'nombre:', match[3].strip(), 'estado:', match[4])
    
    return winners, len(matches)

def extract_winner_data_03(text):
    global counter_dict
    # Expresión regular para encontrar los datos de los ganadores
    #pattern = re.compile(r'(\d{6})\s+(\d+)\s+\$([\d,]+)\s+([A-Z\s\.]+)\s+([A-Z\.]+)')
    pattern = re.compile(r'(\d{6})\s+(\d+)\s+([A-Z\s\.]+)\s+([A-Z\s\.]+)\s+([A-Z\s\.]+)\s')
    matches = pattern.findall(text)
    
    winners = []
    for match in matches:
        winners.append({
            'numero_boleto': match[0],
            'numero_premio': match[1],
            'premio_description': match[2], # description
            'nombre': match[3], 
            'estado': match[4], 
        })
        if match[0][first_digit:last_digit] in counter_dict:
            counter_dict[match[0][first_digit:last_digit]] += 1
        else:
            counter_dict[match[0][first_digit:last_digit]] = 1
        #print('numero_boleto:', match[0], 'numero_premio:', match[1], 'premio:', match[2], 'nombre:', match[3].strip(), 'estado:', match[4])
    
    return winners, len(matches)


# Función para leer el PDF y extraer el texto
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        #reader = PyPDF2.PdfFileReader(file)
        reader = PyPDF2.PdfReader(file)
        text = ''
        n_pages = len(reader.pages)
        for page_num in range(n_pages):
            #page = reader.getPage(page_num)
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Función para procesar todos los PDFs en un directorio
def process_pdfs_in_directory(directory, output_path):
    # Lista para almacenar todos los datos
    all_winners = []
    
    # Recorrer todos los archivos en el directorio
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            print(f"Procesando archivo: {filename}", end=' ')
            
            # Leer el PDF y extraer el texto
            pdf_text = read_pdf(file_path)
            
            # Extraer los datos de los ganadores
            winners, matches = extract_winner_data(pdf_text)
            if matches > 0:
                print("Numero de registros encontrados con 1: ", matches)
            if matches == 0:
                winners, matches = extract_winner_data_02(pdf_text)
                if matches > 0:
                    print("Numero de registros encontrados con 2: ", matches)
            if matches == 0:
                winners, matches = extract_winner_data_03(pdf_text)
                if matches > 0:
                    print("Numero de registros encontrados con 3: ", matches)
            
            # Agregar los datos a la lista general
            all_winners.extend(winners)
    
    # Convertir la lista de diccionarios a un DataFrame de pandas
    df = pd.DataFrame(all_winners)
    
    # Guardar el DataFrame en un archivo Parquet
    output_file = os.path.join(output_path, 'ganadores.parquet')
    output_file_csv = os.path.join(output_path, 'ganadores.csv')
    #df.to_parquet(output_file, engine='pyarrow')
    #df.to_csv(output_file_csv)
    print(f"Datos guardados en {output_file}")



if __name__ == '__main__':
    input_path = '/mnt/d/DATA/SORTEO_TEC/PDFS_03'
    output_path = '/mnt/d/DATA/SORTEO_TEC/PROCESADOS'
    process_pdfs_in_directory(directory=input_path, output_path=output_path)
    for key, value in sorted(counter_dict.items(), key=lambda x: x[1]):
        print(key, value)