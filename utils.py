import os

def get_ip(req):
    x_real_ip = req.headers.get('X-Real-IP')
    return x_real_ip or req.remote_ip

def removeing(post):
    if post['filelink']:
        if os.path.isfile(post['filelink']):
            os.remove(post['filelink'])
