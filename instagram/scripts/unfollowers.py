import json


def main():
    # Read in json file
    with open("./instagram_data/connections.json") as f:
        data = json.load(f)

    # Get followers and following
    followers = [username for username in data["followers"].keys()]
    following = [username for username in data["following"].keys()]

    # Open/Create file to write usernames to
    output = open("./output/unfollowers.txt", "w")

    # Find usernames not following me back
    unfollowers = [username for username in following if username not in followers]
    unfollowers.sort()

    # Print list of unfollowers to file
    for username in unfollowers:
        output.write(username + "\n")

main()
