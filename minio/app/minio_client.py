import boto3
from botocore.exceptions import NoCredentialsError

# Configuración de boto3 para usar MinIO como endpoint S3
s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",  # URL de tu servidor MinIO
    aws_access_key_id="20WNtrMBh7sWYCBeuRvb",  # Tu clave de acceso
    aws_secret_access_key="pX1fh25JfYMNsC9wreczPaMpuJZEGkg4dIXxv9zR",  # Tu clave secreta
    region_name="us-east-1",  # Puedes usar cualquier región
    use_ssl=False  # Cambia a True si usas HTTPS
)

# Verificar si el bucket existe, y si no, crearlo
def create_bucket(bucket_name: str):
    try:
        # Verificar si el bucket ya existe
        s3_client.head_bucket(Bucket=bucket_name)
    except NoCredentialsError:
        print("Credenciales no válidas")
        raise
    except Exception as e:
        # Si no existe, lo creamos
        s3_client.create_bucket(Bucket=bucket_name)
