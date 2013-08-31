

from nntplib import NNTP

server = NNTP('news2.neva.ru')
print server.group('alt.sex.telephone')