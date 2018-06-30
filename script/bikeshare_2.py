from models.city import City
print("hello world")

city = City('washington')
city.filter(month='All', day='0 6')
print(city.filtered_df)
