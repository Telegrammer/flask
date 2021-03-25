from requests import get, post, delete, put
from pprint import pprint

job = {
    'id': 2,
    'team_leader': 1,
    'job': 'Образец',
    'work_size': 15,
    'collaborators': '2 and 3',
    'is_finished': True
}

action = {
    'team_leader': 1,
    'job': 'образец',
    'work_size': 15,
    'is_finished': False
}

print(post('http://localhost:5000/api/jobs', json=job).json())
print(post('http://localhost:5000/api/jobs', json=job).json())
print(put('http://localhost:5000/api/jobs/1', json=action).json())

print(delete('http://localhost:5000/api/jobs/999').json())
print(delete('http://localhost:5000/api/jobs/2').json())

pprint(get('http://localhost:5000/api/users').json())
