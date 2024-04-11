import requests
import pandas as pd
import sys
import io

def geopoints(latitude=(-90, 90), longitude=(-180,180), general_variables=None,
              sampling_years=None, sampling_method_types=None, water_depth=None):
    """
    Extracts a table of all the cores in MOSAIC database, as well as the variables the user is interested in
    :param latitude: tuple of latitude extent
    :param longitude: tuple of longitude extent
    :param water_depth: tuple of water depth ranges (positive values)
    :param sampling_years: tuple of sampling years to be included
    :param sampling_method_types: sampling method used to collect the sample, or list of sampling methods used to
     collect the sample
    :param general_variables: list of general variables to be extracted alongside the main metadata
    """
    assert isinstance(latitude, (list, tuple)) and len(latitude) == 2, \
        f'latitude needs to be a 2 element list or tuple specifying the lower and upper limits to be extracted'
    assert isinstance(longitude, (list, tuple)) and len(longitude) == 2, \
        f'longitude needs to be a 2 element list or tuple specifying the lower and upper limits to be extracted'
    assert -90 <= latitude[0] <= 90 and -90 <= latitude[1] <= 90, f'latitude needs to be between -90 and 90, ' \
                                                                  f'not {latitude}'
    assert -180 <= longitude[0] <= 180 and -180 <= longitude[1] <= 180, f'longitude needs to be between -180 and 180,' \
                                                                        f' not {longitude}'
    assert latitude[0] <= latitude[1], f'Provide tuple of latitudes in ascending order, ' \
                                       f'{latitude[0]} needs to be smaller than {latitude[1]}'
    assert longitude[0] <= longitude[1], f'Provide tuple of longitudes in ascending order, ' \
                                         f'{longitude[0]} needs to be smaller than {longitude[1]}'

    url = 'https://mosaicprd.ethz.ch/api/mosaic_app/geopoints'
    params = {
        'latitude': str(latitude) if latitude is not None else None,
        'longitude': str(longitude) if longitude is not None else None,
        'general_variables': str(general_variables) if general_variables is not None else None,
        'sampling_years': str(sampling_years) if sampling_years is not None else None,
        'sampling_method_types': str(sampling_method_types) if sampling_method_types is not None else None,
        'water_depth': str(water_depth) if water_depth is not None else None
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:  # Successful response
        geopoints_data = response.json()
        # Convert to pandas DataFrame
        geopoints_df = pd.DataFrame(geopoints_data)
        return geopoints_df
    else:
        # Print error
        print(f"Error: {response.status_code}")
        return None


# Sample_analyses
def sample_analysis(analyses=None, general_variables=None, material_analyzed=None, sample_depths=None,
                    calculated=False, latitude=(-90, 90), longitude=(-180, 180),
                    sampling_years=None, water_depth=None, sampling_method_types=None,
                    references=True, method=True, method_details=True, calculated_column=True,
                    material_analyzed_column=True):

    # Asserts
    if analyses:
        assert isinstance(analyses, (list, tuple)), f'Provide the analyses as a list'


    url = 'https://mosaicprd.ethz.ch/api/mosaic_app/samples'
    params = {
        'latitude': str(latitude) if latitude is not None else None,
        'longitude': str(longitude) if longitude is not None else None,
        'general_variables': str(general_variables) if general_variables is not None else None,
        'sampling_years': str(sampling_years) if sampling_years is not None else None,
        'sampling_method_types': str(sampling_method_types) if sampling_method_types is not None else None,
        'water_depth': str(water_depth) if water_depth is not None else None,
        'analyses': ','.join(analyses) if analyses is not None else None,
        'material_analyzed': ','.join(material_analyzed) if material_analyzed is not None else None,
        'sample_depths': str(sample_depths) if sample_depths is not None else None,
        'calculated': str(calculated) if calculated is not None else None,
        'references': str(references) if references is not None else None,
        'method': str(method) if method is not None else None,
        'method_details': str(method_details) if method_details is not None else None,
        'calculated_column': str(calculated_column) if calculated_column is not None else None,
        'material_analyzed_column': str(material_analyzed_column) if material_analyzed_column is not None else None
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:  # Successful response
        sample_data = response.json()
        # Convert to pandas DataFrame
        samples_df = pd.DataFrame(sample_data)
        return samples_df
    else:
        # Print error
        print(f"Error: {response.status_code}")
        return None

