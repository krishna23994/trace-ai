"""OpenAPI 3.0 specification for Trace-AI API"""

swagger_config = {
    "openapi": "3.0.0",
    "info": {
        "title": "Trace-AI API",
        "description": "Log collection and analysis API with trace correlation for debugging applications",
        "version": "1.0.0",
        "contact": {
            "name": "Trace-AI Support"
        }
    },
    "servers": [
        {
            "url": "http://localhost:5000",
            "description": "Development server"
        }
    ],
    "components": {
        "schemas": {
            "LogEntry": {
                "type": "object",
                "required": ["trace_id", "message", "timestamp"],
                "properties": {
                    "trace_id": {
                        "type": "string",
                        "description": "Unique identifier for grouping related logs",
                        "example": "user-login-123"
                    },
                    "message": {
                        "type": "string",
                        "description": "Log message content",
                        "example": "User authentication successful"
                    },
                    "level": {
                        "type": "string",
                        "description": "Log severity level",
                        "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        "default": "INFO"
                    },
                    "timestamp": {
                        "type": "string",
                        "format": "date-time",
                        "description": "ISO 8601 timestamp",
                        "example": "2024-01-01T10:00:00Z"
                    }
                }
            },
            "LogResponse": {
                "type": "object",
                "properties": {
                    "trace_id": {"type": "string"},
                    "logs": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "level": {"type": "string"},
                                "timestamp": {"type": "string"}
                            }
                        }
                    }
                }
            },
            "DeleteResponse": {
                "type": "object",
                "properties": {
                    "deleted": {
                        "type": "integer",
                        "description": "Number of logs deleted"
                    }
                }
            },
            "SummaryResponse": {
                "type": "object",
                "properties": {
                    "trace_id": {
                        "type": "string",
                        "description": "Trace identifier"
                    },
                    "summary": {
                        "type": "string",
                        "description": "Generated summary of log entries"
                    }
                }
            },
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "description": "Error message"
                    }
                }
            }
        }
    },
    "paths": {
        "/v1/logs": {
            "post": {
                "summary": "Store log entry",
                "description": "Store a new log entry with trace correlation",
                "tags": ["Logs"],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LogEntry"},
                            "example": {
                                "trace_id": "user-login-123",
                                "message": "User authentication started",
                                "level": "INFO",
                                "timestamp": "2024-01-01T10:00:00Z"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Log stored successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {"status": {"type": "string"}}
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid request",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            },
            "delete": {
                "summary": "Delete logs",
                "description": "Delete logs by trace ID, timestamp, or all logs",
                "tags": ["Logs"],
                "parameters": [
                    {
                        "name": "trace_id",
                        "in": "query",
                        "description": "Delete logs for this trace ID",
                        "schema": {"type": "string"},
                        "example": "user-login-123"
                    },
                    {
                        "name": "before",
                        "in": "query",
                        "description": "Delete logs before this timestamp",
                        "schema": {"type": "string", "format": "date-time"},
                        "example": "2024-01-01T12:00:00Z"
                    },
                    {
                        "name": "after",
                        "in": "query",
                        "description": "Delete logs after this timestamp",
                        "schema": {"type": "string", "format": "date-time"},
                        "example": "2024-01-01T08:00:00Z"
                    },
                    {
                        "name": "all",
                        "in": "query",
                        "description": "Delete all logs (set to 'true')",
                        "schema": {"type": "string", "enum": ["true"]}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Logs deleted successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/DeleteResponse"}
                            }
                        }
                    },
                    "400": {
                        "description": "Missing or invalid parameters",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/v1/logs/{trace_id}": {
            "get": {
                "summary": "Get logs by trace ID",
                "description": "Retrieve all logs for a specific trace identifier",
                "tags": ["Logs"],
                "parameters": [
                    {
                        "name": "trace_id",
                        "in": "path",
                        "required": True,
                        "description": "Trace identifier to search for",
                        "schema": {"type": "string"},
                        "example": "user-login-123"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Logs retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/LogResponse"}
                            }
                        }
                    }
                }
            },

        },

        "/v1/summarize/{trace_id}": {
            "get": {
                "summary": "Get trace summary",
                "description": "Generate a summary of all logs for a specific trace",
                "tags": ["Analysis"],
                "parameters": [
                    {
                        "name": "trace_id",
                        "in": "path",
                        "required": True,
                        "description": "Trace identifier to summarize",
                        "schema": {"type": "string"},
                        "example": "user-login-123"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Summary generated successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SummaryResponse"}
                            }
                        }
                    },
                    "404": {
                        "description": "No logs found for trace",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        }
    },
    "tags": [
        {
            "name": "Logs",
            "description": "Log storage and retrieval operations"
        },
        {
            "name": "Analysis",
            "description": "Log analysis and summarization"
        }
    ]
}