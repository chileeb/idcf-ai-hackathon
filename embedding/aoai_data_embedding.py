import os
import fitz  # PyMuPDF
import csv
import openai
from utility import *
from dotenv import load_dotenv

load_dotenv()


openai.api_type='azure'
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_EMBEDDING_ENGINE = os.getenv("OPENAI_EMBEDDING_ENGINE")

# Define if generate new PDF files
generate_new_pdf = True

cwd = os.getcwd()
source_folder_name = "embedding\\data"
target_folder_name = "embedding\\data_output"
# set the path to the "data" subdirectory
source_folder = os.path.join(cwd, source_folder_name)
target_folder = os.path.join(cwd, target_folder_name)
if generate_new_pdf:
    split_pdf_to_pages(source_folder, target_folder)

# Define the output CSV file
csv_output_file = "output.csv"

# Initialize the CSV writer
csv_file = open(csv_output_file, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)

# Write the header to the CSV file
csv_writer.writerow(["text", "embedding"])

# Traverse through each PDF file in the directory
for file_name in os.listdir(target_folder):
    if file_name.endswith(".pdf"):
        # Open the PDF file
        pdf_file = fitz.open(os.path.join(target_folder, file_name))

        # Extract the text from the PDF file
        text = ""
        for page in pdf_file:
            text += page.get_text()
        
        text = text.replace('\n', ' ').replace('\r', '')
        embedding = openai.Embedding().create(input=[text], engine=OPENAI_EMBEDDING_ENGINE)["data"][0]["embedding"]

        # Write the file name and the embedding text to the CSV file
        csv_writer.writerow([file_name, text, embedding])

# Close the CSV file
csv_file.close()

# exit from Python
exit()
