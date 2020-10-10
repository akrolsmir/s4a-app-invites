import cached_github
import streamlit as st
import pandas as pd
import zipfile

"# S4A App Explorer"

# Parsing the user's input

def err(msg):
    """Print an error message to the user and stop."""
    st.warning(msg)
    st.stop()

def get_config():
    """Returns all the config information to run the app."""
    
    # Get input
    config = st.sidebar.beta_expander('Config', expanded=True)
    raw_input = config.file_uploader('User list zip file.', types='zip')
    access_token = config.text_input("Github access token", type="password")

    # Check for input
    if not raw_input:
        err('Please upload a user file. Ask TC for the file.')
    if not access_token:
        err('Please enter a github access token.')

    # Parse and return the information
    user_table = extract_csv_from_zip_file(raw_input)
    github = cached_github.from_access_token(access_token)
    return user_table, github

@st.cache
def extract_csv_from_zip_file(raw_input):
    with zipfile.ZipFile(raw_input) as zip_input:
        names = zip_input.namelist()
        assert len(names) == 1 and names[0].endswith('.csv'), \
            "Zipfile must have only one csv."
        with zip_input.open(names[0]) as csv_input:
            return pd.read_csv(csv_input)


user_table, github = get_config()
status = st.selectbox('Status', list(set(user_table['Status'])))
filtered_users = user_table[user_table['Status'] == status]
filtered_users = filtered_users.sort_values(by='Applied At', ascending=True)
filtered_users, len(filtered_users)
for s4a_user in filtered_users.itertuples():
    github_user = cached_github.get_user_from_email(github, s4a_user.Email)
    'type(github_user)', type(github_user)
    if not github_user:
        continue
    github_login = github_user.login
    f'email: `{s4a_user.Email}`'
    f'twitter_username: `{github_user.twitter_username}`'
    f'created_at: `{github_user.created_at}`'
    f'name: `{github_user.name}`'
    f'login: `{github_login}`'
    rv = cached_github.get_streamlit_repos(github, github_login)
    'rv', rv
    raise RuntimeError('Stopping here.')

