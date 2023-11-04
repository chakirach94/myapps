from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import ipaddress

app = FastAPI()

@app.get("/check_ip/")
async def check_ip(ip: str = Query(..., title="IP address to check")):
    try:
        # Define the network range, this is Apple's known IP range
        network_range = ipaddress.ip_network('17.0.0.0/8', strict=False)
        # Create an IPv4 address object
        ip_obj = ipaddress.ip_address(ip)
        # Check if the IP address is within the network range
        is_in_range = ip_obj in network_range
        # Return the result
        return {"ip": ip, "is_in_range": is_in_range}
    except ValueError as e:
        # If there was an error parsing the IP address, raise an HTTPException
        raise HTTPException(status_code=400, detail=str(e))

# Define a Pydantic model to structure the response data
class IPCheckResponse(BaseModel):
    ip: str
    is_in_range: bool

@app.get("/check_ip/{ip}", response_model=IPCheckResponse)
async def check_ip_path(ip: str):
    try:
        network_range = ipaddress.ip_network('17.0.0.0/8', strict=False)
        ip_obj = ipaddress.ip_address(ip)
        is_in_network = ip_obj in network_range
        is_in_range = "good" if is_in_network else "not good"
        return {"ip": ip, "is_in_range": is_in_range}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IP address format.")
