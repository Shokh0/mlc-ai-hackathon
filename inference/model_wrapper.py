# LLM section import
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# IMPORTS FOR TEXT GENERATION PIPELINE CHAIN
from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain

class AiAssistant:

    def __init__(self,):
        """This method initializes LLM model."""
        ### INITIALIZING LAMINI MODEL
        self.checkpoint = "./model/"
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
        self.base_model = AutoModelForSeq2SeqLM.from_pretrained(self.checkpoint,
                                                                device_map='auto',
                                                                torch_dtype=torch.float32)

        ### INITIALIZING PIPELINE WITH LANGCHAIN
        llm = HuggingFacePipeline.from_model_id(model_id=self.checkpoint,
                                                task = 'text2text-generation',
                                                model_kwargs={"temperature":0.45,"min_length":30, "max_length":350, "repetition_penalty": 5.0})
        template = """{text}"""
        self.prompt = PromptTemplate(template=template, input_variables=["text"])
        self.chat = LLMChain(prompt=self.prompt, llm=llm)

    def create_chat(self):
        return self.chat
