import streamlit as st

from postly.clients.singleton_client import SingletonPostlyClient
from postly.common.css import get_theme

# Initialize the PostlyClient singleton
client = SingletonPostlyClient.get_instance()

# Custom CSS for Twitter-like feel
st.markdown(
    get_theme(),
    unsafe_allow_html=True,
)

# Initialize user session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None


def register():
    st.title("Register")
    user_name = st.text_input("Enter user name", placeholder="Username")
    password = st.text_input("Enter password", type="password", placeholder="Password")
    if st.button("Register"):
        if user_name and password:
            try:
                client.add_user(user_name, password)
                st.session_state.logged_in = True
                st.session_state.current_user = user_name
                st.success(f"User '{user_name}' registered and logged in successfully.")
                st.rerun()
            except ValueError as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please enter both user name and password.")


def login():
    st.title("Login")
    user_name = st.text_input("Enter user name", placeholder="Username")
    password = st.text_input("Enter password", type="password", placeholder="Password")
    if st.button("Login"):
        if client.authenticate_user(user_name, password):
            st.session_state.logged_in = True
            st.session_state.current_user = user_name
            st.success(f"User '{user_name}' logged in successfully.")
            st.rerun()
        else:
            st.error("Invalid user name or password.")


def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("Logged out successfully.")
    st.rerun()


def delete_own_user():
    st.title("Delete Account ❌")
    if st.button("Delete Account"):
        try:
            client.delete_user(st.session_state.current_user)
            st.success(f"User '{st.session_state.current_user}' deleted successfully.")
            logout()
        except KeyError as e:
            st.error(f"Error: {e}")


def get_posts_for_user():
    st.title("Get Posts for User 🔎")
    users = client.get_users()
    user_name = st.selectbox("Select user name", users)
    if st.button("Get Posts"):
        try:
            posts = client.get_posts_for_user(user_name)
            st.write(f"Posts for user '{user_name}':")
            for post in posts:
                st.markdown(post)
        except KeyError as e:
            st.error(f"Error: {e}")


def get_posts_for_topic():
    st.title("Get Posts for Topic 🔎")
    topics = client.get_topics()
    topic = st.selectbox("Enter topic", topics)
    if st.button("Get Posts"):
        posts = client.get_posts_for_topic(topic)
        st.write(f"Posts for topic '{topic}':")
        for post in posts:
            st.markdown(post)


def get_trending_topics():
    st.title("Get Trending Topics 📊")
    current_timestamp = client.get_current_timestamp()
    from_timestamp = st.number_input("Enter from timestamp", min_value=0, step=1)
    to_timestamp = st.number_input(
        "Enter to timestamp", min_value=0, max_value=current_timestamp, step=1, value=current_timestamp
    )
    if st.button("Get Trending Topics"):
        try:
            topics = client.get_trending_topics(int(from_timestamp), int(to_timestamp))
            st.write("Trending topics:")
            for topic in topics:
                st.write(topic)
        except ValueError as e:
            st.error(f"Error: {e}")


def get_all_posts():
    st.title("Feed")

    # Add post section at the top
    post_text = st.text_area("What's happening? 💬", key="new_post_text")
    if st.button("Add Post 🖊️"):
        try:
            client.add_post(st.session_state.current_user, post_text)
            st.success("Post added successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

    # Display all posts
    posts = client.get_posts()
    all_posts = []
    for user_name, user_posts in posts.items():
        for post in user_posts:
            all_posts.append((user_name, post))
    sorted_posts = sorted(all_posts, key=lambda x: x[1].timestamp)[::-1]
    for user_name, post in sorted_posts:
        liked = st.session_state.current_user in post.liked_by
        like_button_label = "👍" if not liked else "👎"

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(
                f"""
                <div class="post-container">
                    <div class="post-header">{user_name}</div>
                    <div class="post-content">{post.content}</div>
                    <div class="post-timestamp">{post.timestamp}</div>
                    <div class="post-likes">Likes: {post.likes}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            if st.button(like_button_label, key=f"like_{post.timestamp}"):
                client.like_post(st.session_state.current_user, post.timestamp)
                st.rerun()


def main():
    st.sidebar.title("Postly 📝\nSimple social media platform")

    if st.session_state.logged_in:
        st.sidebar.write(f"Logged in as: {st.session_state.current_user}")
        if st.sidebar.button("Logout"):
            logout()
        page = st.sidebar.selectbox(
            "Choose an action",
            [
                "View All Posts",
                "Delete Account",
                "Get Posts for User",
                "Get Posts for Topic",
                "Get Trending Topics",
            ],
            index=0,
        )

        if page == "View All Posts":
            get_all_posts()
        elif page == "Delete Account":
            delete_own_user()
        elif page == "Get Posts for User":
            get_posts_for_user()
        elif page == "Get Posts for Topic":
            get_posts_for_topic()
        elif page == "Get Trending Topics":
            get_trending_topics()
    else:
        page = st.sidebar.selectbox("Choose an action", ["Register", "Login"], index=0)
        if page == "Register":
            register()
        elif page == "Login":
            login()

    st.sidebar.markdown(
        """
        **About Postly**

        Welcome to Postly, a simple social media platform created for fun.
        This app allows different users to share posts and like each other's posts.

        **Important Information**

        - The entire app is kept in global memory for all users accessing the app on the same instance.
        - Do not use a username and password actually used with any other apps.
        - We hash the password, but no real attempt to make a bulletproof solution was made.
        """
    )


if __name__ == "__main__":
    main()
