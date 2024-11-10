# src/app/core/middleware.py

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict
from typing import Dict
import logging

class AdvancedMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.rate_limit_records: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.logger = logging.getLogger("uvicorn.access")

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = int(time.time())
        
        # Clean up old records
        window_start = current_time - self.window_seconds
        # Remove timestamps older than the window
        old_timestamps = [timestamp for timestamp in self.rate_limit_records[client_ip] if timestamp < window_start]
        for timestamp in old_timestamps:
            del self.rate_limit_records[client_ip][timestamp]
        
        # Increment the count for the current second
        self.rate_limit_records[client_ip][current_time] = self.rate_limit_records[client_ip].get(current_time, 0) + 1
        
        # Calculate total requests in the window
        total_requests = sum(self.rate_limit_records[client_ip].values())
        
        if total_requests > self.max_requests:
            self.logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return Response("Too Many Requests", status_code=429)
        
        # Measure processing time
        start_process = time.time()
        response = await call_next(request)
        process_time = time.time() - start_process
        
        # Add custom headers
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"
        
        # Log the request
        self.logger.info(f"Request to {request.url.path} from {client_ip} completed in {process_time:.4f}s with status {response.status_code}")
        
        return response
