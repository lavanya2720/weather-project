**WEATHER DATA COLLECTION SYSTEM**
A small, production-minded project that demonstrates core DevOps practices by collecting real-time weather from the OpenWeather API, timestamping it, and storing each record in AWS S3. Includes Infrastructure-as-Code (Terraform), Python code, environment management, simple error handling, and CI scheduling (GitHub Actions).
Terraform is used to create cloud infrastructure consistently.
Python fetches the weather data and handles errors gracefully.
Environment variables keep secrets protected.
GitHub Actions automates the job on a schedule — similar to how production systems run recurring tasks.
S3 storage keeps all your weather records organized over time.

**Project Architecture.**
weather-data-collector/
│
├── src/
│ ├── weather.py
│ ├── utils.py
│ ├── requirements.txt
│ ├── .env.example
│
├── data/ (JSON files generated here)
│
├── infra/ (Terraform infrastructure code)
│ ├── main.tf
│ ├── variables.tf
│ ├── outputs.tf
│
└── README.md

**Setup-**
1.	Create and activate the virtual environment
python3 -m venv venv
           source venv/bin/activate
2.	Install Python dependencies
           pip install -r src/requirements.txt
3.	Set up environment variables
           Inside src/.env - change these variables

**API key**
Get API Key from open weather API Key
Go to google and open weather there you can create an account
Then you can get API Key by default.

**AWS Access Key**
Go to AWS console and search IAM
Create a user.
It will generate AWS Access key and secret access key.

**S3 Bucket**
S3_Bucket_Name= Your Bucket Name
Give a bucket Name.

**Cities**
Add the names of cities for which weather data is required.

4.	Deploy Infrastructure with Terraform
Go to the infra/ folder:
cd infra
terraform init

Terraform will create:
S3 bucket
ACL settings
Public access configuration
Bucket policy

After this step, your bucket is ready to receive uploaded JSON files.
5.	Run the Weather Collector
    cd src
   python3 weather.py
   <img width="1920" height="1080" alt="W1" src="https://github.com/user-attachments/assets/b71e88ba-0a78-40c2-a716-e78db637ed82" />
   <img width="1920" height="1080" alt="W2" src="https://github.com/user-attachments/assets/cfa95da8-694c-457d-a592-70bf2c24846c" />
   <img width="1920" height="1080" alt="W3" src="https://github.com/user-attachments/assets/6fcd3fb0-8d26-4ddc-9a57-a7fc49827e04" />
   <img width="1919" height="757" alt="W" src="https://github.com/user-attachments/assets/5e853043-a628-453f-8b09-e8078f27a027" />
   









 


