import json

class Cliente:
    def __init__(self, id, nome, email, fone, senha):
        self.id = id
        self.set_nome(nome)
        self.set_email(email)
        self.set_fone(fone)
        self.set_senha(senha)

    def __str__(self):
        return f"{self.get_nome()} - {self.get_email()} - {self.get_fone()}"

    def to_json(self):
        dic = {}
        dic["id"] = self.get_id()
        dic["nome"] = self.get_nome()
        dic["email"] = self.get_email()
        dic["fone"] = self.get_fone()
        dic["senha"] = self.get_senha()
        return dic

    def get_id(self):
        return self.id

    def get_nome(self):
        return self._nome

    def get_email(self):
        return self._email

    def get_fone(self):
        return self._fone

    def get_senha(self):
        return self._senha

    def set_id(self, id):
        if not isinstance(id, int):
            raise ValueError("ID deve ser um inteiro.")
        self.id = id
        
    def set_nome(self, nome):
        if not isinstance(nome, str):
            raise ValueError("Nome deve ser uma string.")
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        self._nome = nome

    def set_email(self, email):
        if not isinstance(email, str):
            raise ValueError("E-mail deve ser uma string.")
        if not email:
            raise ValueError("E-mail não pode ser vazio.")
        self._email = email

    def set_fone(self, fone):
        if not isinstance(fone, str):
            raise ValueError("Telefone deve ser uma string.")
        if not fone:
            raise ValueError("Telefone não pode ser vazio.")
        self._fone = fone

    def set_senha(self, senha):
        if not isinstance(senha, str):
            raise ValueError("Senha deve ser uma string.")
        if not senha:
            raise ValueError("Senha não pode ser vazia.")
        self._senha = senha


class Clientes:
    objetos = []  # Atributo estático

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        m = 0
        for c in cls.objetos:
            if c.get_id() > m:
                m = c.get_id()
        obj.set_id(m + 1)
        cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for c in cls.objetos:
            if c.get_id() == id:
                return c
        return None

    @classmethod
    def atualizar(cls, obj):
        c = cls.listar_id(obj.get_id())
        if c is not None:
            c.set_nome(obj.get_nome())
            c.set_email(obj.get_email())
            c.set_fone(obj.get_fone())
            c.set_senha(obj.get_senha())
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        c = cls.listar_id(obj.get_id())
        if c is not None:
            cls.objetos.remove(c)
            cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        cls.objetos.sort(key=lambda cliente: cliente.get_nome())
        return cls.objetos
    
    @classmethod
    def verificar_id_valido(cls, id):
        for obj in cls.objetos:
            if obj.get_id() == id:
                return True
        return False

    @classmethod
    def verificar_email_repetido(cls, e):
        for obj in cls.objetos:
            if obj.get_email() == e:
                return True
        return False

    @classmethod
    def salvar(cls):
        with open("clientes.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars)

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("clientes.json", mode="r") as arquivo:
                texto = json.load(arquivo)
                for obj in texto:
                    c = Cliente(obj["id"], obj["_nome"], obj["_email"], obj["_fone"], obj["_senha"])
                    cls.objetos.append(c)
        except FileNotFoundError:
            pass
