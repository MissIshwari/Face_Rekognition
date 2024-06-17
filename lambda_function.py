import os
import boto3
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
sns = boto3.client('sns')
sqs = boto3.client('sqs')

def create_thumbnail(image_path):
    with Image.open(image_path) as img:
        img.thumbnail((100, 100))
        thumbnail_io = BytesIO()
        img.save(thumbnail_io, format=img.format)
        thumbnail_io.seek(0)
        return thumbnail_io

def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        
        # Check if the object is in the designated folder
        if not object_key.startswith('input/'):
            continue
        
        # Generate output key for the thumbnail
        output_key = 'thumbnails/' + os.path.basename(object_key) + '.thumbnail.jpg'
        
        # Download the image from S3
        
        # object_key="/"+object_key
        print(object_key)
        print(bucket_name)
        print(record)
        image_object = s3.get_object(Bucket="aws-ishwari-rekog", Key=object_key)
        image_body = image_object['Body'].read()
        
        # Create thumbnail
        thumbnail_io = create_thumbnail(BytesIO(image_body))
        
        # Upload the thumbnail to S3
        s3.put_object(Bucket=bucket_name, Key=output_key, Body=thumbnail_io)
        
        # Analyze image using AWS Rekognition
        response = rekognition.detect_labels(
            Image={'Bytes': image_body},
            MaxLabels=10
        )
        
        # Get detected labels
        detected_labels = [label['Name'] for label in response['Labels']]
        
        # Send detected labels to SNS topic
        sns.publish(
            TopicArn='arn:aws:sns:ap-south-1:515210271098:ishwari-aws-rekog-topic-file-upload',
            Message='Detected labels: {}'.format(', '.join(detected_labels))
        )
        
        # Send detected labels to SQS queue
        sqs.send_message(
            QueueUrl='https://sqs.ap-south-1.amazonaws.com/515210271098/ishwari-aws-rekog-file-upload-queue',
            MessageBody='Detected labels: {}'.format(', '.join(detected_labels))
        )
