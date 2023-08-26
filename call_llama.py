from typing import Dict
from langchain import PromptTemplate, SagemakerEndpoint
#from sagemaker_endpoint import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler
from langchain.chains.question_answering import load_qa_chain
import json

from langchain.docstore.document import Document
example_doc_1 = """
Peter and Elizabeth took a taxi to attend the night party in the city. While in the party, Elizabeth collapsed and was rushed to the hospital.
Since she was diagnosed with a brain injury, the doctor told Peter to stay besides her until she gets well.
Therefore, Peter stayed with her at the hospital for 3 days without leaving.
"""

docs = [
    Document(
        page_content=example_doc_1,
    )
]

query = """How long was Elizabeth hospitalized?
"""

prompt_template = """Use the following pieces of context to answer the question at the end.

{context}

Question: {question}
Answer:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
        input_str = json.dumps({prompt: prompt, **model_kwargs})
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json[0]["generated_text"]

SagemakerEndpoint.model_kwargs = {'custom_attributes':'accept_eula=true'}

content_handler = ContentHandler()
llm = SagemakerEndpoint(
        endpoint_name="meta-textgeneration-llama-2-7b-2023-08-26-18-08-09-987",
        credentials_profile_name="temmie",
        region_name="us-east-1",
        model_kwargs={"temperature": 1e-10},
        content_handler=content_handler,
        endpoint_kwargs={"CustomAttributes": 'accept_eula=true'}
        #custom_attributes="accept_eula=true"
    )
#llm._endpoint_kwargs = {"custom_attributes":"accept_eula=true"}
chain = load_qa_chain(
    llm=llm,
    prompt=PROMPT,
)

chain({"input_documents": docs, "question": query}, return_only_outputs=True)