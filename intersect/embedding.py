import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken
import time


def get_embedding(client: OpenAI, text: str, model="text-embedding-3-small"):

    if text is None:
        return None
    
    if text == "":
        return None
    
    def num_tokens_from_string(string: str, model="text-embedding-3-small") -> int:
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    if num_tokens_from_string(text) > 8000:
        raise Exception("Text too long")

    res = client.embeddings.create(model=model, input=text, encoding_format="float")

    return res.data[0].embedding


def generate_embeddings(df: pd.DataFrame) -> pd.DataFrame:
    """Generate embeddings for all jobs in the database. Requires a column called 'description'."""

    load_dotenv()
    client = OpenAI()

    start_time = time.time()
    df["embedding"] = df["description"].apply(lambda x: get_embedding(client, x))
    end_time = time.time()

    print(
        f"Generated embeddings for {df.shape[0]} jobs in {end_time - start_time:.2f} seconds"
    )

    return df