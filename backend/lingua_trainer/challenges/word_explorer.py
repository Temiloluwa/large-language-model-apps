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


def stream_examples(response):
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
        Given a German word, generate {num_sent} sentences with the word.
        First provide a contextual scenario in English, then generate the sentence in German.
        The sentences must vary in meaning, conjugated tense, tone (passive or active tone), and quantity (singular or plural) of the word.
        Avoid using the praeteritum; instead, use partizip II.

        Output Format (comma-separated JSON format):
        
        context: <A series of sentences in English describing a scenario for which the generated sentence is applicable>
        german sentence: <A sentence that was generated based on the supplied German word>
        english translation: <Direct translation of the generated sentence to English>

        German Word: {word}
    """)

    messages=[system_prompt(), user_prompt(word=german_word, num_sent=number_of_sentences)]
    response = OpenAI.prompt(messages, temperature, stream=True)
    
    return response