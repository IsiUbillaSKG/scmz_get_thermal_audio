import os
import boto3
from dotenv import load_dotenv

def upload_files(date, belt, side):

    load_dotenv(".env")

    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    session = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3 = session.resource('s3')
    
    # S3 bucket name - replace with your bucket name
    BUCKET_NAME = 'your-bucket-name'
    
    # Local directory path
    source_dir = './inspection_files'
    
    # List to track uploaded files
    uploaded_files = []
    
    try:
        # Check if directory exists
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Directory not found: {source_dir}")
            
        # Walk through the directory
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                local_path = os.path.join(root, file)
                
                # Create S3 key with organized structure
                s3_key = f"{date}/{belt}/{side}/{file}"

                print(local_path, s3_key)

                if file.endswith('.wav'):
                    content_type = 'audio/wav'
                elif file.endswith(('.jpg', '.jpeg')):
                    content_type = 'image/jpeg'
                try:
                    # Upload file to S3
                    s3.meta.client.upload_file(
                    local_path,
                    'scmz-service',
                    s3_key,
                    ExtraArgs={'ContentType': content_type})
                    
                    uploaded_files.append(s3_key)
                except Exception as e:
                    print(e)
                    
        return uploaded_files
        
    except Exception as e:
        print(e)

upload_files('10212024', 'CT32', 'I')