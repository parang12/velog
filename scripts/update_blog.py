import feedparser
import git
import os

repo = git.Repo('.')
repo.git.config('--local', 'user.name', 'parang12')
repo.git.config('--local', 'user.email', 'gitm955133@gmail.com')

rss_url = 'https://api.velog.io/rss/@parang12'

repo_path = '.'
posts_dir = os.path.join(repo_path, 'velog-posts')

if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

repo = git.Repo(repo_path)
feed = feedparser.parse(rss_url)

for entry in feed.entries:
    file_name = entry.title.replace('/', '-').replace('\\', '-').replace('?', '').replace(':', '').replace('*', '').replace('<', '').replace('>', '').replace('|', '').strip() + '.md'
    file_path = os.path.join(posts_dir, file_name)

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(entry.description)

        repo.git.add(file_path)
        repo.git.commit('-m', f'Add post: {entry.title}')

repo.git.push()
