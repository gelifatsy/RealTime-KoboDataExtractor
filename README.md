### **RealTime KoboDataExtractor: Project Documentation**

#### **1. Overview**
The **RealTime KoboDataExtractor** project is a Python-based system designed to extract, store, and analyze real-time data from KoboToolbox. The project leverages FastAPI for API interactions, SQLAlchemy for database management, and is containerized using Docker for easy deployment.

#### **2. Project Structure**

```plaintext
RealTime-KoboDataExtractor/
│
├── app/
│   ├── api/               # Code for API interaction with KoboToolbox
│   │   └── kobo_client.py
│   ├── database/          # Database connection and ORM models
│   │   ├── db_connection.py
│   │   ├── models.py      # SQLAlchemy models
│   │   └── create_tables.py
│   ├── webhook/           # Webhook handling code
│   │   ├── webhook_endpoint.py
│   │   └── register_webhook.py
│   ├── utils/             # Utility functions (e.g., error handling, logging)
│   │   └── logger.py
│   ├── schemas.py         # Pydantic schemas for data validation and serialization
│   └── main.py            # Main script to run the application
│
├── tests/                 # Unit and integration tests
│   ├── test_api.py        # Tests for API endpoints, including webhook data handling
│   ├── test_database.py   # Tests for database operations, including CRUD actions
│   └── test_webhook.py    # Tests specifically for webhook functionality and response validation
│
├── notebooks/             # Jupyter notebooks for data analysis
│   └── data_analysis_notebook.ipynb
├── Dockerfile             # For containerization
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md              # Documentation
└── .gitignore             # Ignore files

```

#### **3. Setting Up the Project**

**Clone the Repository**
```bash
git clone https://github.com/gelifatsy/RealTime-KoboDataExtractor.git
```

**Install Dependencies**
```bash
cd RealTime-KoboDataExtractor
pip install -r requirements.txt
```

**Set Up Environment Variables**
Create a `.env` file in the root directory with the following content:

```plaintext
Use all actual URLs and tokens with actual values when deploying or running the project. 
```

#### **4. Running the Application**

**Run the Application Locally**
Use Uvicorn to start the FastAPI application:

```bash
uvicorn app.webhook.webhook_endpoint:app --reload
```

Access the application at [http://localhost:8000](http://localhost:8000).

**Extract Data from KoboToolbox**
```bash
python app/api/kobo_client.py
```

#### **5. API Endpoints**

**POST /webhook**
- **Description:** Receives real-time data from the webhook and stores it in the database.
- **Endpoint:** `https://realtime-kobodataextractor.onrender.com/webhook`
- **Method:** POST
- **Content-Type:** application/json
- **Example Request:**

```bash
curl -X POST https://realtime-kobodataextractor.onrender.com/webhook \
-H "Content-Type: application/json" \
-d '{"key": "value", "data": "example"}'
```

**GET /submissions**
- **Description:** Retrieves all stored submissions.
- **Endpoint:** `https://realtime-kobodataextractor.onrender.com/submissions`
- **Method:** GET
- **Example Request:**

```bash
curl https://realtime-kobodataextractor.onrender.com/submissions
```

#### **6. Tools and Technologies Used**
- **FastAPI:** Web framework for building APIs.
- **SQLAlchemy:** ORM for database management.
- **Pydantic:** Data validation and serialization.
- **PostgreSQL:** Relational database system.
- **Pandas:** Data analysis library.
- **Render:** Platform for deploying and hosting the application.
- **Docker:** Containerization for deployment.

#### **7. Testing**
The project includes unit and integration tests located in the `tests/` directory. To run the tests:

```bash
pytest -v tests/test_api.py
```

#### **8. Deployment**
The application is deployed on Render. The webhook URL is configured as per the environment setup in the `.env` file.

---

