import json
from datetime import datetime

class Horario:
    def __init__(self, id, data):
        self.id = id
        self.set_data(data)
        self.confirmado = False
        self.id_cliente = 0
        self.id_servico = 0

    def __str__(self):
        return f"{self.get_id()} - {self.get_data()}"

    def to_json(self):
        dic = {}
        dic["id"] = self.get_id()
        dic["data"] = self.get_data().strftime("%d/%m/%Y %H:%M")
        dic["confirmado"] = self.get_confirmado()
        dic["id_cliente"] = self.get_id_cliente()
        dic["id_servico"] = self.get_id_servico()
        return dic

    def get_id(self):
        return self.id

    def get_data(self):
        return self._data

    def get_confirmado(self):
        return self.confirmado

    def get_id_cliente(self):
        return self.id_cliente

    def get_id_servico(self):
        return self.id_servico

    def set_id(self, id):
        if not isinstance(id, int):
            raise ValueError("ID deve ser um inteiro.")
        self.id = id
        
    def set_data(self, data):
        if not isinstance(data, datetime):
            raise ValueError("Data deve ser um objeto datetime.")
        self._data = data

    def set_confirmado(self, confirmado):
        if not isinstance(confirmado, bool):
            raise ValueError("Confirmado deve ser um valor booleano.")
        self.confirmado = confirmado

    def set_id_cliente(self, id_cliente):
        if not (isinstance(id_cliente, int) or id_cliente is None) or (id_cliente is not None and id_cliente < 0):
            raise ValueError("ID do cliente deve ser um número inteiro positivo ou None.")
        self.id_cliente = id_cliente

    def set_id_servico(self, id_servico):
        if not (isinstance(id_servico, int) or id_servico is None) or (id_servico is not None and id_servico < 0):
            raise ValueError("ID do serviço deve ser um número inteiro positivo ou None.")
        self.id_servico = id_servico


class Horarios:
    objetos = []

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
            c.set_data(obj.get_data())
            c.set_confirmado(obj.get_confirmado())
            c.set_id_cliente(obj.get_id_cliente())
            c.set_id_servico(obj.get_id_servico())
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
    def verificar_servico_com_horario(cls, id):
        for obj in cls.objetos:
            if obj.get_id_servico() == id:
                return True
        return False

    @classmethod
    def verificar_cliente_com_horario(cls, id):
        for obj in cls.objetos:
            if obj.get_id_cliente() == id:
                return True
        return False
    
    @classmethod
    def salvar(cls):
        with open("horarios.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=Horario.to_json)

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("horarios.json", mode="r") as arquivo:
                texto = json.load(arquivo)
                for obj in texto:
                    c = Horario(obj["id"], datetime.strptime(obj["data"], "%d/%m/%Y %H:%M"))
                    c.set_confirmado(obj["confirmado"])
                    c.set_id_cliente(obj["id_cliente"])
                    c.set_id_servico(obj["id_servico"])
                    cls.objetos.append(c)
        except FileNotFoundError:
            pass
