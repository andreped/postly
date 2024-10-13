import re
from collections import Counter
from typing import List

from ..common.models import Post


class PostlyClient:
    """
    The Postly service interface.

    This allows adding and deleting users, adding, and retrieving posts
    and getting trending topics.
    """

    def __init__(self) -> None:
        self.userPosts = {}
        self.post_max_length = 140
        self.timestamp_iter = 0

    @staticmethod
    def get_topics_from_post(post: str) -> List[str]:
        """
        Get topics from post.

        Args:
            post: The post to extract topics from.
        Returns:
            A list of topics.
        """
        return re.findall(pattern=r"#(\w+)", string=post)

    def add_user(self, user_name: str) -> None:
        """
        Add new user to system.

        Args:
            user_name: The name of the user to add.
        Returns:
            None
        """
        self.userPosts[user_name] = []

    def add_post(self, user_name: str, post_text: str, timestamp: int) -> None:
        """
        Add new post to the user's post history.

        Args:
            user_name: The name of the user to add the post to.
            post_text: The text of the post.
            timestamp: The timestamp of the post.
        Returns:
            None
        """
        if user_name not in self.userPosts:
            raise KeyError(f"User {user_name} not found.")
        
        if len(post_text) > self.post_max_length:
            raise RuntimeError("Post is too long")

        if not post_text.strip():
            raise ValueError("Post cannot be empty.")
        
        if not isinstance(timestamp, int) or timestamp < 0:
            raise ValueError("Timestamp must be a non-negative integer.")

        self.timestamp_iter += 1
        curr_topics = self.get_topics_from_post(post_text)

        self.userPosts[user_name].append(Post(content=post_text, timestamp=self.timestamp_iter, topics=curr_topics))

    def delete_user(self, user_name: str) -> None:
        """
        Delete user from system.

        Args:
            user_name: The name of the user to delete.
        Returns:
            None
        """
        if user_name not in self.userPosts:
            raise KeyError(f"User '{user_name}' not found.")
        
        self.userPosts.pop(user_name, None)

    def get_posts_for_user(self, user_name: str) -> List[str]:
        """
        Get all posts for user, sorted by timestamp in descending order.

        Args:
            user_name: The name of the user to retrieve posts for.
        Returns:
            A list of posts.
        """
        if user_name not in self.userPosts:
            raise KeyError(f"User '{user_name} not found.")
        
        return [post_data.content for post_data in self.userPosts[user_name][::-1]]

    def get_posts_for_topic(self, topic: str) -> List[str]:
        """
        Get all posts for topic.

        Args:
            topic: The topic to retrieve posts for.
        Returns:
            A list of posts.
        """
        matched_posts = []
        for user in self.userPosts:
            for post_data in self.userPosts[user]:
                if topic in post_data.topics:
                    matched_posts.append(post_data.content)

        return matched_posts

    def get_trending_topics(self, from_timestamp: int, to_timestamp: int) -> List[str]:
        """
        Get all trending topics within a time interval.

        Args:
            from_timestamp: The start of the time interval.
            to_timestamp: The end of the time interval.
        Returns:
            A list of topics.
        """
        if not isinstance(from_timestamp, int) or from_timestamp < 0:
            raise ValueError("from_timestamp must be a non-negative integer.")
        
        if not isinstance(to_timestamp, int) or to_timestamp < 0:
            raise ValueError("to_timestamp must be a non-negative integer.")
        
        if from_timestamp > to_timestamp:
            raise ValueError("from_timestamp cannot be greater than to_timestamp.")
        
        # construct topic histogram
        topics_frequency = Counter()
        for user in self.userPosts:
            for post_data in self.userPosts[user]:
                if from_timestamp <= post_data.timestamp <= to_timestamp:
                    topics_frequency.update(post_data.topics)

        # retriev top topics in descending order
        return [topic for topic, _ in topics_frequency.most_common()]
