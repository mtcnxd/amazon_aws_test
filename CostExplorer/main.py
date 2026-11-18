import boto3
import config
from datetime import date, timedelta
from collections import defaultdict

# Conectar con AWS
session = boto3.Session(
    region_name="us-east-1",
    aws_access_key_id=config.aws_access_key_id, 
    aws_secret_access_key=config.aws_secret_access_key
)

# CostExplorer client
client = session.client("ce")

# Periodo: desde el primer día del mes hasta hoy
today = date.today()
start = today.replace(day=1)
end = today + timedelta(days=1)

try:
    # Consultar costos agrupados por servicio
    response = client.get_cost_and_usage(
        TimePeriod={
            "Start": start.isoformat(),
            "End": end.isoformat()
        },
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[
            {
                "Type": "DIMENSION",
                "Key": "SERVICE"
            }
        ]
    )

    # Procesar resultados
    services = defaultdict(float)
    currency = "USD"

    for period in response["ResultsByTime"]:
        for group in period["Groups"]:
            service = group["Keys"][0]
            metric = group["Metrics"]["UnblendedCost"]

            services[service] += float(metric["Amount"])
            currency = metric["Unit"]

    # Mostrar resultados
    total = sum(services.values())

    print(f"\nConsumo AWS: {start} - {today}")
    print("-" * 50)

    for service, amount in sorted(
        services.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{service:35} {amount:10.4f} {currency}")

    print("-" * 50)
    print(f"{'TOTAL':35} {total:10.4f} {currency}")

except Exception as error:
    print(f"Error: {error}")