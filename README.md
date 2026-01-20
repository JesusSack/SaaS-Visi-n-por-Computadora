# VisionSaaS - Aesthetic Image Processing MVP

## 📋 Project Overview
This project is a **Software as a Service (SaaS)** MVP backend tailored for the aesthetic market. It focuses on robust **Computer Vision** capabilities to generate visual scenarios from user-uploaded images.

Unlike a standard web application, this solution implements a **non-blocking asynchronous architecture**. Heavy image processing tasks are offloaded to background workers, ensuring high availability and scalability for the API.

### 🚀 Key Features (MVP)
- **High-Res Image Upload:** Supports processing of 2-5 MB images.
- **Asynchronous Processing:** Powered by **Celery** and **Redis** to prevent server blocking.
- **Visual Pipeline:** Automated generation of 3 distinct visual scenarios (Noir, Sketch, Sepia) using **OpenCV**.
- **Scalable Architecture:** Decoupled services (API vs. Worker) ready for future integration with advanced AI models (PyTorch/TensorFlow).
- **Containerized:** Fully Dockerized environment for consistent deployment.

---

## 🏗️ Architecture

The system follows a microservices-inspired architecture to ensure "Clean Code" and separation of concerns:

```mermaid
graph LR
    User["Client / Frontend"] -- Upload Image --> API["FastAPI Backend"]
    API -- Save File --> Storage["Shared Volume / S3"]
    API -- Enqueue Task --> Redis["Redis Broker"]
    Redis -- Pop Task --> Worker["Celery Worker"]
    Worker -- Read Image --> Storage
    Worker -- "Process (OpenCV)" --> Worker
    Worker -- Save Output --> Storage

1.API Service (FastAPI): Handles HTTP requests, validation, and file uploads. It responds immediately with a task_id.

2.Message Broker (Redis): Acts as a queue buffer, managing the load between the API and the Workers.

3.Worker Service (Celery + OpenCV): Consumes tasks from Redis and performs the CPU-intensive image processing in the background.    



🛠️ Tech Stack
Language: Python 3.9

Web Framework: FastAPI (High performance, auto-documented)

Computer Vision: OpenCV (Headless) & NumPy

Task Queue: Celery

Broker: Redis

Containerization: Docker & Docker Compose


📂 Project Structure

.
├── docker-compose.yml    # Service orchestration
├── README.md             # Project documentation
├── app/                  # API Service
│   ├── main.py           # Endpoints & Business Logic
│   └── Dockerfile        # API Container definition
├── worker/               # Background Processing Service
│   ├── tasks.py          # Computer Vision Logic (The "Brain")
│   └── Dockerfile        # Worker Container definition (with CV libs)
└── storage/              # Shared volume for persistence
    └── uploads/          # Generated images location


⚡ How to Run
Prerequisites
Docker

Docker Compose

1.Installation Steps
Clone the repository:
  git clone <repository-url>
cd vision-saas-mvp    


2.Build and Start Services: Run the application in detached mode:
   docker-compose up -d --build


3. Verify Status: Check if all containers (api, worker, redis) are up:
    docker-compose ps  



📖 API Documentation & Usage
Once the container is running, the system auto-generates interactive documentation.

Access the Swagger UI: Open http://localhost:8000/docs in your browser.

Upload an Image:

Use the POST /upload-image/ endpoint.

Upload a .jpg or .png file.

You will receive a JSON response with a task_id and the processing status.

Check Results:

Since this is an MVP, you can verify the generated files via the debug endpoint: http://localhost:8000/debug-files.

Access generated images directly at: http://localhost:8000/storage/uploads/<filename>_scenario_<style>.jpg



# VisionSaaS - Aesthetic Image Processing MVP

## 📋 Project Overview
This project is a **Software as a Service (SaaS)** MVP backend tailored for the aesthetic market. It focuses on robust **Computer Vision** capabilities to generate visual scenarios from user-uploaded images.

Unlike a standard web application, this solution implements a **non-blocking asynchronous architecture**. Heavy image processing tasks are offloaded to background workers, ensuring high availability and scalability for the API.

### 🚀 Key Features (MVP)
- **High-Res Image Upload:** Supports processing of 2-5 MB images.
- **Asynchronous Processing:** Powered by **Celery** and **Redis** to prevent server blocking.
- **Visual Pipeline:** Automated generation of 3 distinct visual scenarios (Noir, Sketch, Sepia) using **OpenCV**.
- **Scalable Architecture:** Decoupled services (API vs. Worker) ready for future integration with advanced AI models (PyTorch/TensorFlow).
- **Containerized:** Fully Dockerized environment for consistent deployment.

---

## 🏗️ Architecture

The system follows a microservices-inspired architecture to ensure "Clean Code" and separation of concerns:

```mermaid
graph LR
    User[Client / Frontend] -- Upload Image --> API[FastAPI Backend]
    API -- Save File --> Storage[Shared Volume / S3]
    API -- Enqueue Task --> Redis[Redis Broker]
    Redis -- Pop Task --> Worker[Celery Worker]
    Worker -- Read Image --> Storage
    Worker -- Process (OpenCV) --> Worker
    Worker -- Save Output --> Storage
API Service (FastAPI): Handles HTTP requests, validation, and file uploads. It responds immediately with a task_id.

Message Broker (Redis): Acts as a queue buffer, managing the load between the API and the Workers.

Worker Service (Celery + OpenCV): Consumes tasks from Redis and performs the CPU-intensive image processing in the background.

🛠️ Tech Stack
Language: Python 3.9

Web Framework: FastAPI (High performance, auto-documented)

Computer Vision: OpenCV (Headless) & NumPy

Task Queue: Celery

Broker: Redis

Containerization: Docker & Docker Compose

📂 Project Structure
Bash

.
├── docker-compose.yml    # Service orchestration
├── README.md             # Project documentation
├── app/                  # API Service
│   ├── main.py           # Endpoints & Business Logic
│   └── Dockerfile        # API Container definition
├── worker/               # Background Processing Service
│   ├── tasks.py          # Computer Vision Logic (The "Brain")
│   └── Dockerfile        # Worker Container definition (with CV libs)
└── storage/              # Shared volume for persistence
    └── uploads/          # Generated images location
⚡ How to Run
Prerequisites
Docker

Docker Compose

Installation Steps
Clone the repository:

Bash

git clone <repository-url>
cd vision-saas-mvp
Build and Start Services: Run the application in detached mode:

Bash

docker-compose up -d --build
Verify Status: Check if all containers (api, worker, redis) are up:

Bash

docker-compose ps
📖 API Documentation & Usage
Once the container is running, the system auto-generates interactive documentation.

Access the Swagger UI: Open http://localhost:8000/docs in your browser.

Upload an Image:

Use the POST /upload-image/ endpoint.

Upload a .jpg or .png file.

You will receive a JSON response with a task_id and the processing status.

Check Results:

Since this is an MVP, you can verify the generated files via the debug endpoint: http://localhost:8000/debug-files.

Access generated images directly at: http://localhost:8000/storage/uploads/<filename>_scenario_<style>.jpg

🔮 Future Expansion
This architecture is designed to grow:

New Algorithms: The worker logic is isolated. Switching from OpenCV to Stable Diffusion or PyTorch requires zero changes to the API code.

Scalability: To handle more traffic, you can simply spawn more Worker containers (docker-compose up -d --scale worker=3) without changing the code.

Storage: The storage volume can be easily swapped for an AWS S3 bucket for production.