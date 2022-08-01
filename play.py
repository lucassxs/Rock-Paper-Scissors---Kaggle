from kaggle_environments import make

env = make("rps", configuration={"episodeSteps": 100}, debug=True)
env.run(["submission.py", lambda obs, conf: random.randint(0, 2)])
print(env.render(mode="ipython", width=600, height=600))


####
####rom kaggle_environments import make

####env = make("rps", configuration={"episodeSteps": 100}, debug=True)
####env.run(["submission.py", lambda obs, conf: random.randint(0, 2)])
####print(env.render(mode="ipython", width=600, height=600))