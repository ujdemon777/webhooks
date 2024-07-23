


import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import jwt
import requests
import logging
import azure.functions as func
import json
# from azure_func_fastapi import AzureFunctionsASGI


# Base model for webhook payloads
class WebhookPayload(BaseModel):
    id: str
    activityId: str
    publisherId: str
    offerId: str
    planId: str
    quantity: int
    subscriptionId: str
    timeStamp: str
    action: str
    status: str
    operationRequestSource: str
    subscription: dict



def main(req: func.HttpRequest) -> func.HttpResponse:  
    try:  
        data = req.get_json()  
        payload = WebhookPayload(**data)  
    except ValueError:  
        return func.HttpResponse("Invalid payload", status_code=400)  
      
    event_action = payload.action  
      
    if event_action == "ChangePlan":  
        handle_change_plan(payload)  
    elif event_action == "ChangeQuantity":  
        handle_change_quantity(payload)  
    elif event_action == "Renew":  
        handle_renew(payload)  
    elif event_action == "Suspend":  
        handle_suspend(payload)  
    elif event_action == "Reinstate":  
        handle_reinstate(payload)  
    elif event_action == "Unsubscribe":  
        handle_unsubscribe(payload)  
    else:  
        return func.HttpResponse("Unknown event action", status_code=400)  
      
    return func.HttpResponse(json.dumps({"message": "Event processed successfully"}), status_code=200) 

    

async def handle_change_plan(data):
  
    subscription_id = data["subscriptionId"]
    new_plan_id = data["planId"]
    old_plan_id = data["subscription"]["planId"]
    
    logging.info(f"Changing subscription {subscription_id} from plan {old_plan_id} to plan {new_plan_id}")
    
    print(f"Subscription {subscription_id} has changed from plan {old_plan_id} to plan {new_plan_id}")

    return {"message": f"Plan change for subscription {subscription_id} from {old_plan_id} to {new_plan_id} processed successfully"}

async def handle_change_quantity(data):
    subscription_id = data["subscriptionId"]
    new_quantity = data["quantity"]
    old_quantity = data["subscription"]["quantity"]
    
    logging.info(f"Changing subscription {subscription_id} quantity from {old_quantity} to {new_quantity}")
    
    print(f"Subscription {subscription_id} quantity has changed from {old_quantity} to {new_quantity}")

    return {"message": f"Quantity change for subscription {subscription_id} from {old_quantity} to {new_quantity} processed successfully"}





async def handle_renew(data):
    # Implement your logic to handle the Renew event
    pass

async def handle_suspend(data):
    # Implement your logic to handle the Suspend event
    pass

async def handle_reinstate(data):
    # Implement your logic to handle the Reinstate event
    pass

async def handle_unsubscribe(data):
    # Implement your logic to handle the Unsubscribe event
    pass