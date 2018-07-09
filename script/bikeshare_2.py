from models.user_prompter import UserPrompter

prompt = UserPrompter()
rerun = True
while rerun:
    city = prompt.get_city()
    prompt.filter_month_and_day()
    city.show_all_stats()
    rerun = prompt.rerun()

