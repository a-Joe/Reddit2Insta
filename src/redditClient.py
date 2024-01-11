import praw
from post import Post
from praw.models import MoreComments

# Reddit client to access a subreddit
class RedditClient:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

    
    def access_subreddit(self, subreddit_name):
        self.subreddit = Subreddit(self.reddit, subreddit_name)
        return self.subreddit





class Subreddit:
    def __init__(self, reddit_client, subreddit_name):
        self.subreddit = reddit_client.subreddit(subreddit_name)
        self.subreddit_name = subreddit_name
        self.reddit = reddit_client

    def get_posts(self, number_of_posts, filter="top", time="month"):
        # Returns a list of post objects after gathering all post information
        posts = []
        
        if filter == "top":
            allPosts = self.subreddit.top(time_filter=time, limit=number_of_posts)
        elif filter == "hot":
            allPosts = self.subreddit.hot(time_filter=time, limit=number_of_posts)
        post_num = 0
        for current_post in allPosts:
            awards = [{'icon_url': award['icon_url'], 'count': award['count'], 'name': award['name'], 'id': award['id']} for award in current_post.all_awardings]
            if current_post.author is None:
                author_name = "[deleted]"
            else:
                author_name = current_post.author.name

            submission = self.reddit.submission(id=current_post.id)
            posts.append(Post(current_post.id, author_name, current_post.title, self.subreddit_name, current_post.ups, current_post.num_comments, awards, current_post.created_utc, submission))
            post_num += 1
            

        return posts
    
