import json

class Servico:
    def __init__(self, id, descricao, valor, duracao):
        self.id = id
        self.set_descricao(descricao)
        self.set_valor(valor)
        self.set_duracao(duracao)

    def __str__(self):
        return f"{self.get_id()} - {self.get_descricao()} - R$ {self.get_valor():.2f} - {self.get_duracao()} min"

    def to_json(self):
        dic = {}
        dic["id"] = self.id
        dic["descricao"] = self.descricao
        dic["valor"] = self.valor
        dic["duracao"] = self.duracao
        return dic

    def get_id(self):
        return self.id

    def get_descricao(self):
        return self._descricao

    def get_valor(self):
        return self._valor

    def get_duracao(self):
        return self._duracao
    
    def set_id(self, id):
        if not isinstance(id, int):
            raise ValueError("ID deve ser um inteiro.")
        self.id = id
    
    def set_descricao(self, descricao):
        if not isinstance(descricao, str):
            raise ValueError("Descrição deve ser uma string.")
        if not descricao:
            raise ValueError("Descrição não pode ser vazia.")
        self._descricao = descricao

    def set_valor(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("Valor deve ser um número positivo.")
        self._valor = valor

    def set_duracao(self, duracao):
        if not isinstance(duracao, (int, float)) or duracao < 0:
            raise ValueError("Duração deve ser um número positivo.")
        self._duracao = duracao


class Servicos:
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
            c.set_descricao(obj.get_descricao())
            c.set_valor(obj.get_valor())
            c.set_duracao(obj.get_duracao())
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
        return cls.objetos

    @classmethod
    def verificar_id_valido(cls, id):
        for obj in cls.objetos:
            if obj.get_id() == id:
                return True
        return False


    @classmethod
    def salvar(cls):
        with open("servicos.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars)

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("servicos.json", mode="r") as arquivo:
                texto = json.load(arquivo)
                for obj in texto:
                    c = Servico(obj["id"], obj["_descricao"], obj["_valor"], obj["_duracao"])
                    cls.objetos.append(c)
        except FileNotFoundError:
            pass
