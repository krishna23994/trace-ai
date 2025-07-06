"""
Unit tests for Trace-AI API endpoints
"""
import json


def test_create_log_success(client):
    """Test successful log creation"""
    response = client.post('/v1/logs', 
        json={
            'trace_id': 'test-123',
            'message': 'Test message',
            'level': 'INFO',
            'timestamp': '2024-01-01T10:00:00Z'
        })
    assert response.status_code == 200
    assert json.loads(response.data)['status'] == 'log stored'


def test_create_log_missing_required_fields(client):
    """Test log creation with missing required fields"""
    response = client.post('/v1/logs', json={'trace_id': 'test-123'})
    assert response.status_code == 400
    assert 'required' in json.loads(response.data)['error']


def test_create_log_no_json_body(client):
    """Test log creation without JSON body"""
    response = client.post('/v1/logs')
    assert response.status_code == 415  # Unsupported Media Type


def test_get_trace_logs(client):
    """Test retrieving logs by trace ID"""
    # Create test log
    client.post('/v1/logs', 
        json={
            'trace_id': 'test-456',
            'message': 'Test message',
            'level': 'ERROR',
            'timestamp': '2024-01-01T10:00:00Z'
        })
    
    # Retrieve logs
    response = client.get('/v1/logs/test-456')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['trace_id'] == 'test-456'
    assert len(data['logs']) == 1
    assert data['logs'][0]['message'] == 'Test message'


def test_get_trace_logs_empty(client):
    """Test retrieving logs for non-existent trace"""
    response = client.get('/v1/logs/nonexistent')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['logs']) == 0


def test_summarize_trace_logs(client):
    """Test log summarization"""
    # Create test log
    client.post('/v1/logs', 
        json={
            'trace_id': 'test-789',
            'message': 'Test summary message',
            'timestamp': '2024-01-01T10:00:00Z'
        })
    
    # Get summary
    response = client.get('/v1/summarize/test-789')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'summary' in data
    assert 'test-789' == data['trace_id']


def test_summarize_nonexistent_trace(client):
    """Test summarization for non-existent trace"""
    response = client.get('/v1/summarize/nonexistent')
    assert response.status_code == 404
    assert 'No logs found' in json.loads(response.data)['error']


def test_delete_all_logs(client):
    """Test deleting all logs"""
    # Create test logs
    client.post('/v1/logs', json={'trace_id': 'test-1', 'message': 'msg1', 'timestamp': '2024-01-01T10:00:00Z'})
    client.post('/v1/logs', json={'trace_id': 'test-2', 'message': 'msg2', 'timestamp': '2024-01-01T11:00:00Z'})
    
    # Delete all
    response = client.delete('/v1/logs?all=true')
    assert response.status_code == 200
    assert json.loads(response.data)['deleted'] == 2
    
    # Verify empty
    response = client.get('/v1/logs/test-1')
    assert len(json.loads(response.data)['logs']) == 0


def test_delete_by_trace_id(client):
    """Test deleting logs by trace ID"""
    # Create test logs
    client.post('/v1/logs', json={'trace_id': 'delete-me', 'message': 'msg1', 'timestamp': '2024-01-01T10:00:00Z'})
    client.post('/v1/logs', json={'trace_id': 'keep-me', 'message': 'msg2', 'timestamp': '2024-01-01T11:00:00Z'})
    
    # Delete by trace ID
    response = client.delete('/v1/logs?trace_id=delete-me')
    assert response.status_code == 200
    assert json.loads(response.data)['deleted'] == 1
    
    # Verify deletion
    response = client.get('/v1/logs/delete-me')
    assert len(json.loads(response.data)['logs']) == 0
    
    # Verify other trace still exists
    response = client.get('/v1/logs/keep-me')
    assert len(json.loads(response.data)['logs']) == 1


def test_delete_by_timestamp(client):
    """Test deleting logs by timestamp"""
    # Create test logs with different timestamps
    client.post('/v1/logs', json={'trace_id': 'old', 'message': 'old msg', 'timestamp': '2024-01-01T09:00:00Z'})
    client.post('/v1/logs', json={'trace_id': 'new', 'message': 'new msg', 'timestamp': '2024-01-01T12:00:00Z'})
    
    # Delete logs before 10:00
    response = client.delete('/v1/logs?before=2024-01-01T10:00:00Z')
    assert response.status_code == 200
    assert json.loads(response.data)['deleted'] == 1
    
    # Verify old log deleted, new log remains
    response = client.get('/v1/logs/old')
    assert len(json.loads(response.data)['logs']) == 0
    response = client.get('/v1/logs/new')
    assert len(json.loads(response.data)['logs']) == 1


def test_delete_by_timestamp_missing_params(client):
    """Test delete by timestamp with missing parameters"""
    response = client.delete('/v1/logs')
    assert response.status_code == 400
    assert 'Specify' in json.loads(response.data)['error']