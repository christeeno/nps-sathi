# NPS Saathi

AI-powered Pension Advisory System providing guidance for the National Pension System (NPS) using Retrieval-Augmented Generation, retirement forecasting models, and decision support logic.

## Project Structure
The project is organized into the following modules:
*   `data/`: Stores raw policy documents, chunks, and FAISS vectors.
*   `rag_engine/`: Document loading, cleaning, chunking, embedding, vector DB logic.
*   `forecasting_engine/`: Rules for retirement simulation and corpus projections.
*   `decision_engine/`: Logic comparing schemes (NPS vs UPS) and asset allocations.
*   `ai_pipeline/`: Intelligent orchestration, routing user intents to the correct capability.
*   `evaluation/`: Scripts for evaluating performance and hallucination rates.
*   `api/`: FastAPI endpoints for web interaction.
*   `utils/`: General helpers and configurations.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/christeeno/nps-sathi.git
    cd nps-sathi
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\Activate.ps1
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```

The API will be available at `http://127.0.0.0:8000`.
