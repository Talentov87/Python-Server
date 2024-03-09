import os

if not os.path.exists('db'):
    os.makedirs('db')
# exit()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# JSON string representing your service account credentials
service_account_info = {
"type": "service_account",
  "project_id": "talentov-jay",
  "private_key_id": "861cf6557ee9b2f6f6a2a373ea00bf28fe47e318",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCbSnoHQIH61KtU\ntigxWmdQOL0qtZ8JUqDsjHq+ic91szt9aj+r5MwFmHy1YeP1fbtdJ7zMwD3XBJp/\n/bxWesRYC3i73SM7Eu8hcjdWdBHpZeFIyoCSEaDTpGCsK9N+M7WbOCxF41bGpbYq\nCqeveEmV3sxLmHJfacvY3m0X+C1c6WIywH1mCFuR8YAJfq39DFvvaLr2OQ7t1SG5\nu2PNOt1qbNlVF0WWJzryUF+ZO7wWHLbMFFM0igTVPA28/Vmz3vf1Gp/9dWkCeFk9\nyswkf3l4/lslYxH7zjvXPfdrGU+RiMlK7+9uGEdPeNAazjFiTPEmCFDw8ET/b2bs\nPLXnRryXAgMBAAECggEAA1BTC02SmH4qS8v5TphNxRX432zxwFqtiW6z/dXmAe55\nsgLu6eWffu0SmDJHEYmF0oaTDlF54Fk+TMXm23eSMgjIokWlR1DvnmiYCrW+Xhso\n9AsyNCvBIVMMJxBmWnaTBQVtWG5x/xoxKXOBwYpRE6wl8uUFZ8jTq0SP0mee3DEs\nP0ejK2DSuG/kyO0C0kd4yWLbQqXxMDowsZo09BWdbVrPaTQWwntVPfocWav+ni5C\nwwnIuUS4c9+mr/dvofHbsjab0PozZ4vhv8QGZb//mrIzB+BOB8nNtU3xffF8yBGJ\nDQpyEUyH6kJ3eo8hr63C8gQXpGxCrD1HX5bJnemEiQKBgQDIy2QrVQ2punUjrBHh\nkwBBfK0itxXbI5XW5imMO99XEG9WBGDWc3Aqc6mPp+a0kvZE2rYdOStoG3NqTznq\n5sadYuZeqJI17zOPMpXx9HGDbeGRx3hY/DH+qIB+u5j1VNXYNidwWmsyNe69jb2K\namOEey+GjOQ5rgIYm6KJR/l+mQKBgQDF/GMaUuE7cz5D3mxjGwGQ0W/IqdIMT5+v\nLXeQTofSUv2lug9QL8lUKu6CXi+KurqjISLx989skMLE/1wUwsEaZdl0kh2debnj\npOvIv1AR7GU78cMzQtI9h2bVPV8WUGkmPoUc6mEq6+OiJs9B3b6oqHXSQmIPzYvD\nfj6cKBwCrwKBgG2ghkcWP8hsEapxNq4GuTwH2us6NIeZbSSQMxzqT2zUf0TiTRCo\npBO5ZFkXXWE3X5eGJanc3bMQUbo4GTID32psZcRGmtUxjN/gyXb5c8RDCMWztyQ2\nRQF5c/Y9bCx9redG4c94vlACnB8HtPVOUpkxPGhkofJP67sNtfbnwfL5AoGAJSoB\nOFnCabRyRa8kzV2uZ47I2vP1t9XidbGlNfNnz3VAo7FPWo/9zMzaRKKFbhcrHaAE\nvUL1Lr3lsbD1ifgc42Wm8hjTclH9MNwuXlp7H0Iuppf1OlQavu4BwZlplfi2JDWs\nKwdcAgCRlEiQsx56wZINu9A2NB0zVRkHi6yDxYUCgYEAqG6MAWNFgBBTW8bS76Oy\nI6bn9545rRz4tCn7Bj6WOyt0HyxiGGhU+Gp1aCzy13TtgvSXR0BQM1NTBbo93Zfu\nPN2iLLbTiMppepJhYU63uL1kMHevj7632VEC1RmW4OaRGBd75KyQq8OKdK9iENgD\nchBZL/SQhZQp0g4fLIDPF4g=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-nwcpz@talentov-jay.iam.gserviceaccount.com",
  "client_id": "104083996773156235474",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-nwcpz%40talentov-jay.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Initialize Firebase Admin SDK with the service account info
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

print("USERS".center(20,"-"))
import user.step1 as userFetch
import user.step2 as userStore

userFetch.run(db)
userStore.run()


print("JOBS".center(20,"-"))
import job.step1 as jobFetch
import job.step2 as jobStore

jobFetch.run(db)
jobStore.run()


print("COMPANY".center(20,"-"))
import comp.step1 as compFetch
import comp.step2 as compStore

compFetch.run(db)
compStore.run()


print("CVS".center(20,"-"))
import cv.step1 as cvFetch
import cv.step2 as cvStore

cvFetch.run(db)
cvStore.run()


print("SPOC".center(20,"-"))
import spoc.step1 as spocFetch
import spoc.step2 as spocStore

spocFetch.run(db)
spocStore.run()

