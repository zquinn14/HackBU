import tweets

tweets.init()

statuses = tweets.get_statuses()

for s in statuses:
    print(s)