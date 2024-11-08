import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregando os dados
df_tickets = pd.read_excel('tickets_TI_ficticios_varied_analistas.xlsx')

# Configuração do Streamlit
st.title("Análise de Atendimentos de TI")

# 1. Número de Tickets por Analista
st.subheader("Número de Tickets por Analista")
analista_counts = df_tickets['Analista'].value_counts()
fig1, ax1 = plt.subplots()
analista_counts.plot(kind='bar', color='orange', ax=ax1)
ax1.set_title("Número de Tickets por Analista")
ax1.set_xlabel("Analista")
ax1.set_ylabel("Número de Tickets")
st.pyplot(fig1)

# 2. Contagem de Tickets por Status
st.subheader("Contagem de Tickets por Status")
status_counts = df_tickets['Status'].value_counts()
fig2, ax2 = plt.subplots()
status_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax2, startangle=90)
ax2.set_ylabel("")
ax2.set_title("Contagem de Tickets por Status")
st.pyplot(fig2)

# 3. Contagem de Tickets por Assunto
st.subheader("Contagem de Tickets por Assunto")
assunto_counts = df_tickets['Assunto'].value_counts()
fig3, ax3 = plt.subplots()
assunto_counts.plot(kind='bar', color='skyblue', ax=ax3)
ax3.set_title("Contagem de Tickets por Assunto")
ax3.set_xlabel("Assunto")
ax3.set_ylabel("Número de Tickets")
st.pyplot(fig3)

# 4. Tickets por Nível de Urgência
st.subheader("Tickets por Nível de Urgência")
urgencia_counts = df_tickets['Urgência'].value_counts()
fig4, ax4 = plt.subplots()
urgencia_counts.plot(kind='bar', color='salmon', ax=ax4)
ax4.set_title("Tickets por Nível de Urgência")
ax4.set_xlabel("Urgência")
ax4.set_ylabel("Número de Tickets")
st.pyplot(fig4)

# 5. Top 10 Clientes por Número de Tickets
st.subheader("Top 10 Clientes por Número de Tickets")
top_clients = df_tickets['Cliente (Completo)'].value_counts().nlargest(10)
fig5, ax5 = plt.subplots()
top_clients.plot(kind='bar', color='purple', ax=ax5)
ax5.set_title("Top 10 Clientes por Número de Tickets")
ax5.set_xlabel("Cliente (Completo)")
ax5.set_ylabel("Número de Tickets")
st.pyplot(fig5)

# 6. Tickets por Área de Negócio
st.subheader("Tickets por Área de Negócio")
area_counts = df_tickets['Área de Negócio'].value_counts()
fig6, ax6 = plt.subplots()
area_counts.plot(kind='bar', color='teal', ax=ax6)
ax6.set_title("Tickets por Área de Negócio")
ax6.set_xlabel("Área de Negócio")
ax6.set_ylabel("Número de Tickets")
st.pyplot(fig6)

# 7. Tempo Médio de Fechamento por Mês de Abertura
st.subheader("Tempo Médio de Fechamento por Mês de Abertura")
df_tickets['Tempo de Fechamento (dias)'] = (df_tickets['Data de Fechamento'] - df_tickets['Aberto em']).dt.days
average_closure_time = df_tickets.groupby(df_tickets['Aberto em'].dt.to_period('M'))['Tempo de Fechamento (dias)'].mean()

fig7, ax7 = plt.subplots()
average_closure_time.plot(kind='line', marker='o', color='orange', ax=ax7)
ax7.set_title("Tempo Médio de Fechamento por Mês de Abertura")
ax7.set_xlabel("Mês de Abertura")
ax7.set_ylabel("Tempo Médio de Fechamento (dias)")
st.pyplot(fig7)

# Exibindo a tabela de dados
st.subheader("Dados de Atendimentos de TI")
st.dataframe(df_tickets)
