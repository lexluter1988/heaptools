import boto3
from moto.s3 import mock_s3
from moto.ec2 import mock_ec2


class S3Obj(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def save(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.put_object(Bucket='mybucket', Key=self.name, Body=self.value)


def test_my_model_save():
    mock = mock_s3()
    mock.start()

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='mybucket')

    model_instance = S3Obj('steve', 'is awesome')
    model_instance.save()

    body = conn.Object('mybucket', 'steve')
    print(body)

    mock.stop()


def test_create_security_group():
    mock = mock_ec2()
    mock.start()

    conn = boto3.resource('ec2', region_name='us-east-1')
    conn.create_security_group(
        GroupName="vps",
        Description="Security group",
        VpcId='11111')
    mock.stop()


test_create_security_group()

