import requests


website = requests.get('https://tss.warthunder.com/index.php?action=current_tournaments')
print(website.text)