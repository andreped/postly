from .postly_client import PostlyClient


class SingletonPostlyClient:
    _instance = None

    @staticmethod
    def get_instance():
        if SingletonPostlyClient._instance is None:
            SingletonPostlyClient._instance = PostlyClient()
        return SingletonPostlyClient._instance
