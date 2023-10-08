# File conversion functions
from countryinfo import CountryInfo
import pandas as pd 
import os 

def convert_to_text(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        print(filename)
        print(file_path)
        
        if filename.endswith('.pdf'):
            text = extract_text('upr_docs/'+filename)
            text_path = os.path.join('upr-files/', filename[:-4] + '.txt')
            with open(text_path, 'w',encoding='utf-8') as text_file:
                text_file.write(text)
            print(f'{filename} converted to {filename[:-4]}.txt')

        elif filename.endswith('.docx'):
            doc = docx.Document(file_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            text_path = os.path.join(directory_path, filename[:-5] + '.txt')
            with open(text_path, 'w',encoding='utf-8') as text_file:
                text_file.write(text)
            print(f'{filename} converted to {filename[:-5]}.txt')

        elif filename.endswith('.doc'):
            word_app = win32com.client.Dispatch('Word.Application')
            word_app.Visible = False
            doc = word_app.Documents.Open(file_path)
            txt_path = file_path[:-4] + '.txt'
            doc.SaveAs(txt_path, FileFormat=win32com.client.constants.wdFormatText)
            doc.Close()
            word_app.Quit()
            print(f'{filename} converted to {os.path.basename(txt_path)}')


def fix_document(path):
    with open(path, 'r',encoding='utf-8') as file:
        text = file.read()
    # Replace sequences of whitespace with single space
    text = ' '.join(text.split())
    # If you want to write the cleaned text back into the file
    with open(path, 'w',encoding='utf-8') as file:
        file.write(text)
    return text 
    
def fix_documents(paths):
    texts = []
    for path in paths:
        texts.append(fix_document(path))
    
    return
# nlp = spacy.load("en_core_web_trf")
# doc = nlp(text)

def convert_excel_to_csv(excel_file_path, output_dir):
    """
    Converts an Excel file to a CSV file.
    
    Parameters:
        excel_file_path (str): Path to the Excel file
        output_dir (str): Directory where the CSV files will be saved
        
    Returns:
        None
    """
    try:
        # Read the Excel file
        xls = pd.ExcelFile(excel_file_path)
        
        # Loop through each sheet in the Excel file
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name)
            
            # Create a CSV file name based on the Excel file name and sheet name
            csv_file_name = f"{os.path.splitext(os.path.basename(excel_file_path))[0]}_{sheet_name}.csv"
            csv_file_path = os.path.join(output_dir, csv_file_name)
            
            # Save the DataFrame to CSV
            df.to_csv(csv_file_path, index=False)
            
        print(f"Successfully converted {excel_file_path} to CSV.")
    except Exception as e:
        print(f"An error occurred while converting {excel_file_path}: {e}")

def mass_convert_excel_to_csv(input_dir, output_dir):
    """
    Converts all Excel files in the input directory to CSV files and saves them in the output directory.
    
    Parameters:
        input_dir (str): Directory containing Excel files
        output_dir (str): Directory where the CSV files will be saved
    
    Returns:
        None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for filename in os.listdir(input_dir):
        if filename.endswith('.xls') or filename.endswith('.xlsx'):
            excel_file_path = os.path.join(input_dir, filename)
            convert_excel_to_csv(excel_file_path, output_dir)

