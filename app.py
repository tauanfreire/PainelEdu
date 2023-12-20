import pandas as pd
import streamlit as st
import funcoes

# Função para adicionar uma linha horizontal no Markdown
def markdown():
    st.markdown('<hr style="height:5px; border:none; color:rgba(red); background-color:rgba(0,0,0,0.3);"/>', unsafe_allow_html=True)

# Tela inicial
with st.columns(3)[1]:
    st.image("logotipo.png", width=200)
st.title('Dashboard de dados educacionais')
st.write("* by [Tauan Freire](https://www.instagram.com/tauanfreire.sn/)")

st.write("Este projeto tem como propósito desenvolver o Painel Edu, uma plataforma de análise e visualização de dados provindos do Google Sala de Aula. Considerando que dados são fundamentais para a compreensão do aprendizado, o Painel Edu se propõe a auxiliar professores e gestores na compreensão do processo educacional. Sendo assim, a intenção deste projeto é propor uma alternativa no sentido de encontrar novas perspectivas para contribuir com o progresso do ensino, além de incentivar a discussão na comunidade educacional acerca dos métodos, estratégias, ferramentas e técnicas que visem a otimização do processo de ensino-aprendizagem.")
markdown()

with st.sidebar.columns(3)[1]:
    st.image("menu.png", width=100)

# Inicialização
st.subheader('Bem-Vindo!')
tipo = st.radio(label="Selecione o tipo da sua base de dados", options=['csv', 'excel'])
arquivo = st.file_uploader(label="Faça o upload do seu arquivo")
markdown() 

