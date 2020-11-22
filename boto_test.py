import boto3
from botocore.handlers import disable_signing
resource = boto3.resource('s3')
resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
bucket = resource.Bucket('adafruit-circuit-python')

for item in bucket.objects.filter(Prefix="bin/circuitplayground_express/en_US/"):
    print(item.key)
