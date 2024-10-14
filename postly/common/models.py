from dataclasses import dataclass, field
from typing import List, Set

from pydantic import BaseModel


class StrictPost(BaseModel):
    content: str
    timestamp: int
    topics: List[str]
    likes: int = 0
    liked_by: Set[str] = set()


@dataclass
class Post:
    content: str
    timestamp: int
    topics: List[str]
    likes: int = 0
    liked_by: Set[str] = field(default_factory=set)


if __name__ == "__main__":
    # this should be OK, as not strictly typed
    post = Post(content="1", timestamp=1, topics=["1"])
    post.likes += 1
    post.liked_by.add("user1")
    print(post)

    # this should result in a validation error, as pydantic enforces strict typing on runtime
    try:
        strict_post = StrictPost(content=1, timestamp=1, topics=["1"])
    except Exception as e:
        print(f"Validation error: {e}")

    # this should be OK, as strictly typed
    strict_post = StrictPost(content="1", timestamp=1, topics=["1"])
    strict_post.likes += 1
    strict_post.liked_by.add("user1")
    print(strict_post)
