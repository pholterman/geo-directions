from pydantic import BaseModel, Field

regex_str: str = "^(\-?\d+(\.\d+)?),\w*(\-?\d+(\.\d+)?)$"


class RouteInputData(BaseModel):
    from_coordinates: str = Field(None, regex=regex_str)
    to_coordinates: str = Field(None, regex=regex_str)


class RouteInput(BaseModel):
    data: RouteInputData


class RouteResponseData(BaseModel):
    travel_time: int
    travel_distance: int


class RouteResponse(BaseModel):
    data: RouteResponseData
