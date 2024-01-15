import configparser
import csv
import os
import urllib.error
import urllib.request

from googleapiclient.discovery import build

from const import channels, genre, names, threshold, DATA_DIR

config = configparser.ConfigParser()
api_key = config["api_key"]


def video_comments(channel: str, channel_id: str, genre: str):
    counter = 0
    file_path = os.path.join(DATA_DIR, f"{channel}.csv")
    with open(file_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(
            [
                "comment_id",
                "author",
                "date",
                "comment",
                "video_id",
                "is_reply",
                "parent_id",
                "channel",
                "genre",
            ]
        )

        # creating youtube resource object
        youtube = build("youtube", "v3", developerKey=api_key)
        try:
            # retrieve youtube video results
            video_response = (
                youtube.commentThreads()
                .list(
                    part="snippet,replies",
                    allThreadsRelatedToChannelId=channel_id,
                    maxResults=10000,
                )
                .execute()
            )

            # iterate video response
            while video_response:
                # extracting required info
                # from each result object
                for item in video_response["items"]:
                    # Extracting comments

                    comment = item["snippet"]["topLevelComment"]["snippet"][
                        "textDisplay"
                    ]
                    comment_id = item["id"]
                    author = item["snippet"]["topLevelComment"]["snippet"][
                        "authorDisplayName"
                    ]
                    date = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                    video_id = item["snippet"]["topLevelComment"]["snippet"]["videoId"]
                    writer.writerow(
                        [
                            comment_id,
                            author,
                            date,
                            comment,
                            video_id,
                            "False",
                            "",
                            channel,
                            genre,
                        ]
                    )
                    # counting number of reply of comment
                    counter += 1
                    replycount = item["snippet"]["totalReplyCount"]

                    # if reply is there
                    if replycount > 0:
                        # iterate through all reply
                        try:
                            for reply in item["replies"]["comments"]:
                                date_2 = reply["snippet"]["publishedAt"]
                                print("=========")
                                id = reply["id"]
                                author = reply["snippet"]["authorDisplayName"]

                                parent_id = reply["snippet"]["parentId"]
                                video_id = reply["snippet"]["videoId"]
                                reply = reply["snippet"]["textDisplay"]
                                writer.writerow(
                                    [
                                        id,
                                        author,
                                        date_2,
                                        comment,
                                        video_id,
                                        "True",
                                        parent_id,
                                        channel,
                                        genre,
                                    ]
                                )
                                counter += 1
                        except KeyError as key_error:
                            print(key_error)
                            pass

                # Again repeat
                if counter > threshold:
                    print("Done")
                    break

                if "nextPageToken" in video_response:
                    video_response = (
                        youtube.commentThreads()
                        .list(
                            part="snippet,replies",
                            allThreadsRelatedToChannelId=channel_id,
                            maxResults=10000,
                            pageToken=video_response["nextPageToken"],
                        )
                        .execute()
                    )
                else:
                    break
        except urllib.error.HTTPError as e:
            print(e)
            pass


for name, channel in zip(names, channels):
    video_comments(name, channel, genre)
