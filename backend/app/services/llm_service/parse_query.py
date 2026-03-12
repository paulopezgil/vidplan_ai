from __future__ import annotations

import json

from langchain_core.prompts import ChatPromptTemplate

from app.schemas import ParsedQuery
from app.services.llm_service.clients import llm

QUERY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a query-understanding assistant for a talent search engine. "
            "Given a natural-language hiring query, extract filter parameters.\n"
            "Respond ONLY with valid JSON:\n"
            '{{"skill_filters": [{{"name": "<skill>", "min_years": <number|null>}}], '
            '"min_years": <total min years|null>, '
            '"department": "<department>"|null, '
            '"grade": "<grade>"|null, '
            '"location": "<location>"|null, '
            '"semantic_query": "<rephrased query for embedding search>"}}',
        ),
        ("human", "{query}"),
    ]
)


async def parse_query(raw_query: str) -> ParsedQuery:
    """Use the LLM to decompose a hiring query into filters + semantic text."""
    chain = QUERY_PROMPT | llm
    result = await chain.ainvoke({"query": raw_query})
    try:
        data = json.loads(result.content)
    except (json.JSONDecodeError, AttributeError):
        data = {"semantic_query": raw_query}
    return ParsedQuery(**data)
