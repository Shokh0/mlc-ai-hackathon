"""This module includes main method for working with AI assistant model."""

# API import Section
from fastapi import FastAPI
import asyncio
import copy

from inference.model_wrapper import AiAssistant

app = FastAPI(
    title="Inference API for Lamini-77M",
    description="A simple API that use MBZUAI/LaMini-Flan-T5-77M as a chatbot",
    version="1.0",
)

ai_assitant = AiAssistant()
chat = ai_assitant.create_chat()

@app.get('/lamini')
async def lamini(question : str):
    res = chat.run(question)
    result = copy.deepcopy(res)
    return result
