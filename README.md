# jira-helper
Streamlit interface for managing Jira

## Description
A Streamlit web application that seeks to provides an intuitive interface for managing time logging in Jira

## Features
- View daily totals of logged hours
- View list of issues and time logged for the week
- Log time to Jira issues
- Navigate to previous and next weeks

## Setup

### Prerequisites
- Python 3.11+
- Jira account with API access

### Installation
1. Clone the repository:

git clone https://github.com/yourusername/jira-helper.git
cd jira-helper


2. Install required packages:

pip install -r requirements.txt


### Configuration
Create a `.env` file in the root directory with the following variables:

JIRA_SERVER=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@domain.com
JIRA_PASSWORD=your-api-token


To get your API token:
1. Log in to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Copy the token and paste it in your `.env` file

### Running the Application
Execute the following command in your terminal:

streamlit run src/streamlit_app.py


The application will open in your default web browser at `http://localhost:8501`

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
