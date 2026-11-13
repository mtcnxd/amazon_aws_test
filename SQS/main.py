import config
from itertools import count
import boto3
import json
from datetime import datetime

queue_url = 'https://sqs.us-east-1.amazonaws.com/204380998201/my_test_queue'

sqs = boto3.client(
    'sqs', 
    aws_access_key_id=config.aws_access_key_id,
    aws_secret_access_key=config.aws_secret_access_key,
    region_name='us-east-1'
)

try:
    for i in range(1, 6):
        mensaje : str = json.dumps({
            'count': i,
            'message': f'This is the message number {i}',
            'created_at': datetime.now().isoformat(),
        })

        '''
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=mensaje
        )
        '''

        # print(f"{response['MessageId']} | Mensaje enviado con exito | count {i}")

    # 2. Recibir mensajes de la cola
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,    # Máximo de mensajes a recibir (rango de 1 a 10)
        WaitTimeSeconds=20         # Long Polling: espera hasta 20 segundos si la cola está vacía (ahorra costos)
    )

    # 3. Verificar si llegaron mensajes
    if 'Messages' in response:
        for message in response['Messages']:
            message_id     = message['MessageId']
            message_body   = message['Body']
            receipt_handle = message['ReceiptHandle']   # ID necesario para borrar el mensaje
            
            print(f"{message_id} | Mensaje recibido: {message_body}")

            # --- AQUÍ VA TU LÓGICA DE PROCESAMIENTO ---
            
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )

            print(f"{message_id} | Mensaje procesado y eliminado correctamente.")

    else:
        print("No hay mensajes nuevos en la cola.")

except Exception as err:
    print(f"An error ocurred: {err}")