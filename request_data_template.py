import requests
params = {
    'token': 'b3e22542-30a3-4c63-8abf-ddbbb2d4ea58',
    'graph_id': 1,
    'title': 'Post Title',
    'text': 'so mush text',
}
requests.post('http://127.0.0.1:8000/append_node', data=params)
