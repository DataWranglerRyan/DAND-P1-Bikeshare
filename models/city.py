import pandas as pd
from pathlib import Path


class City(object):
    def __init__(self, city):
        self.city = city
        self.csv_path = '../data/{}.csv'.format(self.city)
        self.df = None
        if self.has_data():
            self.df = self.__load_csv()
        else:
            raise ValueError('{} does not have a corresponding csv file.'.format(city))
        self.filtered_df = None

    def has_data(self):
        return Path(self.csv_path).is_file()

    def __get_required_columns(self):
        required_cols = ['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type',
                         'Gender', 'Birth Year']
        existing_cols = pd.read_csv(self.csv_path, nrows=0).columns
        return list(set(required_cols) & set(existing_cols))

    def __load_csv(self):
        df = pd.read_csv(self.csv_path, usecols=self.__get_required_columns(), parse_dates=['Start Time', 'End Time'])
        df['Start Day'] = df['Start Time'].dt.dayofweek  # weekday_name
        df['End Day'] = df['End Time'].dt.dayofweek  # weekday_name
        df['Start Hour'] = df['Start Time'].dt.hour
        df['End Hour'] = df['End Time'].dt.hour
        return df

    def __parse_filter_input(self, input_string, start_range=0, end_range=6):
        if input_string.lower() == 'all':
            return list(range(start_range, end_range))
        try:
            if all((int(x) >= start_range) and (int(x) < end_range) for x in input_string.split()):
                return [int(x) for x in input_string.split()]
            else:
                raise ValueError("{} is not in range for filter input.".format(input_string))
        except ValueError:
            print("{} is not a valid filter input.".format(input_string))
            raise

    def filter(self, month='all', day='all'):
        parsed_month = self.__parse_filter_input(month, 0, 12)
        parsed_day = self.__parse_filter_input(day, 0, 7)

        self.filtered_df = self.df[(self.df['Start Day'].isin(parsed_day)) &
                                   (self.df['Start Time'].dt.month.isin(parsed_month))]
        return self.filtered_df
