# How to Set Environment Variables for Credentials:

## Local Environment Setup (e.g., for development or testing):

Set the environment variable using your terminal or IDE. 

### On Linux/macOS, you can use the following command:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
```
### On Windows (using Command Prompt):
```bash
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\credentials.json
```

### Using .env Files (Optional for local development):

If you're using a .env file to manage environment variables, you can create a .env file in the root of your project and add the following line:

Javascript: 
```javascript
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json
```
Python:

If you're using Python, you can load the environment variable using os (this is how the current code is already written):
```python

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"