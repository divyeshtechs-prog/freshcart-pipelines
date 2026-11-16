
# FreshCart Pipelines

An end-to-end Data Engineering project demonstrating Git-based collaboration, CI/CD automation, ELT pipeline development, machine learning orchestration, and event-driven messaging.

## Project Overview

This project explores multiple stages of a modern data engineering workflow:

- **Git & CI/CD:** Version control using Git and automated testing through GitHub Actions.
- **FreshCart ELT:** Extracting, cleaning, validating, deduplicating, and enriching order data.
- **Machine Learning:** Building and evaluating an Iris classification pipeline using Mage and Scikit-learn.
- **Event Streaming:** Implementing real-time event distribution using RabbitMQ topic exchanges.
- **Testing:** Validating data transformations and event routing using Pytest.

## Repository Structure

```text
freshcart-pipelines/
│
├── elt/
│   ├── src/
│   │   ├── mock_data.py
│   │   ├── extract.py
│   │   ├── normalize.py
│   │   ├── load_bronze.py
│   │   ├── transform_silver.py
│   │   ├── deduplicate.py
│   │   ├── load_silver.py
│   │   ├── enrich_fx.py
│   │   ├── enrich_customer.py
│   │   ├── enrich_pincode.py
│   │   ├── load_enriched.py
│   │   └── build_gold.py
│   ├── data/
│   └── tests/
│
├── iris_project/       # Mage Iris classification pipeline
│   ├── data_loaders/
│   ├── transformers/
│   └── pipelines/
│
├── stream/
│   ├── dispatcher.py
│   └── driver.py
│
├── tests/
│   ├── test_prepare_data.py
│   ├── test_etl_pipeline.py
│   └── test_stream_routing.py
│
├── .github/
│   └── workflows/
│
├── .gitignore
├── requirements.txt
└── README.md
```

The Mage project is included in `iris_project/`, containing pipeline metadata and all six block definitions.

## Technologies Used

| Area | Technologies |
|---|---|
| Programming | Python |
| Version Control | Git, GitHub |
| CI/CD | GitHub Actions |
| Data Warehouse | Snowflake SQL |
| Machine Learning | Mage, Scikit-learn |
| Messaging | RabbitMQ, Pika |
| Testing | Pytest |
| Containerization | Docker |

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/divyeshtechs-prog/freshcart-pipelines.git
cd freshcart-pipelines
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Part A: Git and CI/CD

The project uses Git for version control and GitHub Actions for continuous integration.

The CI workflow automatically runs automated tests when changes are pushed to GitHub.

Key activities:
- Repository initialization and structured commits.
- Git push and pull operations.
- Automated testing with Pytest.
- GitHub Actions workflow execution.

## Part B: FreshCart ELT Pipeline

The FreshCart pipeline demonstrates a Bronze-Silver-Gold data architecture.

### Pipeline stages

1. **Extract:** Collect order data from simulated web, mobile, CRM, FX, and pincode sources.
2. **Bronze:** Store raw order data.
3. **Silver:** Normalize records, validate data, and separate rejected records.
4. **Deduplication:** Retain the latest order record, using source priority as a tie-breaker.
5. **Enrichment:** Apply currency conversion, customer-tier history, and geographical information.
6. **Gold:** Calculate revenue and loyalty points and produce an analytics-ready dataset.

The local implementation uses mock source data. Snowflake execution is pending and must be configured and verified separately.

## Part C: Mage Machine Learning Pipeline

The Iris classification workflow uses Mage and Scikit-learn.

Pipeline blocks:

1. `load_iris` – Load the Iris dataset.
2. `prepare_data` – Split the dataset into training and testing sets.
3. `train_model` – Train a Decision Tree classifier.
4. `evaluate_model` – Calculate accuracy, precision, recall, F1-score, and confusion matrix.
5. `save_results` – Save evaluation results as JSON.
6. `feature_importance` – Rank features by their importance.

The model's `max_depth` parameter is evaluated across values from 1 to 5.

## Part D: RabbitMQ Event Streaming

The streaming implementation uses a durable RabbitMQ topic exchange named `rapido-dispatch`.

### Components

- `dispatcher.py` – Publishes ride and food delivery events every two seconds.
- `driver.py` – Creates driver consumers and processes messages from their respective queues.

### Driver routing configuration

| Driver | Routing pattern |
|---|---|
| Ravi | `bangalore.koramangala.*` |
| Priya | `bangalore.indiranagar.*` |
| Arjun | `bangalore.*.ride` |
| Meena | `bangalore.*.food` |
| Karthik | `chennai.tnagar.food` |
| Control | `bangalore.#` |

The consumer uses manual acknowledgements:
- Valid messages are acknowledged using `basic_ack()`.
- Messages with missing zone information are rejected using `basic_nack(requeue=False)`.

### Running the streaming application

Ensure RabbitMQ is running locally and accessible on port `5672`.

Start the consumers in Terminal 1:

```bash
source .venv/bin/activate
python -m stream.driver
```

Start the dispatcher in Terminal 2:

```bash
source .venv/bin/activate
python -m stream.dispatcher
```

RabbitMQ Management UI:

```text
http://localhost:15672
```

## Running Tests

Run the complete automated test suite:

```bash
python -m pytest -v
```

Run individual test modules:

```bash
python -m pytest tests/test_prepare_data.py -v
python -m pytest tests/test_etl_pipeline.py -v
python -m pytest tests/test_stream_routing.py -v
```

## Author

**Divyesh Shivdas Swarge**

B.Tech – Computer Science and Engineering  
IIITDM Jabalpur

GitHub: https://github.com/divyeshtechs-prog
Portfolio: https://divytechs.vercel.app
