from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Schema base para dados de sensor, usado para leitura e retorno na API
class SensorData(BaseModel):
    id: int
    topic: str
    value: float
    unit: str
    timestamp: datetime

    class Config:
        from_attributes = True

# Schema para criação de um log de produção (exemplo para o futuro)
class ProductionLogBase(BaseModel):
    product_id: str = Field(..., example="PROD-00123")
    status: str = Field(..., example="Completed")
    details: Optional[str] = Field(None, example="Quality check passed.")

class ProductionLogCreate(ProductionLogBase):
    pass

class ProductionLog(ProductionLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True