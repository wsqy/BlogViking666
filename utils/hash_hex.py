import hashlib, time, string, random

def ArticleHash():
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, 5))
    sha = str(time.time()) + rand_str
    sha1 = hashlib.sha1()
    sha1.update(sha.encode())
    return sha1.hexdigest()
