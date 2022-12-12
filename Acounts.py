import socket



class Account:
    def __init__(self) -> None:
        self.nickname = ""
        self.pwd = ""
        self.high_score = ""
        self.userquery = []

    def create_user(self, nickname, pwd, highscore) -> str:
        import socket   
        hostname=socket.gethostname()   
        IPAddr=socket.gethostbyname(hostname) 
        print(hostname + " " + IPAddr)
        print(nickname + " " + pwd + " " + str(highscore))
        with open('player.txt', 'w') as f:
            f.write(hostname + "\n" + IPAddr + "\n"+ nickname +"\n" + pwd +"\n" + str(highscore) )


    def exists_user(self, nickname, pwd, highscore)-> bool:
        with open('player.txt') as f:
            [self.userquery.append(line.strip()) for line in f.readlines()] 
        print(self.userquery)
        if nickname in self.userquery and pwd in self.userquery:
            return True
        return False

    def set_highscore(self):
        pass

        

if __name__=="__main__":
    acc = Account()