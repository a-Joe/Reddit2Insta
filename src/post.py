import datetime
from comment import Comment
class Post:
    def __init__(self, id, author: str, text: str, subreddit: str, upvotes, num_comments: int, awards, time_created, submission):
        self.id = id
        self.author = author
        self.text = text
        self.subreddit = subreddit
        self.upvotes = upvotes
        self.awards = awards
        self.time_created = time_created
        self.display_time = self.calculate_time()
        self.num_comments = num_comments
        self.submission = submission

        self.comments = []



    def add_comment(self, comment):
        self.comments.append(comment)

    def remove_comment(self, comment):
        self.comments.remove(comment)
    
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
    
    def calculate_comments_value(self):
        self.num_comments = int(self.num_comments)  # Convert string to integer.
        if (self.num_comments >= 1000):
            comments_k = self.num_comments / 1000
            if comments_k.is_integer():
                comments_str = "{}k".format(int(comments_k))
            else:
                comments_str = "{:.1f}k".format(comments_k)
        else:
            comments_str = str(self.comments)

        return comments_str


    def get_replies(self, number_of_replies):
        self.submission.comment_sort = 'top'
        # Api retrieves less than number_of_replies so call for 20 extra.
        # although loop will still end when we reach number_of_replies retrieved comments
        self.submission.comment_limit = number_of_replies + 20
        self.submission.comments.replace_more(limit=0)
        # Debugging
        # print("GETTING REPLIES FOR POST ... ")
        # print("Number of comments: ", submission.num_comments)
        # print("Limit: ", number_of_replies)
        # print("Title: " , post.text)
        count = 0
        for top_level_comment in self.submission.comments:
            if top_level_comment.body not in [None, '[removed]', '[deleted]']:
                comment = Comment(top_level_comment.id, top_level_comment.author, top_level_comment.body, top_level_comment.score, top_level_comment.created_utc)
                self.add_comment(comment) # Adds a comment to our Post class
                count+=1
                #TO-DO do this in comment class?
                for second_level_comment in top_level_comment.replies:
                    comment_reply = Comment(second_level_comment.id, second_level_comment.author, second_level_comment.body, second_level_comment.score, second_level_comment.created_utc)
                    if comment_reply.redditor and hasattr(comment_reply.redditor, 'name') and comment_reply.redditor.name is not None:
                        comment.add_reply(comment_reply)

            if count >= number_of_replies:
                break
    


    def get_comments(self):
        return self.comments
    
    def get_num_comments(self):
        return len(self.comments)