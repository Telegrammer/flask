import flask
from flask import jsonify, request

from . import db_session
from .jobs import Jobs
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'email',
                                    'position', 'speciality', 'address'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'email',
                                       'position', 'speciality', 'address'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'email', 'password'
                                                           'position', 'speciality', 'address']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.id == request.json['id']).all():
        return jsonify({'error': 'id already exists'})
    user = User(
        id=request.json['id'],
        email=request.json['email'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address']
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Jobs).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif 'id' in request.json.keys():
        return jsonify({'error': 'You cant change id'})

    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'No found'})

    try:
        user.surname = request.json['surname']
    except KeyError:
        pass
    try:
        user.name = request.json['name']
    except KeyError:
        pass
    try:
        user.position = request.json['position']
    except KeyError:
        pass
    try:
        user.speciality = request.json['speciality']
    except KeyError:
        pass
    try:
        user.address = request.json['address']
    except KeyError:
        pass

    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})
