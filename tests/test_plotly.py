from postly.clients.postly_client import PostlyClient


class TestPlotlyClient:
    def setup_method(self):
        self.postly_instance = PostlyClient()

        # define reference data for testing
        self.gt_posts = [
            "just #chilling today",
            "eating #steak for dinner",
            "ugh! this #steak tasted like dog food"
        ]
        self.gt_topics = [["chilling"], ["steak"], ["steak"]]

        # add toy data for testing
        self.postly_instance.add_user("john")
        for post in self.gt_posts:
            self.postly_instance.add_post("john", post)
    
    def test_add_user(self):
        assert "john" in self.postly_instance.userPosts
    
    def test_add_post(self):
        assert len(self.postly_instance.userPosts["john"]) == 3

    def test_get_posts_for_user(self):
        retrieved_posts = self.postly_instance.get_posts_for_user("john")

        assert len(retrieved_posts) == 3
        for post, gt_post in zip(retrieved_posts, self.gt_posts[::-1]):
            assert post == gt_post

    def test_get_posts_for_topic(self):
        retrieved_posts = self.postly_instance.get_posts_for_topic("steak")

        assert len(retrieved_posts) == 2
        for post in retrieved_posts:
            assert "#steak" in post
    
    def test_get_trending_topics(self):
        trending_topics = self.postly_instance.get_trending_topics(1, 3)
        
        assert len(trending_topics) == 2
        assert trending_topics == ["steak", "chilling"]

        trending_topics = self.postly_instance.get_trending_topics(2, 3)

        assert len(trending_topics) == 1
        assert trending_topics == ["steak"]

    def test_delete_user(self):
        temporary_postly_instance = PostlyClient()
        temporary_postly_instance.add_user("simon")
        temporary_postly_instance.add_post("simon", "just #coding today")

        assert "simon" in temporary_postly_instance.userPosts
        
        temporary_postly_instance.delete_user("simon")

        assert "simon" not in temporary_postly_instance.userPosts
