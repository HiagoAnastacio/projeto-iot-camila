import paho.mqtt.client as mqtt
import ssl
import json
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
import sys
import time

# Adiciona o diretório raiz do projeto ao path para encontrar os módulos da app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal, engine
from app import models, crud

# Carrega variáveis de ambiente e prepara o banco
load_dotenv()
print("Verificando e criando tabelas do banco de dados, se necessário...")
models.Base.metadata.create_all(bind=engine)
print("Tabelas prontas.")

# Configurações do MQTT a partir do .env
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PSWD = os.getenv("MQTT_PSWD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado ao Broker MQTT com sucesso!")
        client.subscribe(f"{MQTT_TOPIC}/#") # Se inscreve em todos os sub-tópicos
        print(f"📡 Inscrito no tópico: '{MQTT_TOPIC}/#'")
    else:
        print(f"❌ Falha na conexão, código de retorno: {rc}")
        if rc == 5:
            print("❗ Erro de autenticação: Verifique seu usuário e senha.")

def on_message(client, userdata, msg):
    print(f"\n📩 Mensagem recebida | Tópico: {msg.topic}")
    db: Session = SessionLocal()
    try:
        payload_str = msg.payload.decode('utf-8')
        print(f"   Payload: {payload_str}")
        data = json.loads(payload_str)

        # Regra para persistir dados de sensores
        if msg.topic.startswith(f"{MQTT_TOPIC}/") and isinstance(data.get("value"), (int, float)):
            variable_name = data.get("variable")
            value = float(data.get("value"))
            unit = " indefinida"

            if variable_name == "temperatura":
                unit = "°C"
            elif variable_name == "umidade":
                unit = "%"
            
            full_topic = f"{MQTT_TOPIC}/{variable_name}"
            
            # Utiliza a camada CRUD para criar o registro
            print(f"   💾 Inserindo em 'sensor_data': {variable_name} = {value}{unit}")
            crud.create_sensor_data(db=db, topic=full_topic, value=value, unit=unit)
            print("   ✅ Dados persistidos no banco de dados com sucesso!")
        
        # Adicione outras regras aqui para outros tópicos (ex: produção, estoque)
        # elif msg.topic.startswith("..."):
        #     ...

        else:
            if not isinstance(data.get("value"), (int, float)):
                 print("   ⚠️ Mensagem ignorada: O valor não é numérico.")
            else:
                 print(f"   ⚠️ Tópico '{msg.topic}' não corresponde a nenhuma regra de armazenamento.")

    except json.JSONDecodeError:
        print("   ❌ ERRO: A mensagem recebida não está em um formato JSON válido.")
    except Exception as e:
        print(f"   ❌ ERRO ao processar ou salvar a mensagem: {e}")
        db.rollback()
    finally:
        db.close()

def run_consumer():
    client_id = f"python-mqtt-consumer-{int(time.time())}"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=client_id)

    client.username_pw_set(MQTT_USER, MQTT_PSWD)
    if MQTT_PORT == 8883:
        client.tls_set(tls_version=ssl.PROTOCOL_TLS)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        print(f"🔌 Tentando conectar ao broker em {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except Exception as e:
        print(f"❌ Uma exceção inesperada ocorreu: {e}")

if __name__ == "__main__":
    run_consumer()