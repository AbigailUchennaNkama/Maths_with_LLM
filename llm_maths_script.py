from openai import OpenAI
import json
import pandas as pd
import getpass
import os
import re
# Install necessary packages
#pip install -qU langchain-openai langchain

#get api-key
def _get_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_get_env("OPENAI_API_KEY")

#instatiate the openai client
client = OpenAI()

def get_answer(question, model):

    prompt = f"""You are an expert in high school mathematics.
    Please solve the following high school math problem step-by-step. Follow these guidelines:
    1. Read the problem carefully and identify the key information.
    2. Write out the given information and what needs to be found.
    3. Choose the appropriate mathematical concept or formula to solve the problem.
    4. Show each step of your calculation clearly, explaining your reasoning.
    5. Double-check your calculations for accuracy.
    6. Provide the final answer clearly.
    7. Do not leave the final in fraction.
    Here is the problem:
    {question}
    Step-by-step solution:"""

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def extract_numerical_answer(text):
    # Look for patterns like "Final answer: X" or "The answer is X" at the end of the text
    match = re.search(r'(?:final answer|the answer is)[:\s]*([+-]?\d*\.?\d+)', text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    else:
        # If no clear final answer, look for the last number in the text
        numbers = re.findall(r'[+-]?\d*\.?\d+', text)
        return float(numbers[-1]) if numbers else None

def process_row(row, model):
    problem_id = row['problem_id']
    problem_text = row['problem_text']

    llm_reasoning = get_answer(row, model)  # Changed to pass the entire row

    numerical_answer = extract_numerical_answer(llm_reasoning)

    return {
        'problem_id': problem_id,
        'problem_text': problem_text,
        'llm_reasoning': llm_reasoning,
        'answer': numerical_answer

    }


from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(max_workers=6)

def map_progress(max_num_workers, seq, f, model):
    results = []
    pool = ThreadPoolExecutor(max_workers=max_num_workers)
    with tqdm(total=len(seq)) as progress:
        futures = []

        for el in seq:
            future = pool.submit(f, el, model)  # Added model parameter
            future.add_done_callback(lambda p: progress.update())
            futures.append(future)

        for future in futures:
            result = future.result()
            results.append(result)

    return results


def prepare_prompts_and_get_answers(max_workers, df, model):
    rows = df.to_dict(orient='records')
    results = map_progress(pool, rows, process_row, model)
    return pd.DataFrame(results)

"""To run this script make sure to install the necessary packages; pip install -qU langchain-openai langchain.
Then call the function prepare_prompts_and_get_answers(). This function takes in the following arguments:
- number of workers (e.g, 6),
- a dataframe with keys, problem_id (question id) and problem_text (question)
- a prefered model (e.g, "gpt-4o-mini")

"""
