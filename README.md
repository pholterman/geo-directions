# geo-directions-api
## Installation

### Create conda environment
```commandline
conda create -n geo-directions-api python=3.9
```

After creation:
```commandline
conda activate geo-directions-api
```

Install packages:
```commandline
pip install -r requirements.txt
```

Create .env file from `.env.example`

## Run FastAPI

```commandline
uvicorn src.api:app
```

## API call
endpoint:
```
http://127.0.0.1:8000/travel-time/
```

example request body:
```json
{
    "data":{
        "from_coordinates": "52.5166349,6.0861221",
        "to_coordinates": "52.5129654,6.0917158"
    }
}
```

example response body:
```json
{
    "data": {
        "travel_time": 600,
        "travel_distance": 1000
    }
}
```