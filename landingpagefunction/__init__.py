import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import jwt
import requests
import logging
import azure.functions as func
from jwt.exceptions import ExpiredSignatureError, InvalidAudienceError, InvalidIssuerError


# Your Entra tenant information


SECRET_KEY = "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c" 
TENANT_ID = "85a77b6c-a790-4bcf-8fd6-c1f891dd360b"
CLIENT_ID = "3d066378-5305-45b9-b213-1a9e6bfdcd53"
AUTHORITY_URL = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
OPENID_CONFIG_URL = f"{AUTHORITY_URL}/.well-known/openid-configuration"

# Fetch the JWKS keys
def get_jwks_keys():
    response = requests.get(OPENID_CONFIG_URL)
    jwks_url = response.json()["jwks_uri"]
    response = requests.get(jwks_url)
    return response.json()["keys"]
    
def create_jwt():
    payload = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": 1516239022
    }
    secret_key = "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token



async def main(request: func.HttpRequest) -> func.HttpResponse: 
    token = create_jwt()
    logging.info(f"Token: {token}")
    
    # auth_header = request.headers.get("Authorization")
    # if not auth_header:
    #     raise HTTPException(status_code=401, detail="Missing authorization header")
    
    # token = auth_header.split(" ")[1]
    # logging.info(f"Token: {token}")
    
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], audience=CLIENT_ID, issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0")
        logging.info(f"Payload: {payload}")
        
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidAudienceError:
        raise HTTPException(status_code=401, detail="Incorrect audience claim")
    except InvalidIssuerError:
        raise HTTPException(status_code=401, detail="Incorrect issuer claim")
    except Exception as e:
        logging.error(f"Token validation error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return func.HttpResponse(f"Token is valid. Payload: {payload}", status_code=200)