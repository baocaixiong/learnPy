#!/usr/bin/env python
#coding: utf-8

from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore

PORT = 5005
NAME = 'TestChat'

class EndSession(Exception): pass

class CommandHandler(object):
    def unknown(self, session, cmd):
        '''
        响应未知的命令
        '''
        session.push('Unknown command: %s' % cmd)

    def handle(self, session, line):
        '''
        处理从给定会话中接收到的行
        '''
        if not line.strip():return 
        parts = line.split(' ', 1)

        cmd = parts[0] # 命令

        try:
            line = parts[1].strip()
        except IndexError:
            line = ''

        method = getattr(self, 'do_' + cmd, None)

        try:
            method(session, line)
        except TypeError:
            self.unknown(session, cmd)
            

class Room(CommandHandler):
    '''
    包括一个或多个用户的回话泛型环境，它负责基本的命令处理和广播
    '''
    def __init__(self, server):
        self.server = server
        self.sessions = []

    def add(self, session):
        self.sessions.append(session)

    def remove(self, session):
        self.sessions.remove(session)

    def broadcast(self, line):
        for session in self.sessions:
            session.push(line)

    def do_logout(self, session, line):
        raise EndSession

class LoginRoom(Room):
    '''
    为刚刚连接上的用户准备的房间
    '''
    def add(self, session):
        Room.add(self, session)
        # self.broadcast('Welcome to %\r\n' % self.server.name)

    def unknown(self, session, cmd):
        session.push('Please log in\nUse "login <nick>" \r\n')

    def do_login(self, session, line):
        name = line.strip()

        if not name:
            session.push('Please enter you name\r\n')
        elif name in self.server.users:
            session.push('The name "%s" is taken.\r\n' % name)
            session.push('Please try again.\r\n')
        else:
            session.name = name
            session.enter(self.server.main_room)

class ChatRoom(Room):
    '''
    为多用户聊天准备的房间
    '''
    def add(self, session):
        self.broadcast(session.name + 'has entered the room.\r\n')
        self.server.users[session.name] = session
        Room.add(self, session)
    def remove(self, session):
        Room.remove(self, session)

        self.broadcast(session.name + 'has left the room.\r\n')

    def do_say(self, session, line):
        self.broadcast(session.name + ': ' + line + '\r\n')

    def do_look(self, session, line):
        session.push('The following are in this room: \r\n')
        for other in self.sessions:
            session.push(other.name + '\r\n')

    def do_who(self, session, line):
        session.push('The following are logged in: \r\n')
        for name in self.server.users:
            session.push(name + '\r\n')

class LogoutRoom(Room):
    def add(self, session):
        try:
            del self.server.users[session.name]
        except KeyError:
            pass

class ChatSession(async_chat):
    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.set_terminator('\r\n')
        self.data = []
        self.name = None
        self.enter(LoginRoom(server))
        self.server = server

    def enter(self, room):
        try:
            cur = self.room
        except AttributeError:
            pass
        else: cur.remove(self)
        self.room = room
        room.add(self)

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        line = ''.join(self.data)
        self.data = []
        try:
            self.room.handle(self, line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))

class ChatServer(dispatcher):
    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.name = name
        self.users = {}
        self.main_room = ChatRoom(self)

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)

if __name__ == '__main__':
    s = ChatServer(PORT, NAME)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass