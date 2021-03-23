from requests import get, post, delete
from pprint import pprint

job = {
    'id': 2,
    'team_leader': 1,
    'job': 'Образец',
    'work_size': 15,
    'collaborators': '2 and 3',
    'is_finished': True
}
headers = {'Content-type': 'application/json'}

print(post('http://localhost:5000/api/jobs', json=job).json())
print(post('http://localhost:5000/api/jobs', json=job).json())

print(delete('http://localhost:5000/api/jobs/999').json())
print(delete('http://localhost:5000/api/jobs/1').json())

pprint(get('http://localhost:5000/api/jobs').json())
