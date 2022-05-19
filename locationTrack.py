from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import pandas as pd
import utils.calculations

app = Flask(__name__, template_folder='templates')


@app.route('/upload')
def upload_file():
    """
    the initial route which enables the user to upload gps data along with column names associated,
    the html file associated will direct the data to the /visualiser path
    :return: the rendered html template
    """
    return render_template('upload.html')


@app.route('/visualiser', methods=['GET', 'POST'])
def upload_file_1():
    """
    the route which does the mapping of the coordinates along with the speed calculations
    :return: rendered html with both graphs displayed
    """
    if request.method == 'POST':
        f = request.files['file']
        ext = f.filename.split('.')[1]
        lat_name = request.form['lat']
        long_name = request.form['long']
        time_name = request.form['time']
        f.save(secure_filename(f.filename))
        if ext == 'csv':
            df = pd.read_csv(f.filename)
        elif ext == 'xlsx':
            df = pd.read_excel(f.filename)
        else:
            raise AttributeError
        map_json = utils.calculations.generate_map_figure(coordinate_df=df, lat_column_name=lat_name,
                                                          long_column_name=long_name)

        df, average_speed = utils.calculations.calculate_speed(coordinate_df=df, lat_column_name=lat_name,
                                                               long_column_name=long_name,
                                                               time_column_name=time_name)
        speed_graph_json = utils.calculations.generate_speed_graph(coordinate_df=df, time_column_name=time_name,
                                                                   average_speed=average_speed)
        return render_template('map.html', map_json=map_json, speed_graph_json=speed_graph_json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
