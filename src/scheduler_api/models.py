from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class CreateReminderRequest(BaseModel):
    fire_at: datetime
    channel_id: str
    guild_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    webhook_url: str | None = None
    bot_callback_url: str | None = None

    @model_validator(mode="after")
    def at_least_one_destination(self) -> "CreateReminderRequest":
        if not self.webhook_url and not self.bot_callback_url:
            raise ValueError("Provide webhook_url or bot_callback_url (or both).")
        return self


class ReminderResponse(BaseModel):
    reminder_id: str
    fire_at: datetime
    channel_id: str
    guild_id: str
    payload: dict[str, Any]
    webhook_url: str | None
    bot_callback_url: str | None
    status: Literal["scheduled", "fired", "failed", "cancelled"]
    retry_count: int
    created_at: datetime


class ReminderListResponse(BaseModel):
    reminders: list[ReminderResponse]
    total: int
    limit: int
    offset: int


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    scheduler: str
    pending_jobs: int
