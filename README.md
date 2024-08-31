# RealTime-KoboDataExtractor
This project implements a solution for extracting data from the KoboToolbox API and storing it in a database. It handles real-time updates for new records and edits through a registered webhook endpoint.

## Project structure

REALTIME-KOBODATAEXTRACTOR/
│
├── app/
│   ├── api/
│   │   └── kobo_client.py
│   ├── database/
│   │   ├── db_connection.py
│   │   └── models.py
│   ├── webhook/
│   │   └── webhook_endpoint.py
│   ├── utils/
│   │   └── logger.py
│   └── main.py
│
├── scripts/
│   └── register_webhook.py
│
├── tests/
│   ├── test_api.py
│   ├── test_database.py
│   └── test_webhook.py
│
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore