# Text Extraction and Sentiment Analysis API with Observability

This repository contains a project that utilizes the **Anthropic Sonnet LLM** to extract key-value pairs from text and determine the sentiment of the text. The application is implemented using **FastAPI** for building the API, and integrates a full observability stack using **OpenTelemetry**, **Grafana**, **Tempo**, and **Loki**.

## Features
- **Key-Value Extraction**: Automatically extracts structured information from unstructured text inputs.
- **Sentiment Analysis**: Analyzes the sentiment (positive, negative, or neutral) of the provided text.
- **FastAPI Endpoint**: Provides a RESTful interface for easy integration.
- **Observability**:
  - **OpenTelemetry**: Traces and metrics collection.
  - **Grafana**: Visualizes metrics and traces.
  - **Tempo**: Distributed tracing backend.
  - **Loki**: Centralized logging system.

## Technologies Used
- **Programming Language**: Python
- **LLM**: Anthropic Sonnet
- **API Framework**: FastAPI
- **Observability Stack**: OpenTelemetry, Grafana, Tempo, Loki

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Docker (for running observability tools)
- A valid API key or access credentials for Anthropic Sonnet

### Steps
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   Create a `.env` file in the root directory with the following:
   ```env
   ANTHROPIC_API_KEY=<your_api_key>
   OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
   LOG_LEVEL=info
   ```

5. **Run the Application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   The API will be accessible at `http://localhost:8000`.

6. **Start the Observability Stack**
   Use the provided `docker-compose.yml` file to start Grafana, Tempo, and Loki:
   ```bash
   docker-compose up -d
   ```

### API Endpoints
- **POST /extract**
  - **Description**: Extracts key-value pairs and determines sentiment from the input text.
  - **Request Body**:
    ```json
    {
      "text": "<your_text_here>"
    }
    ```
  - **Response**:
    ```json
    {
      "key_values": {
        "key1": "value1",
        "key2": "value2"
      },
      "sentiment": "positive"
    }
    ```

### Observability Configuration
- Access Grafana dashboard at `http://localhost:3000` (default credentials: `admin`/`admin`).
- Logs and traces are automatically collected by Loki and Tempo.

## Contributing
Feel free to submit issues or pull requests to improve the project.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

## Contact
For questions or support, please contact Rahul Jha or open an issue in the repository.

