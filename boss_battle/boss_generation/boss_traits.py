"""Boss traits returned from the LLM (enforced structure)"""
from pydantic import BaseModel, Field, field_validator

class BossTraits(BaseModel):
    size: int = Field(..., description="Size of the boss", ge=1, le=3)
    moveSpeed: int = Field(..., description="Movement speed of the boss", ge=1, le=10)
    attackSpeed: int = Field(..., description="Attack speed of the boss", ge=1, le=10)
    attackDamage: int = Field(..., description="Attack damage of the boss", ge=1, le=100)
    attackRange: int = Field(..., description="Attack range of the boss", ge=1, le=10)
    attackType: str = Field(..., description="Type of attack", pattern="^(melee|ranged|magic)$")
    