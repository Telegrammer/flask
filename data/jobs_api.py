import flask
from flask import jsonify

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
                [item.to_dict(only=('user.id', 'team_leader', 'job', 'work_size',
                                    'collaborators', 'is_finished', 'start_date', 'end_date'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_news(jobs_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).get(jobs_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': news.to_dict(only=('user.id', 'team_leader', 'job', 'work_size',
                                      'collaborators', 'is_finished', 'start_date', 'end_date'))
        }
    )
