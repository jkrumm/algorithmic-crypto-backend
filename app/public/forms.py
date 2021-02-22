from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class ExchangeConnection(FlaskForm):
    exchange = SelectField('Exchange', choices=[('kraken', 'Kraken')])
    bot = SelectField('Bot', choices=[('btc_eth', 'BTC ETH Bot')])
    api_key = StringField('Api key', validators=[DataRequired()])
    api_secret = PasswordField('Api secret', validators=[DataRequired()])
    submit = SubmitField('Submit exchange connection',
                         validators=[DataRequired()])
