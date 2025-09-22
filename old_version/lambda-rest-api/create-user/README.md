# AWS Lambda Test

Prerequisites:
- a working Docker installation (remember to add your user to the `docker` group on Linux)
- Python 3.12 and pip installed globally (i.e. not in a virtual environment)

To run locally:

1. Install the SAM CLI: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html#install-sam-cli-instructions

2. Create `env.json` in the project root with the following contents:

    ```
    {
        "Parameters": {
            "DB_PASSWORD": "<get this from TJ>"
        }
    }

3. Run `sam build` from the project root.

4. Run `sam local start-api --env-vars ./env.json` from the project root.

5. Navigate to http://127.0.0.1:3000/hello in your browser.
