from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.core.config import settings

embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
llm = ChatOpenAI(
    model=settings.openai_model,
    temperature=0,
    openai_api_key=settings.openai_api_key,
)
