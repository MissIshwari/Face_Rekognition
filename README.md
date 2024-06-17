AWS Rekognition Lambda function
Functionality - Lambda function to get object from S3, create thumbnails, get detected labels from AWS Rekognition and send SNS notification and add detected Labels to SQS queue.

-	Policies needed for User to create AWS resources – 
1.	AmazonS3FullAccess
2.	AmazonSNSFullAccess
3.	AmazonSQSFullAccess
4.	AWSLambda_FullAccess
5.	IAMFullAccess

-	S3 bucket creation-
1.	Search for s3 in AWS management console
2.	Click on create bucket button, provide a bucket name in the form.
3.	Click on create bucket button and submit.

-	Steps to create SNS topic and subscription –
1.	Search for SNS in AWS management console.
2.	Enter the topic name for eg. AWS recognition topic under Create topic box and click on next step button.
3.	In Create topic form select Standard type for topic
4.	Provide name of SNS topic
5.	Click on Create Topic button.

-	Create subscription for notifications –
1.	Click on the hamburger icon on the left and click on “Subscription”.
2.	Click on create subscription button.
3.	A form will appear to provide details of the subscription, namely SNS topic , protocol and endpoint.
4.	Select the SNS topic ARN created earlier, select email as protocol and in endpoint provide the email which will receive the  notification.
5.	Click on Create Subscription to submit the form.

-	SQS for queuing detected labels – 
1.	Search for SQS in AWS management console
2.	Click on Create Queue button on the page.
3.	Select type as Standard and provide an SQS Queue name
4.	Click on create Queue button

-	IAM policy creation – 
1.	Search for IAM in management console search box.
2.	Create a role and add permissions such as 
•	S3 bucket GetObject, PutObject and ListBucket permissions
•	SNS publish permission
•	SQS sendmessage permission
•	AWS cloudwatch CreateLoggroup, CreateLogstream and PutLogEvents permission
•	AWS recognition detectlabels permission

-	Lambda function creation in AWS– 
1.	Search for lambda in AWS management console searchbox.
2.	Click on create function button.
3.	Select Author from scratch radio button.
4.	Provide function name (name that explains the goal of lambda function)
5.	Runtime as Python 3.12
6.	Under permissions, select use existing role and select the role created earlier.
7.	Click on create function button.

-	Adding trigger source for Lambda function –
1.	In Function overview, click on add trigger.
2.	Select S3 as the source for trigger, select bucket.
3.	Select all object create event under event types.
4.	Enter input/ as the prefix for lambda function trigger.
5.	Select the checkbox for acknowledgement of S3 trigger.
6.	Click on add.

-	Creation of lambda function  on local system -
1.	Create lambda_function.py in local system.
2.	install dependencies in a virtual env
3.	install dependencies and create a zip of the python file and the site packages internal directories and files
4.	Upload the zip to the Code source.
 
-	Adding layer to Lambda function
1.	In Function overview page click on the Layers option
2.	Click on Add layer button.
3.	Under choose layer source, select option of Specify an ARN.
4.	Provide arn of the python package that is needed for the Lambda function.
5.	This lambda function needs Pillow
6.	ARN for Pillow - arn:aws:lambda:ap-south-1:770693421928:layer:Klayers-p312-Pillow:2
7.	Provide the above arn and click on add button

Source to get arn of klayers for python packages to be installed for Lambda function –
https://github.com/keithrozario/Klayers


