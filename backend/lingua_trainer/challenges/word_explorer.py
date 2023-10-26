###############      
# 
#
# 
# To be copied from  lingua_trainer/app/worder_exploerer.py in docker
################################################################


import re
import os
import json
import openai
from dotenv import load_dotenv
from typing import List, Dict
from queryverse.llm import OpenAI
from queryverse.prompter import SystemPrompter, UserPrompter


def load_env_var(env_name: str = "OPENAI_API_KEY", 
                env_path: str | None = None) -> str:
    """
        Load an environment variable from a .env file
    Args:
        env_name: The name of the environment variable
        env_path: The path to the env file
    
    Returns:
        str: value of the environment variable
    """
    if env_path and os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()
    env_var = os.getenv(env_name, "")
    return env_var

# set api key
openai.api_key = load_env_var(env_path='/Users/t.adeoti/codes-and-scripts/projects/llm_apps/.env')


def json_parser(response: str) -> List[dict]:
    """ parse json response """
    pattern = r'\{[^{}]*\}'
    matches = re.findall(pattern, response)
    data = [json.loads(match) for match in matches]

    return data


def extract_json_in_string(input_string: str) -> str | None:
    """
    Extracts JSON from a given string.

    Args:
        input_string (str): The input string that may contain JSON data.

    Returns:
        str | None: If valid JSON is found in the input string, it is extracted,
                    parsed, and returned as a string. If no JSON is found or if
                    the JSON is invalid, None is returned.
    """
    pattern = r'\{[^{}]*\}'  # Pattern to detect JSON
    match = re.search(pattern, input_string)
    if match:
        matched_text = match.group()
        try:
            # If a match is found, perform final verification with json.loads
            # We do another json.dumps because we want a string output
            json_string = json.dumps(json.loads(matched_text))
        except json.JSONDecodeError:
            json_string = None

        return json_string
    else:
        return None


def stream_json_examples(response):
    """
    Stream JSON Examples from a Generator of Byte Strings.

    Args:
        response (generator): A generator that yields byte strings.

    Yields:
        str: Valid JSON strings extracted from the accumulated chunks.
    """
    accumulated_chunk = ""
    for chunk in response:
        if 'assistant' not in chunk:
            accumulated_chunk += chunk['no_role']

        if '{' in accumulated_chunk and '}' in accumulated_chunk:
            parsed_json = extract_json_in_string(accumulated_chunk)

            if parsed_json:
                yield parsed_json
                accumulated_chunk = ""
    else:
        yield ""


def stream_tokens(response):
    """
    Stream a token at a time.

    Args:
        response (generator): A generator that yields byte strings.

    Yields:
        str: stream a token at a time
    """
    accumulated_chunk = ""
    for chunk in response:
        if 'assistant' not in chunk:
            yield chunk['no_role']


def word_explainer(german_word: str, temperature: float) -> List[Dict[str, str]]:
    """
    Get an explanation and synonyms of a German word.

    Args:
    - german_word (str): The German word to explain and find synonyms for.
    - llm (OpenAI): An instance of OpenAI language model.

    Returns:
    str: a str that can be parsed to a list of dictionaries containing explanation and synonyms.
    
    Each dictionary has the following keys:
    - 'explanation' (str): A simple explanation in English.
    - 'synonyms' (str): Comma-separated synonyms.

    Example:
    >>> german_word = "Haus"
    >>> explanations_and_synonyms = word_explainer(german_word)
    >>> print(explanations_and_synonyms)
    [{'explanation': 'A house is a place where people live.', 'synonyms': 'Haushalt'}]
    """

    system_prompt = SystemPrompter("You are a fluent German speaker that is great at following instructions.")
    user_prompt = UserPrompter("""
        Given a German word, supply the following:
        1. An explanation of the word in English, in very simple terms (like to a child).
        2. Synonyms of the word if they exist.

        Output Format (comma-separated JSON format):
        
        explanation: <Simple explanation like to a child>
        synonyms: <comma-separated synonyms>

        German Word: {word}
    """)

    messages=[system_prompt(), user_prompt(word=german_word)]
    response = OpenAI.prompt(messages, temperature, stream=False)
    
    explanations_and_synonyms = json_parser(response['messages'][0]['assistant'])
    
    return explanations_and_synonyms


def sentence_generator(german_word: str, number_of_sentences: int, temperature: float) -> List[Dict[str, str]]:
    """
    Generate sentences in German based on a given word.

    Args:
    - german_word (str): The German word to base the generated sentences on.
    - number_of_sentences (int): The number of sentences to generate.
    - llm (OpenAI, optional): An instance of the OpenAI language model (default: None).

    Returns:
    List[Dict[str, str]]: A list of dictionaries containing contextual scenarios, German sentences,
    and their English translations.

    Each dictionary has the following keys:
    - 'context' (str): A series of sentences in English describing a scenario for which the generated sentence is applicable.
    - 'german sentence' (str): The sentence generated in German.
    - 'english translation' (str): The direct translation of the generated sentence to English.

    Example:
    >>> german_word = "Haus"
    >>> number_of_sentences = 2
    >>> generated_sentences = json_parser(sentence_generator(german_word, number_of_sentences))
    >>> for sentence in generated_sentences:
    >>>     print(sentence['context'])
    >>>     print("German: ", sentence['german sentence'])
    >>>     print("English: ", sentence['english translation'])
    """

    system_prompt = SystemPrompter("You are a fluent German speaker that is great at following instructions.")
    user_prompt = UserPrompter("""
        Generate sentences in German for a word. 
        Each sentence should include an English contextual scenario followed by the corresponding German sentence.
        Ensure that the sentences differ in meaning, and include varied conjugations for the verbs. 
        Use partizip II instead of praeteritum. Additionally, vary the tense (present, past, future), tone (active or passive), and quantity (singular or plural) of the word.
        [word]: Geehrte
        [number of sentences]: 2
        [context]In a formal business letter, addressing a company's board of directors
        [german]Sehr geehrte Herren Vorstände, Ich möchte Ihnen mitteilen, dass unsere Firma im nächsten Quartal voraussichtlich eine Gewinnsteigerung verzeichnen wird.
        [english]Dear honored board members, I would like to inform you that our company is expected to experience an increase in profits in the next quarter.
        <hr>
        [context]At a prestigious awards ceremony, introducing a well-respected guest speaker.
        [german]Meine sehr geehrten Damen und Herren, It is my great honor to introduce to you Mr. Schmidt, who is renowned as an expert in the field of renewable energy.
        [english]Ladies and gentlemen, Es ist mir eine große Ehre, Ihnen Herrn Schmidt vorstellen zu dürfen, der als Experte auf dem Gebiet der erneuerbaren Energien gilt.
        ##
        [word]: "{word}"
        [number of sentences]: {num_sent}
    """)

    messages=[system_prompt(), user_prompt(word=german_word, num_sent=number_of_sentences)]
    response = OpenAI.prompt(messages, temperature, stream=True, max_tokens=3500)
    
    return response

# german_word = "wirklich"
# number_of_sentences = 3
# temperature = 1
# all_chunks = ""
# for chunk in sentence_generator(german_word, number_of_sentences, temperature):
#     if 'assistant' not in chunk:
#         all_chunks += chunk['no_role']
# print(all_chunks)

