import io
import random
from flask import Flask, Response, request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import  DataRequired, NumberRange
from wtforms.widgets.html5 import NumberInput

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure

# https://gist.github.com/illume/1f19a2cf9f26425b1761b63d9506331f
app = Flask(__name__)

SECRET_KEY='MatplotlibApp'
app.config['SECRET_KEY'] = SECRET_KEY

class URLForm(FlaskForm):
    num_of_points = IntegerField('Data points:', widget=NumberInput(step=10),
                                 validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit')

@app.route("/", methods=['GET', 'POST'])
def homepage():
    form = URLForm()
    if form.validate_on_submit():
        num_x_points = int(form.num_of_points.data)
    else:
        num_x_points = int(10)

    path = f'/matplot-as-image-{num_x_points}.png'

    return render_template('index.html',  form=form, points=num_x_points, path=path)

@app.route("/matplot-as-image-<int:num_x_points>.png")
def plot_png(num_x_points=50):
    """ renders the plot on the fly.
    """
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(num_x_points)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")

if __name__ == "__main__":
    import webbrowser

    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
