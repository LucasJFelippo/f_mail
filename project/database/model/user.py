class User:
    def __init__(self,**kwargs):
        if(kwargs.get("cod")): self._cod = kwargs["cod"]
        if(kwargs.get("name")): self._name = kwargs["name"]
        if(kwargs.get("nickname")): self._nickname = kwargs["nickname"]
        if(kwargs.get("password")): self._password = kwargs["password"]
        if(kwargs.get("mail")): self._mail = kwargs["mail"]
        if(kwargs.get("admin")): self._admin = kwargs["admin"]
        if(kwargs.get("verify")): self._verify = kwargs["verify"]
        
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,name):
        self._name = name

    @property
    def nickname(self):
        return self._nickname
    @nickname.setter
    def nickname(self,nickname):
        self._nickname = nickname

    @property
    def cod(self):
        return self._cod
    @cod.setter
    def cod(self,cod):
        self._cod = cod

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,password):
        self._password = password

    @property
    def mail(self):
        return self._mail
    @mail.setter
    def mail(self,mail):
        self._mail = mail

    @property
    def admin(self):
        return self._admin
    @admin.setter
    def admin(self,admin):
        self._admin = admin

    @property
    def verify(self):
        return self._verify
    @verify.setter
    def verify(self,verify):
        self._verify = verify

    def doverify(self):
        self.verify = True