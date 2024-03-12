import random

def get_random_hashtags(file_path, min_count=10, max_count=15):
    # Reads hashtags from the specified file and returns a random selection of
    # hashtags within the specified range.


    try:
        with open(file_path, 'r') as file:
            hashtags = [line.strip() for line in file.readlines()]

        # Filter out empty strings
        hashtags = [tag for tag in hashtags if tag]

        if not hashtags:
            print("No hashtags found in the file.")
            return []

        # Randomly select hashtags within range
        hashtag_count = random.randint(min_count, max_count)
        selected_hashtags = random.sample(hashtags, hashtag_count)

        return selected_hashtags
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []


random_hashtags = get_random_hashtags('hashtags.txt')
print("\n")
for x in random_hashtags:
    print(x, end=' ')
print("\n")
