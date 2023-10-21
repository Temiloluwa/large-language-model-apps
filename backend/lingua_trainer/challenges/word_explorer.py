from lingua_trainer.app.word_explorer import word_explanator, sentence_generator, get_llm
from pydantic import BaseModel

class SentenceRequest(BaseModel):
    word: str
    num_sentences: int
    gpt: str

# Create a FastAPI endpoint
@app.post("/generate-sentences/")
def generate_sentences(request_data: SentenceRequest):
    word = request_data.word
    num_sentences = request_data.num_sentences
    gpt = request_data.gpt
    result = sentence_generator(word, num_sentences, gpt)
    return {"result": result}