import os
import requests
from datetime import datetime

repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]

headers = {
    "Authorization": f"token {token}"
}

issues = requests.get(
    f"https://api.github.com/repos/{repo}/issues?labels=guestbook&state=all",
    headers=headers
).json()

entries = []

for issue in issues[:10]:

    user = issue["user"]["login"]

    avatar = issue["user"]["avatar_url"]

    date = datetime.strptime(
        issue["created_at"],
        "%Y-%m-%dT%H:%M:%SZ"
    ).strftime("%d %B %Y")

    message = issue["body"].split("### Mission Log")[-1].strip()

    entries.append(f"""
### 🪖 [{user}](https://github.com/{user})

<img src="{avatar}" width="40">

> "{message}"

📅 {date}

──────────────────────────────
""")

guestbook = "\n".join(entries)

with open("README.md","r",encoding="utf8") as f:
    readme = f.read()

start="<!-- GUESTBOOK_START -->"
end="<!-- GUESTBOOK_END -->"

new = (
    readme.split(start)[0]
    + start
    + "\n\n## 🪖 MISSION LOG\n\n"
    + guestbook
    + "\n"
    + end
)

with open("README.md","w",encoding="utf8") as f:
    f.write(new)
