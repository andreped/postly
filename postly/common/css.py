def get_theme():
    return """
    <style>
    body {
        background-color: #ffffff;
        color: #1DA1F2;
    }
    .stButton>button {
        background-color: #1DA1F2;
        color: white;
    }
    .stTextInput>div>div>input {
        border: 1px solid #1DA1F2;
    }
    .stTextArea>div>div>textarea {
        border: 1px solid #1DA1F2;
    }
    .stSelectbox>div>div>div>div {
        border: 1px solid #1DA1F2;
    }
    .post-container {
        border: 1px solid #1DA1F2;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        background-color: #f5f8fa;
        min-height: 100px; /* Adjust this value as needed */
        position: relative; /* Ensure absolute positioning works within this container */
    }
    .post-header {
        font-weight: bold;
        color: #1DA1F2;
    }
    .post-content {
        color: #14171A;
    }
    .post-likes {
        color: #657786;
        font-size: 14px;
        position: absolute;
        bottom: 10px;
        right: 10px;
    }
    .like-button {
        background-color: transparent;
        border: none;
        color: #1DA1F2;
        cursor: pointer;
        font-size: 20px;
    }
    </style>
    """
