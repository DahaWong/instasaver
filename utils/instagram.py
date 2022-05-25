from instaloader import *
# import config

loader = Instaloader()
# loader.login(config.instagram_user, config.instagram_password)
profile = Profile.from_username(loader.context, 'dahawong')
print(profile)
