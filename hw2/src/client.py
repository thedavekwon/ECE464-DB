import argparse
import configparser

from pymongo import MongoClient


class RedditClient:
    def __init__(self, db):
        self.db = db

    def get_subreddit_list(self):
        """
        Get a list of subreddit
        """
        return self.db.submission.distinct("subreddit.display_name")

    def get_username_list(self):
        """
        Get a list of usernames
        """
        return list(
            set().union(
                *[
                    self.db.submission.distinct("author.name"),
                    map(
                        lambda x: x["_id"],
                        self.db.submission.aggregate(
                            [
                                {"$unwind": {"path": "$comments"}},
                                {"$group": {"_id": "$comments.author.name"}},
                            ],
                            allowDiskUse=True,
                        ),
                    ),
                ]
            )
        )

    def get_user_id_list(self):
        """
        Get a list of user ids
        """
        return list(
            set().union(
                *[
                    self.db.submission.distinct("author._id"),
                    map(
                        lambda x: x["_id"],
                        self.db.submission.aggregate(
                            [
                                {"$unwind": {"path": "$comments"}},
                                {"$group": {"_id": "$comments.author._id"}},
                            ],
                            allowDiskUse=True,
                        ),
                    ),
                ]
            )
        )

    def get_sorted_subreddit_count_list(self):
        """
        Get a list of submission count per each subreddit sorted by the count
        """
        return list(
            self.db.submission.aggregate(
                pipeline=[
                    {
                        "$group": {
                            "_id": "$subreddit.display_name",
                            "count": {"$sum": 1},
                        }
                    },
                    {"$sort": {"count": -1}},
                ],
                allowDiskUse=True,
            )
        )

    def get_sorted_user_submission_count_list(self):
        """
        Get a list of submission count per each user sorted by the count
        """
        return list(
            self.db.submission.aggregate(
                pipeline=[
                    {"$group": {"_id": "$author.name", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                ],
                allowDiskUse=True,
            )
        )

    def get_sorted_user_comment_count_list(self):
        """
        Get a list of comment count per each user sorted by the count
        """
        return list(
            self.db.submission.aggregate(
                pipeline=[
                    {"$unwind": "$comments"},
                    {"$group": {"_id": "$comments.author.name", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                ],
                allowDiskUse=True,
            )
        )

    def get_submission_id_list_by_username(self, username):
        """
        Get a list of submission id given username
        """
        return list(self.db.submission.find({"author.name": username}, {"_id": 1}))

    def get_submission_id_list_by_user_id(self, id):
        """
        Get a list of submission id given user id
        """
        return list(self.db.submission.find({"author._id": id}, {"_id": 1}))

    def get_comment_id_list_by_username(self, username):
        """
        Get a list of comment id given username
        """
        return list(
            self.db.submission.aggregate(
                pipeline=[
                    {"$match": {"comments.author.name": username}},
                    {
                        "$project": {
                            "comments": {
                                "$filter": {
                                    "input": "$comments",
                                    "as": "comment",
                                    "cond": {
                                        "$eq": [
                                            "$$comment.author.name",
                                            username,
                                        ]
                                    },
                                }
                            },
                            "_id": 0,
                        }
                    },
                    {"$unwind": {"path": "$comments"}},
                    {"$replaceRoot": {"newRoot": "$comments"}},
                    {"$project": {"comments._id": 1}},
                ],
                allowDiskUse=True,
            )
        )

    def get_comment_id_list_by_user_id(self, id):
        """
        Get a list of comment id given user id
        """
        return list(
            self.db.submission.aggregate(
                pipeline=[
                    {"$match": {"comments.author._id": id}},
                    {
                        "$project": {
                            "comments": {
                                "$filter": {
                                    "input": "$comments",
                                    "as": "comment",
                                    "cond": {
                                        "$eq": [
                                            "$$comment.author._id",
                                            id,
                                        ]
                                    },
                                }
                            },
                            "_id": 0,
                        }
                    },
                    {"$unwind": {"path": "$comments"}},
                    {"$replaceRoot": {"newRoot": "$comments"}},
                    {"$project": {"comments._id": 1}},
                ],
                allowDiskUse=True,
            )
        )

    def get_user_subreddit_from_submission_list(self):
        """
        Get a list of subreddit count for each user submitted sorted by the count
        (Subreddits that a user submitted to)
        """
        return list(
            self.db.submission.aggregate(
                pipeline=[
                    {
                        "$group": {
                            "_id": "$author.name",
                            "subreddit": {"$addToSet": "$subreddit.display_name"},
                        }
                    },
                    {"$addFields": {"len": {"$size": "$subreddit"}}},
                    {"$sort": {"len": -1}},
                ],
                allowDiskUse=True,
            )
        )

    def get_user_subreddit_from_comment_list(self):
        """
        Get a list of subreddit count for each user commented sorted by the count
        (Subreddits that a user commented)
        """
        return list(
            self.db.submission.aggregate(
                pipeline=[
                    {"$unwind": "$comments"},
                    {
                        "$group": {
                            "_id": "$comments.author.name",
                            "subreddit": {"$addToSet": "$subreddit.display_name"},
                        }
                    },
                    {"$addFields": {"len": {"$size": "$subreddit"}}},
                    {"$sort": {"len": -1}},
                ],
                allowDiskUse=True,
            )
        )

    def get_user_subreddit_from_submission_list_by_username(self, username):
        """
        Get a list of subreddit submitted given username
        """
        return self.db.submission.find({"author.name": username}).distinct(
            "subreddit.display_name"
        )

    def get_user_subreddit_from_comment_list_by_username(self, username):
        """
        Get a list of subreddit commented given username
        """
        return self.db.submission.find({"comments.author.name": username}).distinct(
            "subreddit.display_name"
        )

    def get_user_subreddit_list_by_username(self, username):
        """
        Get a list of subreddit given username
        """
        return list(
            set().union(
                *[
                    self.get_user_subreddit_from_submission_list_by_username(username),
                    self.get_user_subreddit_from_comment_list_by_username(username),
                ]
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reddit Scrapper")
    parser.add_argument(
        "-c",
        type=str,
        help="Config file path",
        required=True,
    )
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.c)
    client = MongoClient(config["MONGO"].get("host"), int(config["MONGO"].get("port")))
    rc = RedditClient(client.reddit)