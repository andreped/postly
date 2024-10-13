import streamlit as st
from postly.clients.postly_client import PostlyClient

# Initialize the PostlyClient in Streamlit's session state
if 'client' not in st.session_state:
    st.session_state.client = PostlyClient()

client = st.session_state.client

def add_user():
    st.title("Add User")
    user_name = st.text_input("Enter user name")
    if st.button("Add User"):
        client.add_user(user_name)
        st.success(f"User '{user_name}' added successfully.")

def add_post():
    st.title("Add Post")
    users = client.get_users()
    user_name = st.selectbox("Select user name", users)
    post_text = st.text_area("Enter post text")
    if st.button("Add Post"):
        try:
            client.add_post(user_name, post_text)
            st.success("Post added successfully.")
        except Exception as e:
            st.error(f"Error: {e}")

def delete_user():
    st.title("Delete User")
    user_name = st.text_input("Enter user name")
    if st.button("Delete User"):
        try:
            client.delete_user(user_name)
            st.success(f"User '{user_name}' deleted successfully.")
        except KeyError as e:
            st.error(f"Error: {e}")

def get_posts_for_user():
    st.title("Get Posts for User")
    user_name = st.text_input("Enter user name")
    if st.button("Get Posts"):
        try:
            posts = client.get_posts_for_user(user_name)
            st.write(f"Posts for user '{user_name}':")
            for post in posts:
                st.write(post)
        except KeyError as e:
            st.error(f"Error: {e}")

def get_posts_for_topic():
    st.title("Get Posts for Topic")
    topic = st.text_input("Enter topic")
    if st.button("Get Posts"):
        posts = client.get_posts_for_topic(topic)
        st.write(f"Posts for topic '{topic}':")
        for post in posts:
            st.write(post)

def get_trending_topics():
    st.title("Get Trending Topics")
    from_timestamp = st.number_input("Enter from timestamp", min_value=0, step=1)
    to_timestamp = st.number_input("Enter to timestamp", min_value=0, step=1)
    if st.button("Get Trending Topics"):
        try:
            topics = client.get_trending_topics(int(from_timestamp), int(to_timestamp))
            st.write("Trending topics:")
            for topic in topics:
                st.write(topic)
        except ValueError as e:
            st.error(f"Error: {e}")

def get_all_posts():
    st.title("All Posts")
    posts = client.get_posts()
    all_posts = []
    for user_name, user_posts in posts.items():
        for post in user_posts:
            all_posts.append((user_name, post))
    sorted_posts = sorted(all_posts, key=lambda x: x[1].timestamp)
    for user_name, post in sorted_posts:
        st.markdown(f"**{user_name}**")
        st.markdown(f"{post.content}")
        st.markdown("---")

def main():
    st.sidebar.title("Postly\nSimple social media platform")
    page = st.sidebar.selectbox("Choose an action", ["Add User", "Add Post", "Delete User", "Get Posts for User", "Get Posts for Topic", "Get Trending Topics", "View All Posts"])

    if page == "Add User":
        add_user()
    elif page == "Add Post":
        add_post()
    elif page == "Delete User":
        delete_user()
    elif page == "Get Posts for User":
        get_posts_for_user()
    elif page == "Get Posts for Topic":
        get_posts_for_topic()
    elif page == "Get Trending Topics":
        get_trending_topics()
    elif page == "View All Posts":
        get_all_posts()

if __name__ == "__main__":
    main()
