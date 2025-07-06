"""
End-to-end integration tests for Trace-AI
Run with: pytest tests/test_e2e.py -m e2e
"""
import pytest


@pytest.mark.e2e
@pytest.mark.skip(reason="E2E tests require manual server setup")
def test_manual_e2e_workflow():
    """Manual E2E test - requires server running on localhost:5000"""
    import requests
    
    BASE_URL = "http://localhost:5000"
    trace_id = "e2e-test-123"
    
    # Store logs
    logs = [
        {"trace_id": trace_id, "message": "User login started", "level": "INFO"},
        {"trace_id": trace_id, "message": "Login successful", "level": "INFO"}
    ]
    
    for log in logs:
        response = requests.post(f"{BASE_URL}/logs", json=log)
        assert response.status_code == 200
    
    # Retrieve logs
    response = requests.get(f"{BASE_URL}/logs/{trace_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data['logs']) == 2
    
    # Get summary
    response = requests.get(f"{BASE_URL}/summarize/{trace_id}")
    assert response.status_code == 200