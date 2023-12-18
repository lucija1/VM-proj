# VM-proj: MNIST Digit Classification Web Application

VM-proj is a Python Flask web application designed to classify MNIST images into digits. Users can register, log in, and utilize the forgot password functionality. Once logged in, users can upload an image containing a digit, and the application will classify the digit.

## Features

- **User Authentication:**
  - Register: Users can create a new account by providing necessary information.
  - Login: Existing users can log in securely.
  - Forgot Password: Users can reset their password if forgotten.

- **Digit Classification:**
  - Users can upload images containing digits.
  - The application uses a trained model to classify the digit in the uploaded image.

## Getting Started

### Prerequisites

- Python 3.11.5
- Docker (optional)

### Installation and Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/lucija1/VM-proj.git
    cd VM-proj
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python run.py
    ```

    The application will be accessible at [http://localhost:5000](http://localhost:5000).

### Docker Support

To build and run the application using Docker:

1. Build the Docker image:

    ```bash
    docker build -t my-flask-app .
    ```

2. Run the Docker container:

    ```bash
    docker run -p 5000:5000 my-flask-app
    ```

    Or, use Docker Compose:

    ```bash
    docker-compose up
    ```

    The application will be accessible at [http://localhost:5000](http://localhost:5000).
