from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired


class EquipForm(FlaskForm):
    eid = IntegerField('id', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    line = StringField('line')
    lineid = StringField('lineid')
    etype= StringField('type')
    filename = StringField('filename')
    simulator = BooleanField('simulator', render_kw={'style': 'height:1em;'})
    errate = FloatField('errate')
    success = FloatField('success')
    generate = SubmitField('Generate')
    submit = SubmitField('Submit')


class DeleteEquip(FlaskForm):
    eid = IntegerField('id', validators=[DataRequired()])
    delete = SubmitField('Delete')


class ContinuousForm(FlaskForm):
    cid = IntegerField('id', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    eid = IntegerField('eid')
    cmax = FloatField('maxval')
    cmin = FloatField('minval')
    distribution = StringField('distribution')
    posparam1 = FloatField('posparam1')
    posparam2 = FloatField('posparam2')
    negparam1 = FloatField('negparam1')
    negparam2 = FloatField('negparam2')
    submit = SubmitField('Submit')


class DeleteContinuous(FlaskForm):
    cid = IntegerField('id', validators=[DataRequired()])
    delete = SubmitField('Delete')


class DiscreteForm(FlaskForm):
    dd = IntegerField('id', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    eid = IntegerField('eid')
    numlevels = IntegerField('numlevels')
    levels = StringField('levels')
    posprobs = StringField('posprobs')
    negprobs = StringField('negprobs')
    submit = SubmitField('Submit')


class DeleteDiscrete(FlaskForm):
    dd = IntegerField('id', validators=[DataRequired()])
    delete = SubmitField('Delete')


class AlertForm(FlaskForm):
    aid = IntegerField('id', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    eid = IntegerField('eid')
    atype = StringField('type')
    warnlevel = FloatField('warnlevel')
    alarmlevel = FloatField('alarmlevel')
    increasing = BooleanField('increasing', render_kw={'style': 'height:1em;'})
    submit = SubmitField('Submit')


class DeleteAlert(FlaskForm):
    aid = IntegerField('id', validators=[DataRequired()])
    delete = SubmitField('Delete')

