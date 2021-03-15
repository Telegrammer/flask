from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, DateTimeField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = IntegerField('Team leader id', validators=[DataRequired()])
    jobs = StringField("Jobs")
    work_size = IntegerField("Work size")
    collaborators = StringField("Collaborators")
    is_finished = BooleanField('Is finished')
    submit = SubmitField('Submit')
