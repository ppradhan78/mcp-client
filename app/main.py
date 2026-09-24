from fastapi import FastAPI, HTTPException

from app.models import WeatherRequest
from app.mcp_client import MCPClientService


app = FastAPI(
    title="FastAPI MCP Client",
    description="FastAPI REST API that calls an MCP Server",
    version="1.0.0"
)


mcp_client = MCPClientService()


@app.get("/health")
async def health():

    return {
        "status": "UP",
        "mcp_server": mcp_client.server_url
    }


@app.get("/weather")
async def get_weather(
    city: str,
    country_code: str
):
    """
    Swagger
        ↓
    FastAPI
        ↓
    MCP Client
        ↓
    MCP Server
        ↓
    get_weather tool
    """

    try:

        result = await mcp_client.call_tool(
            "get_weather",
            {
                "city": city,
                "country_code": country_code
            }
        )

        return result

    except Exception as ex:

        raise HTTPException(
            status_code=502,
            detail=f"MCP Server error: {str(ex)}"
        )


@app.post("/weather")
async def post_weather(
    request: WeatherRequest
):

    try:

        result = await mcp_client.call_tool(
            "get_weather",
            {
                "city": request.city,
                "country_code": request.country_code
            }
        )

        return result

    except Exception as ex:

        raise HTTPException(
            status_code=502,
            detail=f"MCP Server error: {str(ex)}"
        )