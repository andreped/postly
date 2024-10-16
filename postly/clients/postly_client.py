import hashlib
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
        self.user_passwords = {}
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

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using SHA-256.

        Args:
            password: The password to hash.
        Returns:
            The hashed password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, user_name: str, password: str) -> None:
        """
        Add new user to system.

        Args:
            user_name: The name of the user to add.
            password: The password of the user.
        Returns:
            None
        """
        if user_name in self.userPosts:
            raise ValueError(f"User '{user_name}' already exists.")

        self.userPosts[user_name] = []
        self.user_passwords[user_name] = self.hash_password(password)

    def authenticate_user(self, user_name: str, password: str) -> bool:
        """
        Authenticate a user.

        Args:
            user_name: The name of the user.
            password: The password of the user.
        Returns:
            True if authentication is successful, False otherwise.
        """
        if user_name in self.user_passwords:
            hashed_password = self.hash_password(password)
            return self.user_passwords[user_name] == hashed_password
        return False

    def add_post(self, user_name: str, post_text: str) -> None:
        """
        Add new post to the user's post history.

        Args:
            user_name: The name of the user to add the post to.
            post_text: The text of the post.
        Returns:
            None
        """
        if user_name not in self.userPosts:
            raise KeyError(f"User {user_name} not found.")

        if len(post_text) > self.post_max_length:
            raise RuntimeError("Post is too long")

        if not post_text.strip():
            raise ValueError("Post cannot be empty.")

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
        self.user_passwords.pop(user_name, None)

    def get_users(self):
        """
        Get all users.

        Returns:
            A list of users.
        """
        return list(self.userPosts.keys())

    def get_posts(self):
        """
        Get all posts for all users.

        Returns:
            A dictionary of posts.
        """
        return self.userPosts

    def get_topics(self) -> List[str]:
        """
        Get all topics.

        Returns:
            A list of topics.
        """
        topics = set()
        for user in self.userPosts:
            for post_data in self.userPosts[user]:
                topics.update(post_data.topics)

        return list(topics)

    def get_current_timestamp(self) -> int:
        """
        Get the current timestamp.

        Returns:
            The current timestamp.
        """
        return self.timestamp_iter

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

        # retrieve top topics in descending order
        return [topic for topic, _ in topics_frequency.most_common()]

    def like_post(self, user_name: str, post_id: int) -> None:
        """
        Like or unlike a post.

        Args:
            user_name: The name of the user liking the post.
            post_id: The ID of the post to like or unlike.
        Returns:
            None
        """
        post = self.get_post_by_id(post_id)
        if user_name in post.liked_by:
            post.liked_by.remove(user_name)
            post.likes -= 1
        else:
            post.liked_by.add(user_name)
            post.likes += 1

    def get_post_by_id(self, post_id: int) -> Post:
        """
        Get a post by its ID.

        Args:
            post_id: The ID of the post to retrieve.
        Returns:
            The post with the given ID.
        """
        for user_posts in self.userPosts.values():
            for post in user_posts:
                if post.timestamp == post_id:
                    return post
        raise KeyError("Post not found")
