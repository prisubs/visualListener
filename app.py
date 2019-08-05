import backend
from wtforms import Form, StringField, SubmitField, validators

from flask import Flask, render_template, request
app = Flask(__name__)

class URLForm(Form):
	url = StringField("Enter a Spotify playlist URL: ", validators=[validators.data_required()])
	submit = SubmitField('Recommend!')

@app.route('/', methods=['POST', 'GET'])
def my_form_post():
	form = URLForm(request.form)
	if request.method == 'POST':
		url = request.form['url']
		result = backend.driver(url)
		title = backend.playlist_title(url)
		return render_template('result.html', r=result, t=title)
	else:
		return render_template('input.html', form=form)

if __name__ == "__main__":
	app.run(debug=True)

# change this