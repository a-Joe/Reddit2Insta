from dotenv import load_dotenv
from imageRenderer import PostImageRenderer 
from imageRenderer import CommentImageRenderer 
from redditClient import RedditClient
from hasher import hasher
import re
import os
import time

# A program to visualise AskReddit posts as images
# Designed to be used for instagram posts
# Author: Joseph Gibson

#.env file loading for reddit API 
load_dotenv()

reddit = RedditClient(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Sets up which subreddit to search within
subreddit = reddit.access_subreddit("AskReddit")

# Filters for determining which posts to fetch
posts = subreddit.get_posts(4, "top", "week")

# Sets up the post and comment renderers
post_renderer = PostImageRenderer()
comment_renderer = CommentImageRenderer()

# Hasher for storing previously rendered posts as hashes, to avoid duplicated renders
db_hasher = hasher("Database/postHashes.txt")

# Whether to create duplicates/ignore the postHashes.txt file which stores previously rendered posts.
force_render_duplicates = True

# main function for rendering posts and their comments into images
def RenderImages():
    with open("Database/postHashes.txt", 'a') as file:
        file.write("---\n")
    post_counter = 1
    for post in posts:
        sanitized_title = re.sub('[\\/*?:"<>|]', "", post.text) # remove illegal characters
        post_folder_name = sanitized_title.replace(" ", "_") # replace spaces with underscores
        post_folder_name = post_folder_name[:200] # Shortens file name length to fit windows max file name size

        # determines if post is previously rendered based on postHashes.txt
        isPostInDatabase = db_hasher.addToDatabaseIfNotExist(post.text)

        # Determines whether post should be rendered if force render OR it already exists in postHashes.txt 
        if (force_render_duplicates == True or isPostInDatabase == False):
            os.makedirs("outputs/" +post_folder_name, exist_ok=True) # Make a file for each post
            print(post_counter , ": " , "running") # Counter to track how many posts have been rendered                      

            # Render the post
            post_renderer.render_image(post)
            # Save image
            output_path = "outputs/" + post_folder_name + "/" + str(post_counter)+"img"
            post_renderer.save_image(output_path)

            # use reddit client to retrieve replies from the post
            post.get_replies(4)
            comments = post.get_comments()

            # Render comments:
            comment_num = 0
            for comment in comments:
                comment_num +=1
                if comment.redditor and hasattr(comment.redditor, 'name') and comment.redditor.name is not None:
                    if(len(comment.text) < 850):
                        comment_renderer.render_image(comment)
                        comment_renderer.save_image("outputs/" + post_folder_name + "/" + str(post_counter)+"comment"+str(comment_num))

            post_counter += 1



        

RenderImages()

print("done")






