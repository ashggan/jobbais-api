# Job bais ML model API

- The Job Bias ML Model API is a publicly accessible API built using Python Flask. This API serves as an interface for interacting with a machine learning model that aims to detect bias in job descriptions.

## Setup and Installation

- Clone the repository to your local machine.
- Install the required dependencies by running
  `pip install -r requirements.txt.` .
- Run the Flask application using flask run
  `flask --app main run --reload`.
- The API will be accessible at http://localhost:5000/process .
  [POST] Content-Type: application/json
  Body Request
  `{
"text": "We are seeking a highly motivated individual to join our dynamic team. Must have 5+ years of experience in software development."
// add you job descriptiion
  }`

## Contributing

- Contributions to the Job Bias ML Model API project are welcome. If you identify any issues or have suggestions for improvements, please submit a pull request or open an issue in the project repository.
