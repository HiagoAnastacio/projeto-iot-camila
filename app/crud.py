from sqlalchemy.orm import Session
from . import models
from typing import Optional, List

def get_sensor_data(db: Session, skip: int = 0, limit: int = 100, topic_filter: Optional[str] = None) -> List[models.SensorData]:
    """
    Busca registros de dados de sensores.
    - skip: número de registros a pular.
    - limit: número máximo de registros a retornar.
    - topic_filter: filtra registros cujo tópico contenha a string.
    """
    query = db.query(models.SensorData)
    
    if topic_filter:
        query = query.filter(models.SensorData.topic.like(f"%{topic_filter}%"))
        
    return query.order_by(models.SensorData.id.desc()).offset(skip).limit(limit).all()

def create_sensor_data(db: Session, topic: str, value: float, unit: str) -> models.SensorData:
    """
    Cria uma nova entrada de dados de sensor no banco.
    """
    db_sensor_data = models.SensorData(topic=topic, value=value, unit=unit)
    db.add(db_sensor_data)
    db.commit()
    db.refresh(db_sensor_data)
    return db_sensor_data