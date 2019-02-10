import folium
import pandas
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def init_coords(data, col, locator):
    """
    dict -> dict
    :param data: A pandas data type storing proper data.
    :return: A dict with relative coordinates.
    """
    coords = dict()
    for line in data[col]:
        print(line)
        pos = locator.geocode(line)
        coords[line] = (pos.latitude, pos.longitude)
    return coords


def convert_year(year):
    """
    Converts a year in a str with parenthesis to a number.
    :param year: str
    :return: integer
    """
    return int(year[1:5])


def color_creator(year):
    """
    Return a proper color for a year.
    :param year: a year of the movie.
    :return: color in a str format.
    """
    if year < 1980:
        return "red"
    elif 1980 <= year <= 2000:
        return "yellow"
    else:
        return "green"


year_from, year_to = int(input('Enter a start year for search. ')), int(input('Enter a end year for search. '))

geolocator = Nominatim(user_agent='shumakov')
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.01)

data_loc = pandas.read_csv('movies.list', header=0, error_bad_lines=False, encoding='latin-1')
data_school = pandas.read_csv('schools.list', header=0, error_bad_lines=False, encoding='latin-1')
coords_loc = init_coords(data_loc, 'location', geolocator)
coords_school = init_coords(data_school, 'location', geolocator)


map = folium.Map()

loc_group = folium.FeatureGroup(name='Movie Locations And Info')
school_group = folium.FeatureGroup(name='Top Movie Academies')

for i in range(data_loc.shape[0]):
    year = convert_year(data_loc['year'][i])
    if year_from <= year <= year_to:
        loc_group.add_child(folium.CircleMarker(location=[coords_loc[data_loc['location'][i]][0], coords_loc[data_loc['location'][i]][1]],
                                                radius=7,
                                                popup='{} | {} | {}'.format(data_loc['title'][i], data_loc['location'][i], data_loc['year'][i]),
                                                fill_color=color_creator(convert_year(data_loc['year'][i])),
                                                color='white',
                                                fill_opacity=0.5))

for i in range(data_school.shape[0]):
    school_groupo.add_child(folium.Marker(location=[coords_school[data_school['location'][i]][0], coords_school[data_school['location'][i]][1]],
                                      popup='{} | {}'.format(data_school['school'][i], data_school['location'][i]),
                                      icon=folium.Icon()))

map.add_child(loc_group)
map.add_child(school_group)
map.add_child(folium.LayerControl())
map.save('Map.html')
