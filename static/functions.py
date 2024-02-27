@app.route('/land_page3_requisicao', methods=['POST'])
def land_page3_requisicao():
    """
    Função responsável por processar uma requisição de envio de formulário de contato.
    Extrai os dados do formulário, como nome, e-mail, telefone, cidade, curso e ID de log,
    e os armazena no banco de dados. Além disso, atualiza o registro de log associado à ação.

    Parâmetros:
        Nenhum parâmetro de entrada explícito.
        Utiliza o objeto 'request.form' para extrair os dados do formulário.

    Retorna:
        Resposta JSON com status 200 se a operação for bem-sucedida.

    Observações:
        - A função é utilizada para processar envios de formulários de contato em um aplicativo web.
        - Realiza conexão com banco de dados para inserção de novos registros.
        - Atualiza o estado do registro de log associado à ação.
        - Manipula exceções e retorna mensagens de erro caso ocorram problemas durante a operação.
    """
    
    from datetime import datetime
    
    nome = (request.form['nome'])
    email = (request.form['email'])
    telefone = (request.form['telefone'])
    cidade = (request.form['cidade']).lower()
    curso = (request.form['curso']).lower()
    id_log = (request.form['id_log'])
     
    try: 
        data_agendamento = datetime.strftime(datetime.strptime(request.form['data_agendamento'], '%Y-%m-%d'), '%d/%m/%Y') 
    except:
        data_agendamento = None

    try:
        conn = POOL.connection()
        cursor = conn.cursor()
    except Exception as err:
        return f"Erro de conexão ao banco de dados\n{err}"

    try:
        cursor.execute("select id from in.contato_leads where id = (select max(id) from in.contato_leads)")
        max_id_central = cursor.fetchone()
        max_id_central = str(max_id_central).replace("(", "").replace(",)", "")
        max_id_central = int(max_id_central)

        id = max_id_central + 1
        id = str(id)

        query = f"INSERT INTO in.contato_leads (id, nome, telefone, agendamento, data_cadastro, cidade, curso, origem) VALUES ('{id}', '{nome}', '{telefone}', '{data_agendamento}', '{tempo_data_invertida3()}', '{cidade}', '{curso}', 'landing_page');"
        cursor.execute(query)

        cursor.execute(f"UPDATE log_face SET estado = '1' WHERE id = '{id_log}'")

    except Exception as err:
        cursor.close() 
        return jsonify({"error": f"Erro durante a inserção: {err}"}), 500
        
    cursor.close()
    return jsonify({"status": 200}), 200


