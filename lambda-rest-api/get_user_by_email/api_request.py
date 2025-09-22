import json

class ApiRequest:
    @staticmethod
    def extract_body(event) -> dict:
        if isinstance(event['body'], str):
            return json.loads(event['body'])
        elif isinstance(event['body'], dict):
            return event['body']
        return None

    @staticmethod
    def extract_headers(event) -> dict:
        headers = event.get('headers', {})
        if len(headers) > 0:
            return headers
        return None
    
    @staticmethod
    def extract_query_parameters(event) -> dict:
        return event.get('queryStringParameters', {})
