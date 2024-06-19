# import json
# from django.contrib.auth.hashers import make_password

# # List of users with plain text passwords
# new_users = [
#     {
#             "model": "website.CustomUser",
#             "pk": 2,
#             "fields":{
#                 "avatar": "/tools/default-avatar.jpg",
#                 "username": "John",
#                 "email": "John@42.fr",
#                 "first_name": "John",
#                 "last_name":"Doe",
#                 "status": "online",
#                 "password": "etoile12"
#             }
#         },
#         {
#             "model": "website.CustomUser",
#             "pk": 3,
#             "fields":{
#                 "avatar": "/tools/default-avatar.jpg",
#                 "username": "imraoui",
#                 "email": "imraoui@42.fr",
#                 "first_name": "Imen",
#                 "last_name":"Imraoui",
#                 "status": "online",
#                 "password": "etoile12"
#             }
#         },
#         {
#             "model": "website.CustomUser",
#             "pk": 4,
#             "fields":{
#                 "avatar": "/tools/default-avatar.jpg",
#                 "username": "hferjani",
#                 "email": "hinda@42.fr",
#                 "first_name": "Hinda",
#                 "last_name":"Ferjani",
#                 "status": "online",
#                 "password": "etoile12"
#             }
#         },
#         {
#             "model": "website.CustomUser",
#             "pk": 5,
#             "fields":{
#                 "avatar": "/tools/default-avatar.jpg",
#                 "username": "mvicedo",
#                 "email": "Marine@42.fr",
#                 "first_name": "Marine",
#                 "last_name":"Vicedo",
#                 "status": "online",
#                 "password": "etoile12"
#             }
#         },
#         {
#             "model": "website.CustomUser",
#             "pk": 6,
#             "fields":{
#                 "avatar": "/tools/default-avatar.jpg",
#                 "username": "pmaimait",
#                 "email": "Parida@42.fr",
#                 "first_name": "Parida",
#                 "last_name":"Maimait",
#                 "status": "online",
#                 "password": "etoile12"
#             }
# 	},
# ]

# # Hash the passwords for new users
# for user in new_users:
#     user['fields']['password'] = make_password(user['fields']['password'])

# # Read existing data from user_data.json (handle potential FileNotFoundError)
# try:
#     with open('user_data.json', 'r') as file:
#         existing_users = json.load(file)
# except FileNotFoundError:
#     existing_users = []

# # Update existing data with new users (avoid overwriting)
# all_users = existing_users.copy()  # Create a copy to avoid modifying original
# all_users.extend(new_users)  # Add new users to the copy

# # Write the merged data back to user_data.json
# with open('user_data.json', 'w') as f:
#     json.dump(all_users, f, indent=4)