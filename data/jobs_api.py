import flask
from flask import jsonify, request

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'user.id', 'team_leader', 'job', 'work_size',
                                    'collaborators', 'is_finished', 'start_date', 'end_date'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_news(jobs_id):
    db_sess = db_session.create_session()
    action = db_sess.query(Jobs).get(jobs_id)
    if not action:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': action.to_dict(only=('id', 'user.id', 'team_leader', 'job', 'work_size',
                                        'collaborators', 'is_finished', 'start_date', 'end_date'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished', 'id']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    if db_sess.query(Jobs).filter(Jobs.id == request.json['id']).all():
        return jsonify({'error': 'id already exists'})
    jobs = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def edit_jobs(jobs_id):
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif 'id' in request.json.keys():
        return jsonify({'error': 'You cant change id'})

    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'No found'})

    try:
        jobs.team_leader = request.json['team_leader']
    except KeyError:
        pass
    try:
        jobs.job = request.json['job']
    except KeyError:
        pass
    try:
        jobs.work_size = request.json['work_size']
    except KeyError:
        pass
    try:
        jobs.collaborators = request.json['collaborators']
    except KeyError:
        pass
    try:
        jobs.is_finished = request.json['is_finished']
    except KeyError:
        pass

    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})
