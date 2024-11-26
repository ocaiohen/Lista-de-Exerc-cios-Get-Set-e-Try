import streamlit as st
import pandas as pd
from views import View
import time

class ManterClienteUI:
    def main():
        st.header("Cadastro de Clientes")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterClienteUI.listar()
        with tab2: ManterClienteUI.inserir()
        with tab3: ManterClienteUI.atualizar()
        with tab4: ManterClienteUI.excluir()

    def listar():
        clientes = View.cliente_listar()
        if len(clientes) == 0: 
            st.write("Nenhum cliente cadastrado")
        else:    
            dic = []
            for obj in clientes: 
                dic.append({
                    "id": obj.get_id(),
                    "nome": obj.get_nome(),
                    "email": obj.get_email(),
                    "fone": obj.get_fone(),
                    "senha": obj.get_senha()
                })
            df = pd.DataFrame(dic)
            st.dataframe(df)

    def inserir():
        nome = st.text_input("Informe o nome do cliente")
        email = st.text_input("Informe o e-mail")
        fone = st.text_input("Informe o fone")
        senha = st.text_input("Informe a senha", type="password")
        if st.button("Inserir"):
            try:
                View.cliente_inserir(nome, email, fone, senha)
                st.success("Cliente inserido com sucesso")
            except Exception as err:
                    st.error(f"Erro: {err}")
            time.sleep(2)
            st.rerun()

    def atualizar():
        clientes = View.cliente_listar()
        if len(clientes) == 0: 
            st.write("Nenhum cliente cadastrado")
        else:
            op = st.selectbox("Atualização de cliente", clientes)
            nome = st.text_input("Informe o novo nome do cliente", op.get_nome())
            email = st.text_input("Informe o novo e-mail", op.get_email())
            fone = st.text_input("Informe o novo fone", op.get_fone())
            senha = st.text_input("Informe a nova senha", op.get_senha(), type="password")
            if st.button("Atualizar"):
                try:
                    View.cliente_atualizar(op.get_id(), nome, email, fone, senha)
                    st.success("Cliente atualizado com sucesso")
                except Exception as err:
                    st.error(f"Erro: {err}")
                time.sleep(2)
                st.rerun()

    def excluir():
        clientes = View.cliente_listar()
        if len(clientes) == 0: 
            st.write("Nenhum cliente cadastrado")
        else:
            op = st.selectbox("Exclusão de cliente", clientes)
            if st.button("Excluir"):
                try: 
                    View.cliente_excluir(op.get_id())
                    st.success("Cliente excluído com sucesso")
                except Exception as err:
                    st.error(f"Erro: {err}")
                time.sleep(2)
                st.rerun()
