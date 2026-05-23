Teachable Machine: Decoupled Full-Stack AI Classification System
An enterprise-grade, microservice-based vision classifier engineered to separate real-time data streaming from deep learning computational workloads. This architecture ensures strict decoupling, runtime isolation, and multi-container cloud scalability.

System Architecture and Layout
Unlike traditional legacy monolithic single-script AI prototypes, this system is divided into structural microservices communicating across network boundaries via high-performance REST APIs.

Frontend UI Service (Streamlit): Orchestrates real-time browser media streams, handles dynamic client-side layout states, and renders asynchronous frame metrics using clean reactive binding layers.

Backend Inference Engine (FastAPI): Ingests image payloads, dynamically structures server-side dynamic directory file trees, executes model feature maps calculation, and handles real-time learning weights optimization.

Technology Core Infrastructure
Network Gateway: FastAPI (Asynchronous ASGI network engine with automated OpenAPI validation schemas).

Deep Learning Pipeline: PyTorch Core (Multidimensional tensor extraction, mathematical matrix formatting, and weight matrix transformations).

Reactive Frontend Layer: Streamlit Engine (Pythonic UI framework backed by active browser WebSocket streaming loops).

Containerization Topology: Multi-Stage Docker and Compose Orchestration Layer.

Architectural Core Rules and Guardrails
1. File-Tree Optimization and Collision Safety (Milestone 1)
User-defined category tokens automatically trigger deterministic OS directory structures on the backend server. To fully eliminate write state race conditions or directory index collisions, incoming image frames are stamped using automated UUIDv4 hexadecimal string encoders.

2. Transfer Learning Framework Strategy (Milestone 2)
Training complex deep neural nets from scratch is resource-prohibitive on local client endpoints. This design utilizes a frozen pre-trained MobileNetV3 backbone layout as a structural deep feature map extractor. Latent embedding feature vectors are piped into a lightweight multi-class linear classifier matrix head (Logistic Regression) for instant training loops on generic compute environments.

3. Inference Matrix Routing (Milestone 3)
Live input frames undergo strict pre-processing matrices to secure numerical mapping parity:

Interpolation: Spatial downsizing of images arrays to static [224, 224, 3] configurations.

Normalization: Channel-wise mean and standard deviation array matching backbone tensor bounds.

Activation: Softmax operations mapping raw multidimensional logit arrays into safe probability confidence vectors.

4. Memory State Tracking Guardrails (Milestone 4)
Stateless REST backends do not persist structural UI contexts natively. Application lifecycles are tracked securely via client-side st.session_state parameters. A strict execution guardrail conditionally locks testing widgets and prediction routes until at least 2 distinct valid dataset directories are populated, avoiding runtime application memory drops.

Production Container Setup and Initialization
To run this decoupled environment without setting up manual local Python configurations, use the multi-container Docker deployment configuration. This eliminates environmental mismatch across Windows, macOS, and Linux nodes.

Ensure you have Docker and Docker Compose installed on your host system, then execute the orchestration routing terminal command in your terminal:

docker-compose up --build

Once running, the multi-tier microservice architecture endpoints become active:

Frontend UI Gateway: http://localhost:8501

Interactive OpenAPI Docs: http://localhost:8000/docs

Closed-Classifier and Out-of-Distribution (OOD) Analysis
Empirical profiling checks under an untrained input matrix (e.g., an Out-of-Distribution Human Face) expose a closed-classifier phenomenon. Because vector spaces are finite to explicitly trained clusters, structural edge distribution and deep texture similarities trigger false high-confidence predictions (e.g., mapping facial tensors to Cat Class with 89.5% confidence limits).

Project Reviewer Details
Solution Architect: Muhammad Zaid

Platform Implementation: Saylani Mass IT Training (SMIT) Bootcamp

System Status: Deployed, Horizontally Scalable, and Open for Architecture Audit.

🚀 Step 2: Save Kaise Karna Hai? (Commit Changes)
