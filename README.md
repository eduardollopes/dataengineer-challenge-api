# Data Engineer Challenge - API

This project aims to consume data from an API and process it using Apache Spark.
The proposal is to create an engine capable of making requests based on the search term, and to save this data for future exploration.

## Repository Structure

- `data/files`: Folder for storing processing results.
- `src/`: Contains the project's source code.
- `utils/`: Utility modules, such as JSON data processing.
- `Dockerfile`: Configuration file for creating the Docker image.
- `main.py`: Main script responsible for consuming the API and processing the data.
- `README.md`: This documentation file.
- `requirements.txt`: List of project dependencies.

## Requirements

Before running the project, make sure you have installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Running the Project

1. Build the Docker image:
    ```bash
   docker build -t challenge-api .
    ```

2. Run the image to perform the processing:
    ```bash
    docker run -v $PWD/data:/app/data challenge-api
    ```

This will start the process of consuming the API, processing the data and saving the results in the `data/files` directory.

## Contributing
Feel free to contribute by opening issues or submitting pull requests.