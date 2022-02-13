APP_NAME = "mixed-language wikinews reader"
EMAIL_OR_CONTACT_PAGE = "https://api.wikimedia.org/wiki/User:Etbubs"
with open("secrets.txt", "r") as f:
    secrets = {key: val for key, val in map(lambda line: line.split("="), f.readlines())}