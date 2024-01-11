import textwrap
import PIL
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from post import Post
from comment import Comment
import os 
from position import Position

# TODO !
# Refactor position code (self.positon.x , self.position.y) - for better encapsulation

class ImageRenderer:
    
    MAIN_FONT = ImageFont.truetype('resources/fonts/Roboto-Bold.ttf', 50)
    SECONDARY_FONT = ImageFont.truetype('resources/fonts/Roboto-Bold.ttf', 32)
    COMMENT_FONT = ImageFont.truetype('resources/fonts/Roboto-medium.ttf', 40)

    def __init__(self):
        self.image = Image.new('RGB', (1080, 1080), color=(0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)


    def save_image(self, output_path: str):
        self.image.save(output_path + ".png")
        self.image = Image.new('RGB', (1080, 1080), color=(0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
        self.position = Position(10,400)

    def initialise_icons(self):
        self.downvote_icon = Image.open('resources/img/down_arrow2.png')
        self.upvote_icon = Image.open('resources/img/upvote_arrow.png')
        self.comment_icon = Image.open('resources/img/comment.png')
        self.share_icon = Image.open('resources/img/share.png')




class PostImageRenderer(ImageRenderer):
    def __init__(self):
        super().__init__()
        self.position = Position(10,400)



    def initialise_icons(self):
        super().initialise_icons()
        #TODO Allow to be any Subreddit Icon
        self.profile_icon = Image.open('resources/img/AskReddit_Icon.png')
        
        self.profile_icon = self.profile_icon.resize((100,100))
        self.upvote_icon = self.upvote_icon.resize((50,50))
        self.comment_icon = self.comment_icon.resize((48,48))

    def render_image(self, post: Post):
        self.initialise_icons()
        self.draw_header_icons(post)
        self.draw_awards(post.awards)
        self.draw_main_text(post.text)
        self.draw_footer_icons(post)


    # No longer viable/used due to reddit removing awards
    def draw_awards(self, awards):
        max_awards = 10
        # Sorts awards by most common to be displayed first
        awards = sorted(awards, key=lambda a: a['count'], reverse=True)
        position = (self.position.x+15,self.position.y+35)
        for award in awards:
            if max_awards <= 0:
                break
            try:
                award_icon = Image.open("resources/awards_icons/award_"+award['id']+'.png').resize((40, 40))
                self.image.paste(award_icon, (position[0] + self.position.x, position[1]))

                self.draw.text((position[0] + 45 + self.position.x, position[1] + 8), f"{award['count']}", font=ImageFont.truetype('fonts/Roboto-medium.ttf', 22), fill=(255, 215, 0))
                self.position.x+= 87
                max_awards -= 1
            except FileNotFoundError:
                print(f"File awards_icons/award_{award['id']}.png not found, skipping this award.")
                continue
        self.position.x = 10

    def draw_footer_icons(self, post: Post):
        self.image.paste(self.downvote_icon, (200, self.position.y+140))
        self.image.paste(self.upvote_icon, (40, self.position.y+140))
        self.image.paste(self.comment_icon, (315, self.position.y+142))
        self.draw.text((510, self.position.y+140), "•••", font=ImageFont.truetype('resources/fonts/Roboto-medium.ttf', 40), fill=(119, 121, 122))


        upvotes_value = post.calculate_upvotes_value()
        self.draw.text((100,self.position.y+150), upvotes_value, font=ImageFont.truetype('resources/fonts/Roboto-medium.ttf', 32), fill=(255, 69, 0))
        
        comments_value = post.calculate_comments_value()
        self.draw.text((380, self.position.y+150), comments_value, font=self.SECONDARY_FONT, fill=(119, 121, 122))
    
    def draw_main_text(self, text):
        line_width = 42
        lines = textwrap.wrap(text, width=line_width)
        for line in lines:
            self.draw.text((self.position.x+25, self.position.y+65), line, font=self.MAIN_FONT, fill=(255, 255, 255))
            self.position.y += 50  #Move down the line height for the next line
    
    def draw_header_icons(self, post: Post):
        self.image.paste(self.profile_icon, (self.position.x+15, self.position.y-95))   
        self.draw.text((self.position.x+135,self.position.y-90), post.subreddit, font=self.MAIN_FONT, fill=(200, 60, 80))
        
        #Calculate text width and add it to time ago text's x-coordinate
        username_width = self.draw.textlength(text=post.author, font=self.SECONDARY_FONT)
        self.draw.text((self.position.x+135,self.position.y-35), post.author, font=self.SECONDARY_FONT, fill=(40, 130, 200))
        self.draw.text((self.position.x+135+username_width+10, self.position.y-35), "• " + post.display_time, font=self.SECONDARY_FONT, fill=(200, 200, 200))

class CommentImageRenderer(ImageRenderer):
    def __init__(self):
        super().__init__()
        self.line_height = 50
        self.line_width = 53
        self.divided_chars = 0
        self.use_top_reply = False

        self.position = Position(10,500)



    def save_image(self, output_path: str):
        super().save_image(output_path)
        self.position.y = 500
    
    def download_user_avatar(self, redditor):
        has_avatar = False
        
        try:
            user_avatar_url = redditor.snoovatar_img
            if user_avatar_url != '' and user_avatar_url != None:
                has_avatar = True
                user_avatar_img = requests.get(user_avatar_url).content
                with open(f'resources/avatars/avatar_{redditor}.png', 'wb') as handler:
                    handler.write(user_avatar_img)
        except AttributeError:
            print("No Avatar for user, likely a [deleted] user")

        return has_avatar
    #TODO 
    # change avatar
    def initialise_icons(self):
        super().initialise_icons()
        self.profile_icon = Image.open("resources/avatars/avatar_default.png")    
        self.profile_icon = self.profile_icon.resize((90,110))
        self.upvote_icon = self.downvote_icon.resize((45,45)).rotate(180)
        self.downvote_icon = self.downvote_icon.resize((45,45))
        self.comment_icon = self.comment_icon.resize((38,38))
        self.share_icon = self.share_icon.resize((40,40))

    # Determines if reply (to the original comment) should be used
    def determine_use_top_reply(self, comment):
        comment_reply = comment.get_reply(0)
        draw_top_reply = False 
        
        if (comment_reply is not None):
            if (len(comment.text) + len(comment_reply.text)) < 750:
                if (comment_reply.upvotes / comment.upvotes > 0.45):
                    draw_top_reply = True

        return draw_top_reply
    
    def render_image(self, comment: Comment):
        # Get comment chars (len) to and determine amount to adjust y by to aprox centre text
        comment_chars = len(comment.text)
        divided_chars = comment_chars / self.line_width
        added_y = round(divided_chars) * round(self.line_height/1.65)
        self.position.y-=added_y
        
        self.use_top_reply = self.determine_use_top_reply(comment)
        # if using top reply 
        # determine how far to additionally move text "up"
        if (self.use_top_reply == True):
            comment_reply = comment.get_reply(0)
            if (comment_reply is not None):
                reply_chars = len(comment_reply.text)
                divided_chars_reply = reply_chars / self.line_width
                self.position.y-= round(divided_chars_reply) * round(self.line_height/1.7)
        self.initialise_icons()
        self.draw_header_icons(comment)
        self.draw_main_text(comment)



    def draw_footer_icons(self, comment):
        self.image.paste(self.downvote_icon, (200, self.position.y+100))
        self.image.paste(self.upvote_icon, (40, self.position.y+100))
        self.image.paste(self.comment_icon, (315, self.position.y+102))
        self.draw.text((410, self.position.y+100), "•••", font=ImageFont.truetype('resources/fonts/Roboto-medium.ttf', 40), fill=(119, 121, 122))
        upvotes_value = comment.calculate_upvotes_value()
        self.draw.text((100,self.position.y+110), upvotes_value, font=ImageFont.truetype('resources/fonts/Roboto-medium.ttf', 32), fill=(119, 121, 122))
        

    def draw_footer_icons_reply(self, comment):
        self.draw.text((720, self.position.y+70), "•••", font=ImageFont.truetype('resources/fonts/Roboto-medium.ttf', 40), fill=(119, 121, 122))
        self.image.paste(self.share_icon, (950, self.position.y+70))
        self.image.paste(self.upvote_icon, (790, self.position.y+70))
        upvotes_value = comment.calculate_upvotes_value()
        self.draw.text((850,self.position.y+75), upvotes_value, font=ImageFont.truetype('resources/fonts/Roboto-medium.ttf', 32), fill=(119, 121, 122))

    
    def draw_header_icons(self, comment):
        has_avatar = self.download_user_avatar(comment.redditor) # Download users avatar returns false if cannot download
        if (has_avatar):
            try:
                user_avatar_icon = Image.open('resources/avatars/avatar_' + comment.redditor.name + '.png')
            except PIL.UnidentifiedImageError:
                user_avatar_icon = Image.open('resources/avatars/avatar_default.png')
        else:
            user_avatar_icon = Image.open('resources/avatars/avatar_default.png')
                
        user_avatar_icon = user_avatar_icon.resize((90,110))
        self.image.paste(user_avatar_icon, (self.position.x+15, self.position.y-85))
        username_width = self.draw.textlength(text=comment.redditor.name, font=self.SECONDARY_FONT)
        self.draw.text((self.position.x+115,self.position.y-45), comment.redditor.name, font=self.SECONDARY_FONT, fill=(40, 130, 200))
        self.draw.text((self.position.x+115+username_width+10, self.position.y-45), "• " + comment.display_time, font=self.SECONDARY_FONT, fill=(200, 200, 200))
        
    def draw_header_icons_reply(self, comment):
        has_avatar = self.download_user_avatar(comment.redditor) # Download users avatar returns false if cannot download
        if (has_avatar):
            try:
                user_avatar_icon = Image.open('resources/avatars/avatar_' + comment.redditor.name + '.png')
            except PIL.UnidentifiedImageError:
                user_avatar_icon = Image.open('resources/avatars/avatar_default.png')
        else:
            user_avatar_icon = Image.open('resources/avatars/avatar_default.png')
                
        user_avatar_icon = user_avatar_icon.resize((70,90))
        self.image.paste(user_avatar_icon, (self.position.x+105, self.position.y+95))
        username_width = self.draw.textlength(text=comment.redditor.name, font=self.SECONDARY_FONT)
        self.draw.text((self.position.x+205,self.position.y+130), comment.redditor.name, font=self.SECONDARY_FONT, fill=(40, 130, 200))
        self.draw.text((self.position.x+205+username_width+10, self.position.y+130), "• " + comment.display_time, font=self.SECONDARY_FONT, fill=(200, 200, 200))

    def draw_main_text(self, comment):

        lines = textwrap.wrap(comment.text, width=self.line_width)
        for line in lines:
            self.draw.text((self.position.x+25, self.position.y+45), line, font=self.COMMENT_FONT, fill=(255, 255, 255))
            self.position.y += self.line_height  # Move down the line height for the next line

        # Finish main comment with its footer icons 
        if self.use_top_reply == False:
            self.draw_footer_icons(comment)
        else: 
            self.draw_footer_icons_reply(comment)

        # draws everything for comments reply if determined to be used.
        if self.use_top_reply:
            # draw footer icons of first comment then proceede with secondary comment
            comment_reply = comment.get_reply(0)
            if (comment_reply is not None):
                self.draw_header_icons_reply(comment_reply)
                lines_reply = textwrap.wrap(comment_reply.text, width=50)
                for line in lines_reply:
                    self.draw.text((self.position.x+105, self.position.y+200), line, font=self.COMMENT_FONT, fill=(255, 255, 255))
                    self.position.y += 42
            self.position.y +=160
            self.draw_footer_icons_reply(comment_reply)

        
