from __future__ import annotations

import json

from langchain_core.prompts import ChatPromptTemplate

from app.schemas import EmployeeProfile, ParsedEmployeeProfile
from app.services.llm_service.clients import llm

EXTRACT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a metadata extraction assistant. Given an employee profile, "
            "extract structured data. Respond ONLY with valid JSON matching this schema:\n"
            '{{"skills": [{{"name": "<skill>", "years_experience": <number|null>, '
            '"description": "<brief description>"}}], '
            '"years_experience": <total years|null>}}',
        ),
        ("human", "{profile_text}"),
    ]
)


async def parse_employee_profile(profile: EmployeeProfile) -> ParsedEmployeeProfile:
    """Use the LLM to extract skills and experience from the employee bio."""
    chain = EXTRACT_PROMPT | llm
    result = await chain.ainvoke({"profile_text": profile.bio})
    try:
        data = json.loads(result.content)
    except (json.JSONDecodeError, AttributeError):
        data = {}
    return ParsedEmployeeProfile(
        **profile.model_dump(),
        skills=data.get("skills", []),
        years_experience=data.get("years_experience"),
    )
