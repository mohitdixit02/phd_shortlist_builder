from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import os

def get_llm():
    """
    Initializes and returns the Meta Llama 3.1 8B model using HuggingFace.
    """
    llm_endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation",
        max_new_tokens=1024,
        temperature=0.4,
        do_sample=True,
        repetition_penalty=1.03,
    )
    
    model = ChatHuggingFace(llm=llm_endpoint)
    return model
