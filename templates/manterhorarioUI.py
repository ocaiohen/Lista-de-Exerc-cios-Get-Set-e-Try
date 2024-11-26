import streamlit as st
import pandas as pd
from views import View
import time
from datetime import datetime

class ManterHorarioUI:
    def main():
        st.header("Cadastro de Horários")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterHorarioUI.listar()
        with tab2: ManterHorarioUI.inserir()
        with tab3: ManterHorarioUI.atualizar()
        with tab4: ManterHorarioUI.excluir()

    def listar():
        horarios = View.horario_listar()
        if len(horarios) == 0: 
            st.write("Nenhum horário cadastrado")
        else:  
            dic = []
            for obj in horarios:
                cliente = View.cliente_listar_id(obj.get_id_cliente())
                servico = View.servico_listar_id(obj.get_id_servico())
                cliente_nome = cliente.get_nome() if cliente is not None else None
                servico_descricao = servico.get_descricao() if servico is not None else None
                dic.append({
                    "id": obj.get_id(),
                    "data": obj.get_data(),
                    "confirmado": obj.get_confirmado(),
                    "cliente": cliente_nome,
                    "serviço": servico_descricao
                })
            
            df = pd.DataFrame(dic)
            st.dataframe(df)

    def inserir():
        clientes = View.cliente_listar()
        servicos = View.servico_listar()
        data = st.text_input("Informe a data e horário do serviço", datetime.now().strftime("%d/%m/%Y %H:%M"))
        confirmado = st.checkbox("Confirmado")
        cliente = st.selectbox("Informe o cliente", clientes, index=None)
        servico = st.selectbox("Informe o serviço", servicos, index=None)
        
        if st.button("Inserir"):
            horario_inserido = datetime.strptime(data, "%d/%m/%Y %H:%M")
            if horario_inserido <= datetime.now():
                st.error("O horário inserido deve ser posterior ao horário atual.")

            id_cliente = cliente.get_id() if cliente is not None else None
            id_servico = servico.get_id() if servico is not None else None
            
            try:
                View.horario_inserir(horario_inserido, confirmado, id_cliente, id_servico)
                st.success("Horário inserido com sucesso")
            except Exception as err:
                st.error(f"Erro: {err}")
            
            time.sleep(2)
            st.rerun()

    def atualizar():
        horarios = View.horario_listar()
        if len(horarios) == 0: 
            st.write("Nenhum horário cadastrado")
        else:
            clientes = View.cliente_listar()
            servicos = View.servico_listar()
            op = st.selectbox("Atualização de horário", horarios)
            data = st.text_input("Informe a nova data e horário do serviço", op.get_data().strftime("%d/%m/%Y %H:%M"))
            confirmado = st.checkbox("Nova confirmação", op.get_confirmado())
            id_cliente = None if op.get_id_cliente() in [0, None] else op.get_id_cliente()
            id_servico = None if op.get_id_servico() in [0, None] else op.get_id_servico()
            cliente = st.selectbox("Informe o novo cliente", clientes, next((i for i, c in enumerate(clientes) if c.get_id() == id_cliente), None))
            servico = st.selectbox("Informe o novo serviço", servicos, next((i for i, s in enumerate(servicos) if s.get_id() == id_servico), None))
            if st.button("Atualizar"):
                horario_inserido = datetime.strptime(data, "%d/%m/%Y %H:%M")
                # if horario_inserido <= datetime.now():
                #     st.error("O horário inserido deve ser posterior ao horário atual.")
                
                id_cliente = cliente.get_id() if cliente is not None else None
                id_servico = servico.get_id() if servico is not None else None
                try:
                    View.horario_atualizar(op.get_id(), horario_inserido, confirmado, id_cliente, id_servico)
                    st.success("Horário atualizado com sucesso")
                except Exception as err:
                    st.error(f"Erro: {err}")
                time.sleep(2)
                st.rerun()

    def excluir():
        horarios = View.horario_listar()
        if len(horarios) == 0: 
            st.write("Nenhum horário cadastrado")
        else:
            op = st.selectbox("Exclusão de horário", horarios)
            if st.button("Excluir"):
                try:
                    View.horario_excluir(op.get_id())
                    st.success("Horário excluído com sucesso")
                except Exception as err:
                    st.error(f"Erro: {err}")
                time.sleep(2)
                st.rerun()
