from models.city import City


class UserPrompter(object):
    def __init__(self):
        self.city = None

    def get_city(self):
        while True:
            try:
                city_response = input('Which city\'s bikeshare data would you like to explore?')
                self.city = City(city_response)
                print("{} bikeshare data has been loaded!".format(city_response.title()))
                return self.city
            except ValueError as e:
                print(e)
                continue

    def filter_month_and_day(self):
        while True:
            try:
                month_filter = input("""{}\'s bikeshare program has data for the first 6 months of 2017. Which months would you like to explore?
(enter 1-6)(for multiple months insert a space between each month)(enter 'All' for every month)""".format(self.city.name.title()))
                day_filter = input("""Which days would you like to explore?
(enter 0-6, where 0 is Sunday)(for multiple days insert a space between each day)(enter 'All' for every day)""")
                filtered = self.city.filter(month=month_filter, day=day_filter)
                return filtered
            except ValueError:
                continue


