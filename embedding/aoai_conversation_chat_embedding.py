import pandas as pd  # for storing text and embeddings data
import ast  # for converting embeddings saved as strings back to arrays
from utility import *
from dotenv import load_dotenv

load_dotenv()

embeddings_path="output.csv"

cwd = os.getcwd()
file_path = os.path.join(cwd, embeddings_path)
df = pd.read_csv(file_path)
# convert embeddings from CSV str type back to list type
df['embedding'] = df['embedding'].apply(ast.literal_eval)

# get the similarity content from embedding content
# append the similarity content to the content parameter
response_message = conversation(df=df)