@app.route('/landing_page', methods=['GET', 'POST'])
def landing_page3():
    """
    Função responsável por processar uma requisição para a página de destino do aplicativo web.
    Recupera parâmetros da URL, como cidade e curso, e realiza operações de registro de atividade do usuário
    no banco de dados. Em seguida, renderiza um template HTML com base nas informações obtidas.

    Parâmetros:
        Nenhum parâmetro de entrada explícito.
        Utiliza o objeto 'request' para recuperar os argumentos da URL.

    Retorna:
        Renderização do template HTML 'landing_p.html' com as seguintes informações:
        - cidade: Cidade selecionada ou padrão (Salvador).
        - localizacao_unidade: Dicionário contendo informações de endereço das unidades em diferentes cidades.
        - curso: Curso selecionado ou padrão (Programação Full Stack).
        - informacoes_curso: Dicionário contendo informações detalhadas sobre diferentes cursos disponíveis.
        - id_log: ID de registro de atividade, se aplicável.

    Observações:
        - A função integra um sistema web que registra atividades de usuários e exibe informações de cursos.
        - Realiza conexão com banco de dados para registro de atividades do usuário.
        - Calcula diferenças de tempo entre registros para controle de atividade.
        - Pode haver oportunidades de simplificação e otimização do código para melhor legibilidade e desempenho.
    """

    cidade = request.args.get('ci')
    curso = request.args.get('cur')

    if cidade != None:
        try:
            cidade = cidade.upper()
        except:
            ...
        
    if curso != None:
        try:
            curso = curso.upper()
        except:
            ...
            
    informacoes_curso = {
        'PROGRAMAÇÃO FULL STACK': {
            'link_video': 'https://www.youtube.com/embed/WKeyh7c4rVA?si=t8fN0f2wOyTeR8dl',
            'ementa': 'LÓGICA DE PROGRAMAÇÃO, PYTHON, HTML/CSS, JAVASCRIPT',
            'descricao': "Para quem quer entrar nas profissões de desenvolvimento de sistemas, aplicativos, IA, e web. Do front end ao back end.",
            'css_div': 'first_box',
            'css_i': 'fa-solid fa-code',
            'salarios': {
                'junior': '3.812,00',
                'pleno': '6.491,00',
                'senior': '11.993,00',
            },
        },
        'ANÁLISE DE DADOS': {
            'link_video': 'https://www.youtube.com/embed/WKeyh7c4rVA?si=t8fN0f2wOyTeR8dl',
            'ementa': 'LÓGICA DE PROGRAMAÇÃO, PYTHON, DATA SCIENCE PRO, PROJETO',
            'descricao': "Torne-se um especialista em dados com PYTHON. Entre na área mais bem pagad a programação e domine data sciente no nível avançado.",
            'css_div': 'first_box',
            'css_i': 'fa-solid fa-magnifying-glass-chart',
            'salarios': {
                'junior': '3.812,00',
                'pleno': '6.491,00',
                'senior': '11.993,00',
            },
        },
        'MARKETING DIGITAL': {
            'link_video': 'https://www.youtube.com/embed/SwXLLp2tYLk?si=zZg6R1jXzB4ySZgz',
            'ementa': 'INTRODUÇÃO DE MARKETING COM CHAT GPT, CRIAÇÃO DE CRIATIVOS COM IA E CANVA, REDES SOCIAIS (MÍDIA ORGÂNICA), TRÁFEGO PAGO COM FACEBOOK ADS(INSTAGRAM), GOOGLE SEO E GOOGLE ANALYTICS',
            'descricao': 'Aprenda a criar campanhas completas de marketing digital e gerenciar redes sociais de forma éficaz.',
            'css_div': 'first_box',
            'css_i': 'fa-solid fa-comments-dollar',
            'salarios': {
                'junior': '2.250,00',
                'pleno': '4.500,00',
                'senior': '9.000,00',
            },
        },
        'FOTOGRAFIA DESIGN': {
            'link_video': 'https://www.youtube.com/embed/yw54IkUAztM?si=DCEfd9-PkZ7cvnbE',
            'ementa': 'FOTOGRAFIA, PÓS PRODUÇÃO, LIGHTROOM, PHOTOSHOP',
            'descricao': 'Torne-se um diretor de fotografia profissional e aprenda a criar composições incríveis.',
            'css_div': 'first_box' ,
            'css_i': 'fa-solid fa-camera-retro',
            'salarios': {
                'junior':'1.750,00',
                'pleno': '4.500,00',
                'senior': '6.000,00',
            },
        },

        'DESIGN FULL STACK': {
            'link_video': 'https://www.youtube.com/embed/oFsEKFamIV0?si=PMsot3UPvyKLh8WE',
            'ementa': 'FOTOGRAFIA DIGITAL, EDIÇÃO DE IMAGENS, PRODUÇÃO GRÁFICA, CRIAÇÃO AUDIOVISUAL, EDIÇÃO DE VÍDEO DIGITAL',
            'descricao': 'Para quem busca entrar no universo da inúdistria criativa e das novas técnicas da arte digital.',
            'css_div': 'first_box',
            'css_i': 'fa-solid fa-pen-ruler',
            'salarios': {
                'junior': '3.000,00',
                'pleno': '6.000,00',
                'senior':'Mais de R$ 8.000,00!!!',
            },
        },
        'FILM DESIGN': {
            'link_video': 'https://www.youtube.com/embed/5TGI7GfSccU?si=e0VrLWLe0H8O2PAu',
            'ementa': 'NARRATIVA AUDIOVISUAL, CAPTURA DE VÍDEO, EDIÇÃO DE VÍDEO, EDIÇÃO DE ÁUDIO, PÓS-PRODUÇÃO, COLORIZAÇÃO',
            'descricao': 'Aprenda em 14 meses a se tornar um expert na área de vídeos e efeitos especiais.',
            'css_div': 'first_box',
            'css_i': 'class="fa-solid fa-film',
            'salarios': {
                'junior':'1.505,00',
                'pleno': '2.125,00',
                'senior': '3.021,00',
            },
        },
    }

    localizacao_unidade = {
        'SALVADOR': {
            'endereco':"https://www.google.com.br/maps/place/Infinity+School/@-12.9766837,-38.4593614,17z/data=!3m1!4b1!4m6!3m5!1s0x7161bfce64f7c2d:0x8d355fdcd1358496!8m2!3d-12.9766837!4d-38.4567811!16s%2Fg%2F11f7kj88dl?entry=ttu",
            'local': "Alameda Salvador, 1057, Edf. Salvador Shopping Business, Torre Europa, Sala 310.",
        },
        'FORTALEZA': {
            'endereco':"https://www.google.com.br/maps/place/Av.+Santos+Dumont+-+Aldeota,+Fortaleza+-+CE/@-3.7349664,-38.5048436,17z/data=!3m1!4b1!4m6!3m5!1s0x7c74881b09b88ef:0xe6f7c3f410959f98!8m2!3d-3.7349664!4d-38.5022633!16s%2Fg%2F121w6t2b?entry=ttu",
            'local': "Avenida Santos Dumont, Aldeota",
        },
        'BELO HORIZONTE': {
            'endereco':"https://www.google.com.br/maps/place/Av.+do+Contorno,+6480+-+01+-+Santa+Efigênia,+Belo+Horizonte+-+MG,+30110-017/@-19.9396346,-43.9421587,17z/data=!3m1!4b1!4m5!3m4!1s0xa699d747f7e80f:0x4aa5ffb63e211c55!8m2!3d-19.9396346!4d-43.9395784?entry=ttu",
            'local': "Avenida do Contorno, 6480, Loja 01, Savassi",
        },    
    }

    if cidade == None or cidade not in localizacao_unidade:
        cidade = "SALVADOR"
    if curso == None or curso not in informacoes_curso:
        curso = "PROGRAMAÇÃO FULL STACK"

    try:
        conn = POOL.connection()
        cursor = conn.cursor()
    except Exception as err:
        return f"Erro de conexão ao banco de dados\n{err}"

    try:
        cursor.execute(f"SELECT tempo FROM in.log_face ORDER BY id DESC LIMIT 1")
        rest = cursor.fetchall()
    except Exception as err:
        return f"Erro de conexão ao banco de dados\n{err}"

    rest = str(rest).replace("((", "").replace(",),)", "").replace("'", "").replace('"', '').replace('(', "").replace(")","").replace(",", "")

    tempo_registrado = rest

    tempo_agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
    date_format = "%d/%m/%Y %H:%M:%S.%f"
    time1 = datetime.strptime(tempo_registrado, date_format)
    time2 = datetime.strptime(tempo_agora, date_format)
    diff = time2 - time1
    days = diff.days
    days_to_hours = days * 24
    diff_btw_two_times = (diff.seconds) / 3600
    diferenca_horas = days_to_hours + diff_btw_two_times
    diferenca_horas = float(diferenca_horas)
    id_log = ""
    if (diferenca_horas != 0.004):
        try:
            conn = POOL.connection()
            cursor = conn.cursor()
        except Exception as err:
            return f"Erro de conexão ao banco de dados\n{err}"

        try:
            cursor.execute("select id from in.log_face where id = (select max(id) from in.log_face)")
            max_id_central = cursor.fetchone()
            max_id_central = str(max_id_central).replace("(", "").replace(",)", "")
            max_id_central = int(max_id_central)

            id = max_id_central + 1
            id_log = str(id)

            print(tempo_agora)

            query = f"INSERT INTO in.log_face (id, data, curso, cidade, tempo, html) VALUES ('{id_log}', '{tempo_data_invertida3()}', '{curso}', '{cidade}', '{tempo_agora}', 'landing_page_v1');"
            cursor.execute(query)
        except Exception as err:
            cursor.close()
            return jsonify({"error": f"Erro durante a inserção: {err}"}), 500

    return render_template('landing_p.html', cidade=cidade, localizacao_unidade=localizacao_unidade, curso=curso,  informacoes_curso=informacoes_curso, id_log=id_log)
