from replit import db

def watchlisted(key,username):
    text = f"<b>{username}'s Watchlist</b>\n\n"

    if key in db.keys():
        count = 0
        for product in db[key]:
            count += 1
            alert = product.get('alert', 'None')
            title = product.get('title', 'None')
            url = product.get('url', 'None')

            text += f'{count})\n<b>Name:</b> <a href="{url}">{title}</a>\n<b>Alert:</b> {alert}\n\n'
    else:
        text += '<code>Empty</code>'

    return text


def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        return False

    return True

def scraper_cc(url):
    cc_list = ['us','uk','ca','de','fr','es','br','mx','in','jp','cn','au']
    cc = url[19:].split('/')[0]
    if len(cc) == 3:
        cc = 'us'
    else:
        cc = cc[-2:]
        if cc not in cc_list:
            cc = 'us'
    return cc
