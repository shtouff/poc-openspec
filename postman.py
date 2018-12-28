from flask import json

from app import api, app

urlvars = False  # Build query strings in URLs
swagger = True  # Export Swagger specifications

app.config['SERVER_NAME'] = 'localhost:5000'

with app.app_context():
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    print(json.dumps(data))
