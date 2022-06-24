indeed_configs = {'indeed':{'name':'indeed.com'}}

# get name key from indeed_configs

for key,value in indeed_configs.items():
    # get all the keys inside the key
    for key_inside,value_inside in value.items():
        print(key_inside)