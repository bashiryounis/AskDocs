from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

# Import routers from services
from src.services.user.user import router as user_router
from src.services.file import router as file_router
from src.services.chat.chat import router as chat_router
from src.services.chat.chat_socket import router as socket_router
from src.core.logging_config import setup_logging

# Initialize logging
setup_logging()

app = FastAPI(
    debug=True,
    title="LangChain Service",
    description="API server providing various functionalities including user operations, file handling, and chat services."
)

# Configure CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Redirect root path to API documentation
@app.get("/", include_in_schema=False)
def root_redirect():
    """
    Redirects the root URL to the API documentation.
    """
    return RedirectResponse(url="/docs/")

# Include routers with specific prefixes and tags for API endpoints
app.include_router(user_router, prefix="/user", tags=["User Operations"])
app.include_router(file_router, prefix="/data", tags=["Data Operations"])
app.include_router(chat_router, prefix="/chat", tags=["Chat Operations"])
app.include_router(socket_router, prefix="/socket", tags=["Socket Testing"])
