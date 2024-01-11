import requests
import datetime

class Comment:
    def __init__(self, id, redditor, text, upvotes, time):
        self.id = id
        self.redditor = redditor # object to hold all info related to author aka redditor
        self.text = text
        self.upvotes = upvotes
        #self.awards = awards
        self.time_created = time
        self.display_time = self.calculate_time()

        self.replies = []

    def add_reply(self, reply):
        #reply == Comment()
        self.replies.append(reply)

    def remove_reply(self, reply):
        self.replies.remove(reply)

    def download_user_avatar(self):
        has_avatar = False 
        try:
            user_avatar_url = self.redditor.snoovatar_img
            if user_avatar_url != '' and user_avatar_url != None:
                has_avatar = True
                print("PRINTING" , user_avatar_url)
                user_avatar_img = requests.get(user_avatar_url).content
                with open(f'avatars/avatar_{self.redditor}.png', 'wb') as handler:
                    handler.write(user_avatar_img)
        except AttributeError:
            print("No Avatar for user, likely a [deleted] user")

        return has_avatar
    
    def calculate_upvotes_value(self):
        self.upvotes = int(self.upvotes)  # Convert string to integer.
        if (self.upvotes >= 1000):
            upvotes_k = self.upvotes / 1000
            if upvotes_k.is_integer():
                upvotes_str = "{}k".format(int(upvotes_k))
            else:
                upvotes_str = "{:.1f}k".format(upvotes_k)
        else:
            upvotes_str = str(self.upvotes)

        return upvotes_str
    
    def get_reply(self, num):
        if (len(self.replies) > num):
            return self.replies[num]
        else: 
            return None

    def calculate_time(self):
        # Get the post's creation time (in Unix timestamp format)
        creation_time = datetime.datetime.fromtimestamp(self.time_created)

        # Get the current time
        current_time = datetime.datetime.now()

        # Calculate the time difference
        time_diff = current_time - creation_time
        
        # Display the time difference in a human-friendly format
        if time_diff.days > 365:
            years = time_diff.days // 365
            time = f'{years} year ago' if years == 1 else f'{years} years ago'
        elif time_diff.days > 30:
            months = time_diff.days // 30
            time = f'{months} month ago' if months == 1 else f'{months} months ago'
        elif time_diff.days > 0:
            days = time_diff.days
            time = f'{days} day ago' if days == 1 else f'{days} days ago'
        elif time_diff.seconds > 3600:
            hours = time_diff.seconds // 3600
            time = f'{hours} hour ago' if hours == 1 else f'{hours} hours ago'
        elif time_diff.seconds > 60:
            minutes = time_diff.seconds // 60
            time = f'{minutes} minute ago' if minutes == 1 else f'{minutes} minutes ago'
        else:
            time = 'Just now'

        return time