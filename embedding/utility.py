import os
import fitz  # PyMuPDF
import shutil
import openai
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from dotenv import load_dotenv
from scipy import spatial  # for calculating vector similarities for search

load_dotenv()

openai.api_type='azure'
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_ENGINE")
OPENAI_GPT35_ENGINE = os.getenv("OPENAI_GPT35_ENGINE")
GPT_MODEL = "gpt-3.5-turbo"

def split_pdf_to_pages(source_folder: str, target_folder: str):
    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)
    os.mkdir(target_folder)

    for file in os.listdir(source_folder):
        path = os.path.join(source_folder, file)
        doc = fitz.open(path)

        # Iterate through each page in the PDF
        for page_num in range(doc.page_count):
            # Create a new PDF for the current page
            single_page_pdf = fitz.open()

            # Insert the current page into the new PDF
            single_page_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)
            single_file_name = os.path.splitext(file)[0]
            # Save the new PDF to a file
            output_pdf_path = f'{single_file_name}-{page_num + 1}.pdf'
            single_page_pdf.save(os.path.join(target_folder, output_pdf_path))

            # Close the new PDF
            single_page_pdf.close()

# search function
def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 100
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        engine=EMBEDDING_MODEL,
        input=query,    
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]

def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def query_message(
    query: str,
    df: pd.DataFrame,
    model: str,
    token_budget: int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    introduction = ''
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_article = f'"""\n{string}\n"""'
        if (
            num_tokens(message + next_article + question, model=model)
            > token_budget
        ):
            break
        else:
            message += next_article
    return message + question


def completion(
    query: str,
    df: pd.DataFrame,
    engine: str = OPENAI_GPT35_ENGINE,
    model: str = GPT_MODEL,
    token_budget: int = 4096 - 2000,
    print_message: bool = True,
) -> str:
    system_prompt = """
    You are a system assistant. 
    You need answer questions regards content below.
    If you do not know the answer to a question, respond by saying \"I do not know the answer to your question.\"
    """

    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]
    response = openai.ChatCompletion.create(
        engine=engine,
        messages=messages,
        temperature=0
    )
    response_message = response["choices"][0]["message"]["content"]
    return response_message

def conversation(
    df: pd.DataFrame,
    engine: str = OPENAI_GPT35_ENGINE,
    model: str = GPT_MODEL,
    token_budget: int = 800,
    print_message: bool = True,
) -> str:
    
    system_prompt = """
    You are a system assistant. 
    You need answer questions regards content below.
    If you do not know the answer to a question, respond by saying \"I do not know the answer to your question.\"
    """
    conversation=[{"role": "system", "content": system_prompt}]
    while(True):
        user_input = input('User: \n')  
        if 'exit' in user_input.lower():
            exit()

        """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
        message = query_message(query=user_input, df=df, model=model, token_budget=token_budget)
        if print_message:
            print(message)

        conversation.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            engine=engine, 
            messages = conversation,
            temperature=0
        )

        conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        print("\nGPT: \n" + response['choices'][0]['message']['content'] + "\n")

