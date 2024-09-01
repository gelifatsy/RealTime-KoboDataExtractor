Here's the converted README.md in proper markdown format:

```markdown
# Real-Time Kobo Data Extractor

This project is a FastAPI-based application that handles real-time data extraction from a webhook, processes the data, and stores it in a PostgreSQL database. The application is deployed on Render, ensuring seamless communication for webhook submissions.

## Project Overview

- **API Framework**: FastAPI
- **Database**: PostgreSQL
- **Deployment**: Render
- **Data Handling**: SQLAlchemy for ORM, Pydantic for data validation and serialization, and Pandas for data analysis.

## Folder Structure

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
├── notebooks/             # Jupyter notebooks for data analysis
│   └── data_analysis_notebook.ipynb
├── Dockerfile             # For containerization
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md              # Documentation
└── .gitignore             # Ignore files
```

## How to Use the API

### Running the Application Locally

1. **Clone the Repository**: Clone this repository to your local machine.

   ```bash
   git clone https://github.com/gelifatsy/RealTime-KoboDataExtractor.git
   ```

2. **Install Dependencies**: Navigate to the project directory and install the required dependencies.

   ```bash
   cd RealTime-KoboDataExtractor
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**: Create a `.env` file in the root directory and add your environment variables (e.g., `DATABASE_URL` for connecting to PostgreSQL).

4. **Run the Application**: Use Uvicorn to start the FastAPI application.

   ```bash
   uvicorn app.webhook.webhook_endpoint:app --reload
   ```

5. **Access the Application**: The application will be running on `http://localhost:8000`.

## How to Use the API

The application is deployed and accessible via a public endpoint. You don't need to run it locally to use it.

### API Endpoints

- **POST /webhook**: Receives real-time data from the webhook and stores it in the database.
  - Endpoint: `https://realtime-kobodataextractor.onrender.com/webhook`
  - Method: POST
  - Content-Type: application/json
  - Example request:
    ```bash
    curl -X POST https://realtime-kobodataextractor.onrender.com/webhook \
    -H "Content-Type: application/json" \
    -d '{"key": "value", "data": "example"}'
    ```

- **GET /submissions**: Retrieves all stored submissions.
  - Endpoint: `https://realtime-kobodataextractor.onrender.com/submissions`
  - Method: GET
  - Example request:
    ```bash
    curl https://realtime-kobodataextractor.onrender.com/submissions
    ```

## Tools Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **SQLAlchemy**: An SQL toolkit and ORM for Python, used for database interactions.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **PostgreSQL**: A powerful, open-source relational database system.
- **Pandas**: Python data analysis library, used for manipulating and analyzing data.
- **Render**: Platform-as-a-Service (PaaS) for deploying and hosting the application.
- **Docker**: Used for containerization (optional).

## How to Contribute

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**: Fork this repository to your GitHub account.

2. **Create a Branch**: Create a new branch for your feature or bug fix.

   ```bash
   git checkout -b feature-name
   ```

3. **Make Changes**: Make your changes in the new branch.

4. **Test Your Changes**: Ensure that all existing tests pass and add new tests if necessary.

5. **Commit Your Changes**: Commit your changes