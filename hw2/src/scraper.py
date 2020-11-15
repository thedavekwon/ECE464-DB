import argparse
import configparser
import logging
import requests

import praw
import numpy as np

from multiprocessing import Process
from typing import Dict

from praw.models import Redditor, Submission, Comment
from pymongo import MongoClient
from bs4 import BeautifulSoup


url = "http://redditlist.com/sfw?page="


def generate_subreddit_list(subreddit_list_path: str):
    subreddit_list = []
    for i in range(1, 9):
        page = requests.get(url + str(i))
        soup = BeautifulSoup(page.content, "html.parser")
        # Top 1000 by Subscriber
        sort_by_subscriber = soup.find_all("div", class_="span4 listing")[1]
        subreddits = sort_by_subscriber.find_all(
            "div", attrs={"data-target-filter": "sfw"}, class_="listing-item"
        )
        subreddits = list(map(lambda x: x["data-target-subreddit"], subreddits))
        subreddit_list += subreddits
    assert len(set(subreddit_list)) == 1000

    with open(subreddit_list_path, "w") as f:
        f.write(",".join(subreddit_list))


def parse_redditor(redditor: Redditor) -> Dict[str, any]:
    if not redditor or not hasattr(redditor, "id") or not redditor.id:
        raise Exception("Reddit account deleted")
    return {
        "_id": redditor.id,
        "name": redditor.name,
    }


def parse_comment(comment: Comment) -> Dict[str, any]:
    if not comment or not hasattr(comment, "id") or not comment.id:
        raise Exception("Reddit comment deleted")
    return {
        "_id": comment.id,
        "body": comment.body,
        "created_utc": comment.created_utc,
        "author": parse_redditor(comment.author),
        "score": comment.score,
    }


class RedditSubmission:
    def __init__(self, submission: Submission):
        self.submission = submission

        # Get submission author
        self.author = submission.author

        # Get submission subreddit
        self.subreddit = submission.subreddit

        # Get submission comments
        self.comments = submission.comments

        # Flatten comments
        self.comments.replace_more(limit=None)
        self.comments_list = []
        for comment in self.comments:
            try:
                self.comments_list.append(parse_comment(comment))
            except Exception as e:
                logging.warning(f"Failed to parse comment: {e}")


class RedditScraper:
    def __init__(self, subreddit_list, config):
        self.reddit: praw.Reddit = praw.Reddit(
            client_id=config["REDDIT"].get("client_id"),
            client_secret=config["REDDIT"].get("client_secret"),
            user_agent=config["REDDIT"].get("user_agent"),
        )
        self.subreddit_list = subreddit_list
        self.client: MongoClient = MongoClient(
            config["MONGO"].get("host"), int(config["MONGO"].get("port"))
        )
        self.db = self.client.reddit

        self.submission: RedditSubmission = None

    def get_random_submission(self):
        self.submission = RedditSubmission(
            self.reddit.subreddit("+".join(self.subreddit_list)).random()
        )

    def upload_submission(self):
        s = self.submission
        self.db.submission.update_one(
            filter={"_id": s.submission.id},
            update={
                "$set": {
                    "_id": s.submission.id,
                    "name": s.submission.name,
                    "url": s.submission.url,
                    "subreddit": {
                        "_id": s.subreddit.id,
                        "display_name": s.subreddit.display_name,
                    },
                    "author": parse_redditor(s.author),
                    "title": s.submission.title,
                    "created_utc": s.submission.created_utc,
                    "score": s.submission.score,
                    "upvote_ratio": s.submission.upvote_ratio,
                    "selftext": s.submission.selftext,
                    "comments": s.comments_list,
                }
            },
            upsert=True,
        )


def scrape(subreddit_list, config):
    rs = RedditScraper(subreddit_list, config)
    while True:
        try:
            rs.get_random_submission()
            rs.upload_submission()
        except Exception as e:
            logging.error(f"Failed to upload random submission: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reddit Scrapper")
    parser.add_argument(
        "-c",
        type=str,
        help="Config file path",
        required=True,
    )
    parser.add_argument("--gen", help="Generate subreddit list", action="store_true")

    args = parser.parse_args()

    if args.c:
        config = configparser.ConfigParser()
        config.read(args.c)
        subreddit_list_path = config["REDDIT"].get("subreddit_list_path")
        if args.gen:
            if not subreddit_list_path:
                raise Exception("Need to provide path to generate subreddit list.")
            generate_subreddit_list(subreddit_list_path)
        else:
            num_processes = int(config["REDDIT"].get("num_process"))
            with open(subreddit_list_path) as f:
                subreddit_list = f.readline().split(",")

            if not subreddit_list:
                raise Exception("Empty subreddit list")

            rs = RedditScraper(["Python"], config)
            subreddit_lists = np.array_split(subreddit_list, num_processes)
            for i in range(num_processes):
                Process(target=scrape, args=(subreddit_lists[i], config)).start()
