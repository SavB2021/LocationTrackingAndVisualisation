import pandas as pd
import haversine as hs
import plotly.express as px
import plotly
import json

from haversine import Unit


def calculate_speed(coordinate_df: pd.DataFrame, lat_column_name: str, long_column_name: str,
                    time_column_name: str) -> (pd.DataFrame, float):
    """
    Calculates the moving speed an average given a dataframe with coordinates and matching timestamps
    :param coordinate_df: the dataframe containing the above data
    :param lat_column_name: column name for latitude coordinates
    :param long_column_name: column name for longitude coordinates
    :param time_column_name: column name for timestamps
    :return: the input dataframe with speed calculated along with a single average speed variable
    """
    df_columns = list(coordinate_df.columns)
    if lat_column_name in df_columns and long_column_name in df_columns and time_column_name in df_columns:
        # ensure that the time column is of type date_time
        coordinate_df[time_column_name] = pd.to_datetime(coordinate_df[time_column_name])
        # iterate through df to calculate distance and time delta
        for i in range(0, len(coordinate_df) - 1):
            coordinate_df.at[i + 1, 'distance'] = hs.haversine(
                (coordinate_df.loc[coordinate_df.index[i], lat_column_name],
                 coordinate_df.loc[coordinate_df.index[i], long_column_name]),
                (coordinate_df.loc[coordinate_df.index[i + 1], lat_column_name],
                 coordinate_df.loc[coordinate_df.index[i + 1], long_column_name]), unit=Unit.METERS)

            time = coordinate_df.loc[coordinate_df.index[i + 1], time_column_name] - coordinate_df.loc[
                coordinate_df.index[i], time_column_name]

            coordinate_df.at[i + 1, 'time_delta'] = time.total_seconds()

        coordinate_df = coordinate_df.fillna(0)
        coordinate_df['speed'] = coordinate_df['distance'] / coordinate_df['time_delta']
        average = coordinate_df['speed'].mean()
        return coordinate_df, average
    else:
        raise AttributeError


def generate_map_figure(coordinate_df: pd.DataFrame, lat_column_name: str, long_column_name: str) -> str:
    """
    Generates a figure containing the world map and associated route
    :param coordinate_df: dataframe containing coordinates of route
    :param lat_column_name: column name for latitude coordinates
    :param long_column_name: column name for longitude coordinates
    :return: a json str containing the figure object
    """
    df_columns = list(coordinate_df.columns)
    if lat_column_name in df_columns and long_column_name in df_columns:
        fig = px.line_geo(coordinate_df, lat=lat_column_name, lon=long_column_name)
        fig.update_layout(title='Route On World Map', title_x=0.5, width=1600, height=600)
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json
    else:
        raise AttributeError


def generate_speed_graph(coordinate_df: pd.DataFrame, time_column_name: str, average_speed: float) -> str:
    """
    Generates a line graph of the moving speed associated with the route
    :param coordinate_df: dataframe containing coordinates and speed of route
    :param time_column_name: column name for timestamps
    :param average_speed: a float variable containing the average speed associated with the route
    :return: a json str containing the figure object
    """
    df_columns = list(coordinate_df.columns)
    if time_column_name in df_columns:
        fig2 = px.line(coordinate_df, x=time_column_name, y="speed",
                       title=''.join(['Speed m/s ', '(Average Speed ', str(average_speed), ' m/s)']))
        speed_graph_json = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        return speed_graph_json
    else:
        raise AttributeError
