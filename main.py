from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ipaddress

app = FastAPI()

# Define a Pydantic model for the response
class IPCheckResponse(BaseModel):
    ip: str
    is_in_range: str

@app.get("/check_ip/", response_model=IPCheckResponse)
async def check_ip_query(ip: str):
    try:
        network_range = ipaddress.ip_network('17.0.0.0/8', strict=False)
        ip_obj = ipaddress.ip_address(ip)
        is_in_network = ip_obj in network_range
        is_in_range = "good" if is_in_network else "not good"
        return {"ip": ip, "is_in_range": is_in_range}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IP address format.")

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

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
