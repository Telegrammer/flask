from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, DateTimeField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = IntegerField('Team leader', validators=[DataRequired()])
    jobs = StringField("Jobs")
    work_size = IntegerField("Work size")
    collaborators = StringField("Collaborators")
    start_date = DateTimeField("Start date")
    end_date = DateTimeField("End date")
    is_finished = BooleanField('Is finished')
    submit = SubmitField('Submit')
