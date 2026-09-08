from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    skill_name: str = Field(
        description="Name of the skill to execute"
    )
    message: str = Field(
        min_length=1,
        description="User's request"
    )


class AgentResponse(BaseModel):
    skill_used: str
    response: str
