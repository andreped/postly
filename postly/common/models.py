from dataclasses import dataclass
from pydantic import BaseModel
from typing import List


class StrictPost(BaseModel):
    content: str
    timestamp: int
    topics: List[str]


@dataclass
class Post:
    content: str
    timestamp: int
    topics: List[str]


if __name__ == "__main__":
    # this should be OK, as not strictly typed
    Post(content=1, timestamp=1, topics=["1"])

    # this should result in a validation error, as pydantic enforces strict typing on runtime
    StrictPost(content=1, timestamp=1, topics=["1"])