#Verificando se o arquivo enviado é do tipo csv
if tipo == 'csv':
    if arquivo:
        csv = pd.read_csv(arquivo)
        df = pd.DataFrame(csv)
        #criando elementos no sidebar
        sb1 = st.sidebar.subheader('Análise dos dados!')
        sb2 = st.sidebar.selectbox('Selecione uma opção:', ['Selecione:', 'Sobre a base de dados', 'Gráficos'])
        
        if sb2 == 'Sobre a base de dados':
            funcoes.dataframeInfo(df)
            more = st.sidebar.multiselect('Quais dados você quer visualizar? ', ['Descrição', 'Tipo de dados'])
            
            if 'Descrição' in more:
                funcoes.descricao(df) 
            if 'Tipo de dados' in more:
                funcoes.tipoDados(df)  

        #plotando os graficos       
        elif sb2 == 'Gráficos':
            tipoDado = st.sidebar.selectbox('Tipo de dado:', ['Média', 'Mediana', 'Desvio Padrão', 'Maior e Menor Nota',
                                                              'Aluno x Aluno', 'Aluno x Turma'])
            tipoGrafico = st.sidebar.selectbox('Tipo de gráfico:', ['Barra','Linha', 'Área'])

            def lines(qtde):
                if tipoGrafico == 'Linha':
                        if len(qtde) < 2:
                            st.error('Selecione pelo menos duas colunas para visualizar o gráfico de linhas! ')
            def selectColunas(colunas):
                if not colunas:
                    st.warning("Selecione as colunas de notas no sidebar!", icon = "🚨")
            
            
            # Filtra as colunas selecionadas que são numéricas
            colunas = df.select_dtypes(include='number').columns.tolist()
            
            if colunas:
                if tipoDado == 'Média':
                    colunas = st.sidebar.multiselect('Selecione as colunas de notas: ', df.select_dtypes(include='number').columns.tolist())
                    # Calcula a média das colunas selecionadas

                    media_df = df[colunas].mean()  
                    media_df = pd.DataFrame(media_df, columns=['Media'])
                    st.dataframe(media_df)
                    media_df['Atividade'] = media_df.index
                    selectColunas(colunas)
                    if tipoGrafico == 'Linha':
                        lines(colunas)
                        funcoes.linechart(media_df, 'Media') 
                    elif tipoGrafico == 'Barra':
                        funcoes.barchart(media_df, 'Media')  
                    elif tipoGrafico == 'Área':
                        funcoes.areachart(media_df, 'Media')  

                elif tipoDado == 'Mediana':
                    colunas = st.sidebar.multiselect('Selecione as colunas de notas: ', df.select_dtypes(include='number').columns.tolist())
                    # Calcula a mediana das colunas selecionadas
                    mediana_df = df[colunas].median()  
                    mediana_df = pd.DataFrame(mediana_df, columns=['Mediana'])
                    selectColunas(colunas)
                    st.dataframe(mediana_df)
                    if tipoGrafico == 'Linha':
                        lines(colunas)
                        funcoes.linechart(mediana_df, 'Mediana')
                    elif tipoGrafico == 'Barra':
                        funcoes.barchart(mediana_df, 'Mediana')
                    elif tipoGrafico == 'Área':
                        funcoes.areachart(mediana_df, 'Mediana')    

                elif tipoDado == 'Desvio Padrão':
                    colunas = st.sidebar.multiselect('Selecione as colunas de notas: ', df.select_dtypes(include='number').columns.tolist())
                    # Calcula o desvio padrão das colunas selecionadas
                    desvio_padrao = df[colunas].std()  
                    desvio_padrao = pd.DataFrame(desvio_padrao, columns=['Desvio Padrão'])
                    st.dataframe(desvio_padrao)
                    selectColunas(colunas)
                    if tipoGrafico == 'Linha':
                        lines(colunas)
                        funcoes.linechart(desvio_padrao, 'Desvio Padrão')
                    elif tipoGrafico == 'Barra':
                        funcoes.barchart(desvio_padrao, 'Desvio Padrão')
                    elif tipoGrafico == 'Área':
                        funcoes.areachart(desvio_padrao, 'Desvio Padrão')    
                                         
                elif tipoDado == 'Maior e Menor Nota':
                    colunas = st.sidebar.multiselect('Selecione as colunas de notas: ', df.select_dtypes(include='number').columns.tolist())
                    # st.write('o')
                    selectColunas(colunas)
                    # Calcula as maiores e menores notas das colunas selecionadas
                    maiorMenor = df[colunas].agg(['max', 'min']).transpose()  
                    maiorMenor.columns = ['Maior Nota', 'Menor Nota']
                    st.dataframe(maiorMenor)
                    if tipoGrafico == 'Barra':
                        st.bar_chart(data=maiorMenor[['Maior Nota', 'Menor Nota']])
                    elif tipoGrafico == 'Linha':
                        lines(colunas)
                        funcoes.linechart(maiorMenor, ['Maior Nota', 'Menor Nota'])
                    elif tipoGrafico == 'Área':
                        funcoes.areachart(maiorMenor, ['Maior Nota', 'Menor Nota'])

                #Comparando Aluno x Aluno
                elif tipoDado == 'Aluno x Aluno':
                    st.subheader('Aluno x Aluno')
                    colunasNotas = st.sidebar.multiselect('Selecione as colunas de notas: ', df.select_dtypes(include='number').columns.tolist())
                    colunaAlunos = st.selectbox('Selecione a coluna de Alunos', df.select_dtypes(include='object').columns.tolist())

                    aluno1 = st.selectbox('Aluno 1: ', df[colunaAlunos].tolist())
                    aluno2 = st.selectbox('Aluno 2: ', df[colunaAlunos].tolist())
                    
                    # Filtrar as linhas correspondentes aos alunos selecionados e colunas de notas
                    alunoSelecionado1 = df[df[colunaAlunos] == aluno1]
                    alunoSelecionado2 = df[df[colunaAlunos] == aluno2]
                    markdown()
                    
                    df_aluno1 = pd.DataFrame(alunoSelecionado1, columns=colunasNotas)
                    df_aluno2 = pd.DataFrame(alunoSelecionado2, columns=colunasNotas)
                    df_aluno1 = df_aluno1.transpose()
                    df_aluno1['Atividade'] = df_aluno1.index
                    df_aluno2 = df_aluno2.transpose()
                    df_aluno2['Atividade'] = df_aluno2.index
                    df_alunos = pd.merge(df_aluno1, df_aluno2, on='Atividade')
                    df_alunos.columns = [aluno1,'Atividade', aluno2]

                    #Criando meu dataframe so com os alunos selecionados, e depois adicionando cada atividade como meu index
                    df_grafico = df_alunos[[aluno1, aluno2]]
                    df_grafico.index = colunasNotas
                    selectColunas(colunasNotas)

                    if tipoGrafico == 'Linha':
                        lines(colunasNotas)
                        if aluno1 == aluno2:
                            st.error("**PARA VISUALIZAR OS DADOS, O ALUNO 1 TEM QUER SER DIFERENTE DO ALUNO 2**", icon="⚠️")
                        #visualizando meu dataframe, e visualizando meu grafico de linha
                        st.dataframe(df_grafico)
                        st.line_chart(df_grafico, height=600)
                        markdown()
                    elif tipoGrafico == 'Barra':
                        st.bar_chart(df_grafico)
                    elif tipoGrafico == 'Área':
                        st.area_chart(df_grafico)


                elif tipoDado == 'Aluno x Turma':
                     #agora comparando um aluno com a turma
                    st.subheader('Aluno x Turma')
                    colunasNotas = st.sidebar.multiselect('Selecione as colunas de notas: ', df.select_dtypes(include='number').columns.tolist())
                    colunaAlunos = st.selectbox('Selecione a coluna de Alunos', df.select_dtypes(include='object').columns.tolist())
                    aluno = st.selectbox('Aluno: ', df[colunaAlunos].tolist())
                    
                    # Filtrar as linhas correspondentes ao alunos selecionado
                    alunoSelecionado = df[df[colunaAlunos] == aluno]

                    df_aluno = pd.DataFrame(alunoSelecionado, columns=colunasNotas)
                    df_aluno = df_aluno.transpose()
                    df_aluno['Atividade'] = df_aluno.index

                    #media da turma
                    mediaTurma = df[colunasNotas].mean().round(2)
                    
                    #converti mediaTurma de serie para um dataframe
                    df_mediaTurma = pd.DataFrame(mediaTurma)
                    
                    #criei uma coluna chamada atividade, e o valor de cada campu dessa coluna, é o valor do meu index, que no caso é minha atividade
                    df_mediaTurma['Atividade'] = df_mediaTurma.index
                    
                    #'Mergando meu aluno com minha turma a partir da coluna Atividade
                    alunoTurma = pd.merge(df_aluno, df_mediaTurma, on='Atividade')
                    
                    #renomeando minhas colunas
                    alunoTurma.columns = [aluno, 'Atividade', 'Media da Turma']
                    
                    #criando o dataframe so com as colunas aluno1 e 'media da turma
                    turmaGraf = alunoTurma[[aluno, 'Media da Turma']]
                    turmaGraf.index = colunasNotas
                    selectColunas(colunasNotas)
                    st.dataframe(turmaGraf)
                    if tipoGrafico == 'Linha':
                        st.line_chart(turmaGraf, height=600)
                    elif tipoGrafico == 'Barra':
                        st.bar_chart(turmaGraf, height=600)
                    elif tipoGrafico == 'Área':
                        st.area_chart(turmaGraf, height=600)
    


