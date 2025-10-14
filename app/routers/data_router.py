from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/sensors",
    tags=["Dados dos Sensores"],
)

@router.get(
    "/",
    response_model=List[schemas.SensorData],
    summary="Consulta dados de sensores com filtros",
    description="""
Retorna uma lista com os últimos registros de sensores, ordenados do mais novo para o mais antigo.

Você pode filtrar os resultados usando o parâmetro `topic`.
- **Sem `topic`**: Retorna todos os dados.
- **`topic=temperatura`**: Retorna apenas dados de temperatura.
- **`topic=umidade`**: Retorna apenas dados de umidade.
"""
)
def read_sensor_data(
    skip: int = 0,
    limit: int = 100,
    topic: Optional[str] = Query(None, description="Filtre por parte do nome do tópico (ex: 'temperatura')"),
    db: Session = Depends(get_db)
):
    sensor_data = crud.get_sensor_data(db, skip=skip, limit=limit, topic_filter=topic)
    return sensor_data