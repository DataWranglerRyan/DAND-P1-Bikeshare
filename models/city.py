import pandas as pd
import calendar
from datetime import datetime
from pathlib import Path


class City(object):
    def __init__(self, name):
        self.name = name
        self.csv_path = '../data/{}.csv'.format(self.name.replace(' ', '_'))
        self.df = None
        if self.__has_data():
            self.df = self.__load_csv()
        else:
            raise ValueError('Currently, {} doesn\'t have bikeshare data. Try another city!'.format(name))
        self.filtered_df = None

    def __has_data(self):
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
        df['Start Month'] = df['Start Time'].dt.month
        df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
        return df

    def __parse_filter_input(self, input_string, start_range=0, end_range=6):
        '''
        Converts a string of numbers separated by spaces into a list of integers. Checks that each integer is between
        the start_range and end_range.
        :param input_string: string of numbers to be parsed.
        :param start_range: lower bound that each integer must be greater than.
        :param end_range: upper bound that each integer must be less than.
        :return: list of integers.
        '''
        error_msg = "{} is not a valid filter input.".format(input_string)
        if input_string.lower() == 'all':
            return list(range(start_range, end_range))
        try:
            if all((int(x) >= start_range) and (int(x) < end_range) for x in input_string.split()):
                return [int(x) for x in input_string.split()]
            else:
                error_msg = "{} is not in between {} and {}.".format(input_string, start_range, end_range-1)
                raise ValueError
        except ValueError:
            print(error_msg)
            raise

    def filter(self, month='all', day='all'):
        parsed_month = self.__parse_filter_input(month, 1, 7)
        parsed_day = self.__parse_filter_input(day, 0, 7)

        self.filtered_df = self.df[(self.df['Start Day'].isin(parsed_day)) &
                                   (self.df['Start Time'].dt.month.isin(parsed_month))]
        return self.filtered_df

    def most_common_month(self):
        return self.filtered_df['Start Month'].value_counts().idxmax()

    def most_common_day(self):
        return self.filtered_df['Start Day'].value_counts().idxmax()

    def most_common_hour(self):
        return self.filtered_df['Start Hour'].value_counts().idxmax()

    def show_popular_travel_times(self):
        print("The most common travel month is: {}".format(calendar.month_name[self.most_common_month()]))
        print("The most common travel day is: {}".format(calendar.day_name[self.most_common_day()]))
        print("The most common travel hour is: {}".format(datetime.strptime(str(self.most_common_hour()), "%H").strftime('%I:%M %p')))

    def show_popular_stations(self):
        print("The most common start station is: {}".format(self.filtered_df['Start Station'].value_counts().idxmax()))
        print("The most common end station is: {}".format(self.filtered_df['End Station'].value_counts().idxmax()))
        print("The most common trip is: {}".format(self.filtered_df['Trip'].value_counts().idxmax()))

    def show_trip_duration_stats(self):
        print("The sum of all trip durations is: {0:0.2f} days".format(self.filtered_df['Trip Duration'].sum()/60/60/24))
        print("The average trip duration is: {0:0.2f} minutes".format(self.filtered_df['Trip Duration'].mean()/60))
