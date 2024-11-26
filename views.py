from models.cliente import Cliente, Clientes
from models.horario import Horario, Horarios
from models.servico import Servico, Servicos
from datetime import datetime, timedelta

class View:
    def cliente_admin():
        for c in View.cliente_listar():
            if c.get_email() == "admin": return
        View.cliente_inserir("admin", "admin", "1234", "1234")

    def cliente_inserir(nome, email, fone, senha):
        if Clientes.verificar_email_repetido(email):
            raise ValueError("Insira um email único.")

        c = Cliente(0, nome, email, fone, senha)
        Clientes.inserir(c)

    def cliente_listar():
        return Clientes.listar()    

    def cliente_listar_id(id):
        return Clientes.listar_id(id)    

    def cliente_atualizar(id, nome, email, fone, senha):
        if Clientes.verificar_email_repetido(email):
            raise ValueError("Insira um email único.")
        c = Cliente(id, nome, email, fone, senha)
        Clientes.atualizar(c)

    def cliente_excluir(id):
        if Horarios.verificar_cliente_com_horario(id):
            raise ValueError("Esse cliente possui um horário agendado, não é possível deletá-lo.")
        c = Cliente(id, "aaa", "aaa", "aaa", "aaa")
        Clientes.excluir(c)    

    def cliente_autenticar(email, senha):
        for c in View.cliente_listar():
            if c.get_email() == email and c.get_senha() == senha:
                return {"id" : c.get_id(), "nome" : c.get_nome() }
        return None

    def horario_inserir(data, confirmado, id_cliente, id_servico):
        if not Clientes.verificar_id_valido(id_cliente) and id_cliente != None:
            raise ValueError("Insira um ID válido de cliente.")
        if not Servicos.verificar_id_valido(id_servico) and id_servico != None:
            raise ValueError("Insira um ID válido de serviço.")
        c = Horario(0, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        Horarios.inserir(c)

    def horario_listar():
        return Horarios.listar()    

    def horario_listar_disponiveis():
        horarios = View.horario_listar()
        disponiveis = []
        for h in horarios:
            if h.get_data() >= datetime.now() and h.get_id_cliente() == None: disponiveis.append(h)
        return disponiveis   

    def horario_atualizar(id, data, confirmado, id_cliente, id_servico):
        if not Clientes.verificar_id_valido(id_cliente):
            raise ValueError("Insira um ID válido de cliente.")
        if not Servicos.verificar_id_valido(id_servico):
            raise ValueError("Insira um ID válido de serviço.")
        c = Horario(id, data)
        c.set_confirmado(confirmado) 
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico) 
        Horarios.atualizar(c)

    def horario_excluir(id):
        if Horarios.listar_id(id).get_id_cliente() != 0:
            raise ValueError("Esse horário não pode ser excluido pois está reservado para um cliente.")
        c = Horario(id, None)
        Horarios.excluir(c)    

    def horario_abrir_agenda(data, hora_inicio, hora_fim, intervalo):
        try:
            di = datetime.strptime(data + " " + hora_inicio, "%d/%m/%Y %H:%M")
            df = datetime.strptime(data + " " + hora_fim, "%d/%m/%Y %H:%M")
        except ValueError:
            raise ValueError("A data ou hora fornecida está no formato incorreto. Use o formato 'dd/mm/aaaa' para a data e 'HH:MM' para a hora.")

        if di >= df:
            raise ValueError("A hora inicial não pode ser maior ou igual à hora final.")

        if not isinstance(intervalo, int) or intervalo <= 0:
            raise ValueError("O intervalo deve ser um número inteiro positivo.")

        x = di
        while x <= df:
            View.horario_inserir(x, False, None, None)
            x = x + timedelta(minutes=intervalo)

    def servico_inserir(descricao, valor, duracao):
        c = Servico(0, descricao, valor, duracao)
        Servicos.inserir(c)

    def servico_listar():
        return Servicos.listar()    

    def servico_listar_id(id):
        return Servicos.listar_id(id)    

    def servico_atualizar(id, descricao, valor, duracao):
        c = Servico(id, descricao, valor, duracao)
        Servicos.atualizar(c)

    def servico_excluir(id):
        if Horarios.verificar_servico_com_horario(id):
            raise ValueError("Esse serviço possui um horário agendado, portanto não é possível deletá-lo.")
        c = Servico(id, "aaa", 0, 0)
        Servicos.excluir(c)    
