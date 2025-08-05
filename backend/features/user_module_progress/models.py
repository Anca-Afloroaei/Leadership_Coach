from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class UserModuleProgressCreate(BaseModel):
    user_id: str
    module_id: str
    progress_percentage: int = 0  # Progress percentage (0-100)
    status: str  # e.g: "In Progress", "Completed", "On Hold"
    last_accessed: datetime = datetime.now()  # Last time the module was accessed
    notes: Optional[str] = None  # Optional notes or comments about the module

class UserModuleProgressRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    module_id: str
    progress_percentage: int
    status: str  # e.g: "In Progress", "Completed", "On Hold"
    last_accessed: datetime
    notes: Optional[str] = None  # Optional notes or comments about the module
    completed: bool = False  # Whether the module is completed
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None  # Optional completion date if the module is completed



class UserModuleProgressUpdate(BaseModel):
    progress_percentage: Optional[int] = None  # Progress percentage (0-100)
    status: Optional[str] = None  # e.g: "In Progress", "Completed", "On Hold"
    last_accessed: Optional[datetime] = None  # Last time the module was accessed
    notes: Optional[str] = None  # Optional notes or comments about the module
    completed: Optional[bool] = None  # Whether the module is completed
