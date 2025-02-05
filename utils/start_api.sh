#!/bin/bash

uvicorn src.api_gateway_app:app --host 0.0.0.0 --port 8000
