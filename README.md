Teachable Machine: Decoupled Full-Stack AI Classification System
An enterprise-grade, microservice-based vision classifier engineered to separate real-time data streaming from deep learning computational workloads. This application allows users to train functional machine learning models directly via their browser using image uploads or a live webcam feed—completely containerized and local.

✨ Features
Offline-First Architecture: No cloud dependencies or external API calls, ensuring complete data privacy and local execution.

Dual Data Collection: Upload custom image datasets from local storage or capture samples using a real-time webcam stream.

Transfer Learning Backend: Utilizes a pre-trained MobileNetV3 neural network as a deep feature extractor coupled with a Logistic Regression head for lightning-fast training.

Microservices Architecture: Frontend and backend are completely decoupled, ensuring fault containment.

Containerized Deployment: Multi-container production setup configured natively with Docker and Docker Compose.

📁 Project Directory Structure
Plaintext

my_teachable_machine/
├── dataset/                  # Dynamic local storage for uploaded samples
│   ├── cat/                  # Class folder containing Cat images
│   └── dog/                  # Class folder containing Dog images
├── __pycache__/              # Python compiled runtime cache
├── Dockerfile.backend        # Container configuration for FastAPI backend
├── Dockerfile.frontend       # Container configuration for Streamlit frontend
├── docker-compose.yml        # Multi-container orchestration topology
├── app.py                    # Streamlit UI dashboard & session state
├── main.py                   # FastAPI implementation & ML pipeline
├── model.pkl                 # Serialized binary containing model weights
└── requirements.txt          # 
Unified Python dependencies matrix

🚀 Getting Started
Prerequisites
Make sure you have the following software utilities installed on your host environment:

Docker (Desktop or Engine)

Docker Compose

🛠️ Execution & Deployment Steps
Follow these basic commands in your terminal to initialize the ecosystem from the root folder:

Build and Run the Containers:

Bash
docker-compose up --build
Accessing the Interfaces:

Frontend UI (Streamlit): Open your web browser and navigate to http://localhost:8501

Backend API Documentation (FastAPI Docs): View the interactive Swagger documentation at http://localhost:8000/docs

Stopping the Services:

Bash
docker-compose down
🧠 Technical Workflow & Guardrails
1. Ingestion Pipeline & Collision Safety
User-defined category tokens automatically trigger deterministic OS directory structures on the backend server. To fully eliminate write state race conditions or directory index collisions, incoming image frames are stamped using automated UUIDv4 hexadecimal string encoders.

2. AI Training Engine via Transfer Learning
Training complex deep neural nets from scratch is resource-prohibitive on local endpoints. This design utilizes a frozen pre-trained MobileNetV3 backbone layout as a structural deep feature map extractor. Latent embedding feature vectors are piped into a lightweight multi-class linear classifier matrix head (Logistic Regression) via Scikit-Learn.

3. Real-Time Inference Tensor Pipeline
Live input frames undergo strict pre-processing matrices to secure numerical mapping parity before passing into the model:

Interpolation: Spatial downsizing of images arrays to static [224, 224, 3] configurations.

Normalization: Channel-wise mean and standard deviation array matching backbone tensor bounds.

Activation: Softmax operations mapping raw multidimensional logit arrays into safe probability confidence vectors.

4. Memory State Tracking Guardrails
Stateless REST backends do not persist structural UI contexts natively. Application lifecycles are tracked securely via client-side st.session_state parameters. A strict execution guardrail conditionally locks testing widgets and prediction routes until at least 2 distinct valid dataset directories are populated.

🔬 Closed-Classifier & Out-of-Distribution (OOD) Analysis
Empirical profiling checks under an untrained input matrix (e.g., an Out-of-Distribution Human Face) expose a closed-classifier phenomenon. Because vector spaces are finite to explicitly trained clusters, structural edge distribution and deep texture similarities trigger false high-confidence predictions (e.g., mapping facial tensors to Cat Class with 89.5% confidence limits).

👨‍💻 Project Reviewer Details
Solution Architect: Muhammad Zaid

Platform Implementation: Saylani Mass IT Training (SMIT) Bootcamp

System Status: Deployed, Horizontally Scalable, and Open for Architecture Audit.
