from github import Github, Auth


def get_token(filename):
    with open(filename) as file:
        token = file.readline().strip()
    return token


def get_github_client(token_filepath):
    return Github(auth=Auth.Token(get_token(token_filepath)))


def get_lines_from_file(filename):
    with open(filename) as file:
        return (line.strip() for line in file.readlines() if line.strip())
