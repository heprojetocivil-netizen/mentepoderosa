import streamlit as st
from groq import Groq
from datetime import datetime
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MENTE PODEROSA", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

    .stApp { background-color: #FFFFFF; color: #000000; font-family: 'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { display: none; }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>div {
        background-color: #F5F3FF !important;
        color: #000000 !important;
        border: 1px solid #C4B5FD !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(135deg, #4C1D95, #7C3AED) !important;
        color: white !important; font-weight: 600; border: none;
        box-shadow: 2px 2px 8px rgba(76,29,149,0.25);
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { background: linear-gradient(135deg, #3B0764, #4C1D95) !important; transform: translateY(-1px); }

    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1A1A2E !important; }
    p, span, label, div { color: #1A1A2E !important; font-family: 'DM Sans', sans-serif; }

    .card {
        background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #C4B5FD; margin-bottom: 15px;
        color: #1A1A2E; box-shadow: 0 2px 12px rgba(76,29,149,0.08);
        white-space: pre-wrap;
    }
    .card-dark {
        background: linear-gradient(135deg, #0F0420 0%, #1A0535 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #7C3AED; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-dark, .card-dark * { color: #DDD6FE !important; }

    .card-blue {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #93C5FD; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-green {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #86EFAC; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-pink {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4EE 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #FFB6C1; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-orange {
        background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #FDBA74; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-teal {
        background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #5EEAD4; margin-bottom: 15px;
        white-space: pre-wrap;
    }

    .badge         { background: #4C1D95; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-verde   { background: #059669; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-azul    { background: #1D4ED8; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-rosa    { background: #BE185D; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-teal    { background: #0D9488; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }

    .stat-box { background: #F5F3FF; border-radius: 12px; padding: 18px; text-align: center; border: 1px solid #C4B5FD; }
    .stat-numero { font-size: 2em; font-weight: 700; color: #4C1D95 !important; font-family: 'Playfair Display', serif; }

    .hist-item { background: #F5F3FF; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; border-left: 4px solid #7C3AED; }

    .perfil-btn>button {
        background: linear-gradient(135deg, #4C1D95, #7C3AED) !important;
        color: white !important; font-weight: 700 !important;
        border-radius: 12px !important; height: 3em !important;
    }

    .divider { border: none; height: 1px; background: linear-gradient(to right, transparent, #C4B5FD, transparent); margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_mente():
    return {"perfis": {}}

_cache = get_cache_mente()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_sessoes', 'conteudos_salvos',
    'maior_bloqueio', 'objetivo_mental', 'estado_emocional',
    'crencas_limitantes', 'sessoes_meditacao', 'diario_entradas',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_sessao(tipo: str, tema: str, conteudo: str):
    st.session_state.historico_sessoes.append({
        'data':    datetime.now().strftime('%d/%m %H:%M'),
        'tipo':    tipo,
        'tema':    tema,
        'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':             "Login",
    'usuario':           "",
    'api_key':           "",
    'pagina':            "Home",
    'historico_sessoes': [],
    'conteudos_salvos':  [],
    'maior_bloqueio':    "",
    'objetivo_mental':   "",
    'estado_emocional':  "Neutro",
    'crencas_limitantes':"",
    'sessoes_meditacao': 0,
    'diario_entradas':   [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- MOTOR DE IA ---
def mente_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um especialista em neurolinguística (PNL), meditação e reprogramação mental.
Usuário: {st.session_state.usuario}.
Maior bloqueio atual: {st.session_state.maior_bloqueio or 'não informado'}.
Objetivo mental: {st.session_state.objetivo_mental or 'não informado'}.
Estado emocional: {st.session_state.estado_emocional}.
{system_extra}
PRINCÍPIOS:
- Baseie-se em PNL, Mindfulness, Terapia Cognitivo-Comportamental e Neurociência
- Tom acolhedor, seguro e transformador — nunca julgue
- Linguagem acessível, sem jargões técnicos desnecessários
- Sempre oriente a buscar ajuda profissional para casos clínicos sérios
- Escreva em português brasileiro natural e humanizado"""
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total   = len(st.session_state.historico_sessoes)
    salvos  = len(st.session_state.conteudos_salvos)
    medit   = st.session_state.sessoes_meditacao
    diario  = len(st.session_state.diario_entradas)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#F5F3FF;border:1px solid #C4B5FD;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} sessões · "
            f"{medit} meditações · {diario} entradas no diário · {salvos} salvos</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"mente_poderosa_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🧠 MENTE PODEROSA")
        st.markdown("**Neurolinguística, Meditação e Reprogramação Mental com Inteligência Artificial**")

        st.markdown("""<div style="background:#F5F3FF;border:1px solid #C4B5FD;border-radius:10px;
        padding:10px 16px;margin:10px 0 16px 0;font-size:0.88em;color:#1A1A2E;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</strong><br>
        🔗 <a href="https://quizcompremios.com.br/" target="_blank"
        style="color:#4C1D95;font-weight:600;text-decoration:none;">quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        # ── PERFIS SALVOS NO SERVIDOR ─────────────────────────
        perfis = perfis_salvos()
        if perfis:
            st.markdown("#### 🧠 Mente Poderosa — clique para acessar seus dados")
            st.caption("Seu progresso mental está no servidor. Um clique e você entra.")
            chave_rapida = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_rapida")
            for nome_p in perfis:
                dados_p  = carregar_perfil_cache(nome_p)
                total_p  = len(dados_p.get('historico_sessoes', [])) if dados_p else 0
                medit_p  = dados_p.get('sessoes_meditacao', 0) if dados_p else 0
                obj_p    = dados_p.get('objetivo_mental', '') if dados_p else ''
                st.markdown('<div class="perfil-btn">', unsafe_allow_html=True)
                if st.button(
                    f"🧠 {nome_p}  —  {total_p} sessões  ·  {medit_p} meditações  {('· ' + obj_p[:30]) if obj_p else ''}",
                    key=f"perfil_{nome_p}",
                    use_container_width=True
                ):
                    if not chave_rapida.strip():
                        st.warning("Cole sua chave API acima antes de entrar.")
                    else:
                        st.session_state.usuario = nome_p
                        st.session_state.api_key = chave_rapida
                        carregar_json_sessao(dados_p)
                        st.session_state.etapa = "App"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("**Ou entre com outro nome:**")

        nome  = st.text_input("Seu Nome:")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="chave_nova")

        if not perfis:
            st.markdown("""<div style="background:#F5F3FF;border:1px solid #C4B5FD;border-radius:10px;
            padding:12px 16px;font-size:0.86em;color:#1A1A2E;line-height:1.7;margin:10px 0;">
            📥 <strong>Seus dados sumiram?</strong> Isso acontece quando o servidor reinicia.<br>
            Selecione abaixo o arquivo <strong>.json</strong> que você salvou antes — seu progresso volta completo.
            </div>""", unsafe_allow_html=True)
            arq_login = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_login")
        else:
            arq_login = None

        dados_login = None
        if arq_login is not None:
            try:
                dados_login = json.load(arq_login)
                nome_login  = dados_login.get('usuario', '')
                st.success(f"✅ Dados de **{nome_login}** reconhecidos! Clique em Entrar.")
            except Exception:
                st.error("Arquivo inválido.")
                dados_login = None

        if st.button("✨ ENTRAR E TRANSFORMAR SUA MENTE"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

        st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#4C1D95;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div style="background:#F5F3FF;border:1px solid #C4B5FD;border-radius:10px;
        padding:10px 14px;font-size:0.8em;color:#6D28D9;line-height:1.6;">
        ⚠️ <strong>Aviso importante:</strong> Este app é uma ferramenta de desenvolvimento pessoal e bem-estar.
        Não substitui acompanhamento psicológico ou psiquiátrico profissional.
        Em casos de crise, procure um profissional de saúde mental.
        </div>""", unsafe_allow_html=True)

# ============================================================
# TELA: APP
# ============================================================
elif st.session_state.etapa == "App":

    barra_salvar()

    # NAVBAR
    cols = st.columns(9)
    paginas_nav = [
        ("🏠", "Home"),
        ("🧘", "Meditacao"),
        ("🗣️", "PNL"),
        ("💬", "Afirmacoes"),
        ("😴", "Sono"),
        ("😰", "Ansiedade"),
        ("🎯", "Visualizacao"),
        ("📖", "Diario"),
        ("❤️", "Salvos"),
    ]
    nomes_nav = {
        "Home":        "Painel Principal",
        "Meditacao":   "Meditação Guiada",
        "PNL":         "Reprogramação com PNL",
        "Afirmacoes":  "Afirmações Personalizadas",
        "Sono":        "Protocolo do Sono",
        "Ansiedade":   "Gestão de Ansiedade",
        "Visualizacao":"Visualização Criativa",
        "Diario":      "Diário Mental",
        "Salvos":      "Salvos e Progresso",
    }
    for i, (icone, pagina) in enumerate(paginas_nav):
        if cols[i].button(icone, key=f"nav_{pagina}", help=nomes_nav[pagina]):
            st.session_state.pagina = pagina
            st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ========================
    # HOME
    # ========================
    if st.session_state.pagina == "Home":
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Bem-vindo, {st.session_state.usuario} 🧠✨")
            st.markdown("<span class='badge'>Jornada Mental</span>", unsafe_allow_html=True)
        with col_r:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Sair"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        # AVISO SE DADOS SUMIRAM
        total_h = len(st.session_state.historico_sessoes)
        if total_h == 0 and st.session_state.sessoes_meditacao == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")
            st.markdown("<br>", unsafe_allow_html=True)

        # PERFIL MENTAL
        st.markdown("#### 🌱 Seu perfil mental")
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.maior_bloqueio   = st.text_input(
                "Seu maior bloqueio mental hoje:", value=st.session_state.maior_bloqueio,
                placeholder="ex: ansiedade, baixa autoestima, procrastinação, medo de falhar...")
            st.session_state.objetivo_mental  = st.text_input(
                "O que você quer transformar na sua mente:", value=st.session_state.objetivo_mental,
                placeholder="ex: ter mais confiança, parar de me sabotar, dormir melhor...")
        with col_b:
            st.session_state.estado_emocional = st.select_slider(
                "Como você está agora:", options=[
                    "Muito mal 😔","Mal 😟","Neutro 😐","Bem 🙂","Muito bem 😁"
                ], value=st.session_state.estado_emocional if st.session_state.estado_emocional in
                ["Muito mal 😔","Mal 😟","Neutro 😐","Bem 🙂","Muito bem 😁"] else "Neutro 😐")
            st.session_state.crencas_limitantes = st.text_area(
                "Crenças que te limitam (opcional):", value=st.session_state.crencas_limitantes,
                height=80,
                placeholder="ex: não sou inteligente o suficiente, não mereço ser feliz, sempre falho...")

        st.markdown("<br>", unsafe_allow_html=True)

        # MÉTRICAS
        tipos = {}
        for s in st.session_state.historico_sessoes:
            tipos[s['tipo']] = tipos.get(s['tipo'], 0) + 1

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_h}</div><div>Sessões realizadas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.sessoes_meditacao}</div><div>Meditações 🧘</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.diario_entradas)}</div><div>Entradas no diário</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.conteudos_salvos)}</div><div>Conteúdos salvos</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('PNL',0)}</div><div>Sessões de PNL</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>💡 <em>'A mente que se abre a uma nova ideia jamais volta ao seu tamanho original.'</em> — Albert Einstein</div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada aba faz")
        guia = {
            "🧘 Meditação":          "Scripts de meditação guiada personalizados para o seu momento",
            "🗣️ PNL":               "Técnicas de reprogramação: ancoragem, reframing, linha do tempo",
            "💬 Afirmações":         "Afirmações criadas para o SEU problema real — não as genéricas",
            "😴 Sono":               "Protocolo completo para dormir melhor e acordar descansado",
            "😰 Ansiedade":          "Técnicas de respiração, grounding e protocolo de crise",
            "🎯 Visualização":       "Script de visualização criativa do futuro que você quer construir",
            "📖 Diário Mental":      "Prompts de reflexão diária para autoconhecimento profundo",
            "❤️ Salvos":             "Seus conteúdos favoritos e histórico completo",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_sessoes:
            st.markdown("### 🕐 Últimas Sessões")
            for item in reversed(st.session_state.historico_sessoes[-4:]):
                st.markdown(
                    f"<div class='hist-item'>"
                    f"<span class='badge'>{item['tipo']}</span> "
                    f"<span class='badge-teal'>{item['tema'][:30]}</span> "
                    f"<small style='color:#888'>{item['data']}</small></div>",
                    unsafe_allow_html=True
                )

    # ========================
    # MEDITAÇÃO GUIADA
    # ========================
    elif st.session_state.pagina == "Meditacao":
        st.header("🧘 Meditação Guiada")
        st.markdown("Scripts de meditação personalizados — para o seu momento e o que você precisa agora.")

        col1, col2 = st.columns(2)
        with col1:
            objetivo_med = st.selectbox("O que você quer trabalhar:", [
                "Ansiedade e tensão","Foco e clareza mental","Autoestima e autoconfiança",
                "Sono e relaxamento profundo","Gratidão e paz interior",
                "Cura emocional","Energia e motivação","Presença e mindfulness",
            ])
            tempo_med    = st.selectbox("Tempo disponível:", [
                "5 minutos (meditação rápida)","10 minutos","15 minutos",
                "20 minutos","30 minutos (meditação profunda)",
            ])
        with col2:
            estilo_med   = st.selectbox("Estilo de meditação:", [
                "Respiração consciente","Body scan (varredura corporal)",
                "Visualização guiada","Mantra e repetição",
                "Mindfulness (atenção plena)","Meditação transcendental (adaptada)",
            ])
            experiencia  = st.radio("Experiência com meditação:", ["Nunca meditei","Já meditei algumas vezes","Medito com frequência"], horizontal=True)

        if st.button("🧘 GERAR MEDITAÇÃO GUIADA"):
            with st.spinner("Preparando sua meditação personalizada..."):
                prompt = (
                    f"Crie um script completo de meditação guiada.\n"
                    f"Objetivo: {objetivo_med}. Tempo: {tempo_med}.\n"
                    f"Estilo: {estilo_med}. Experiência: {experiencia}.\n"
                    f"Estado emocional atual: {st.session_state.estado_emocional}.\n"
                    f"Maior bloqueio: {st.session_state.maior_bloqueio or 'não informado'}.\n\n"
                    f"FORMATO:\n\n"
                    f"🧘 MEDITAÇÃO: {objetivo_med.upper()}\n"
                    f"Duração: {tempo_med} | Estilo: {estilo_med}\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"PREPARAÇÃO (antes de começar):\n"
                    f"[Como se posicionar, ambiente ideal, o que desligar]\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"INÍCIO — ÂNCORA (2 min):\n"
                    f"[Script palavra por palavra — voz suave, pausas indicadas com '...']]\n"
                    f"[Use '(pausa de X segundos)' para indicar silêncios]\n\n"
                    f"DESENVOLVIMENTO — NÚCLEO ({tempo_med} principal):\n"
                    f"[Script completo da meditação — específico para {objetivo_med}]\n"
                    f"[Inclua respiração, visualizações ou mantras conforme o estilo]\n\n"
                    f"ENCERRAMENTO — RETORNO (2 min):\n"
                    f"[Como sair gentilmente da meditação]\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"💡 DICA PÓS-MEDITAÇÃO:\n"
                    f"[O que fazer nos 5 minutos após a meditação para fixar o estado]\n\n"
                    f"📅 FREQUÊNCIA RECOMENDADA:\n"
                    f"[Quantas vezes por semana e quando é o melhor horário]\n\n"
                    f"🌱 PRÓXIMO PASSO:\n"
                    f"[Como evoluir essa prática ao longo do tempo]"
                )
                res = mente_ia(prompt)
                salvar_sessao("Meditação", objetivo_med, res)
                st.session_state.sessoes_meditacao += 1
                st.session_state['med_temp'] = res
                st.markdown(f"<div class='card-dark'>{res}</div>", unsafe_allow_html=True)
                st.success(f"🎉 Meditação {st.session_state.sessoes_meditacao} concluída!")

        if st.session_state.get('med_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar meditação (.txt)",
                    data=st.session_state['med_temp'],
                    file_name=f"meditacao_{objetivo_med.replace(' ','_') if 'objetivo_med' in dir() else 'guiada'}.txt",
                    mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar meditação", use_container_width=True):
                    st.session_state.conteudos_salvos.append({
                        'tipo': 'Meditação', 'tema': objetivo_med if 'objetivo_med' in dir() else '',
                        'conteudo': st.session_state['med_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

    # ========================
    # REPROGRAMAÇÃO COM PNL
    # ========================
    elif st.session_state.pagina == "PNL":
        st.header("🗣️ Reprogramação com PNL")
        st.markdown("Técnicas de Programação Neurolinguística para reprogramar crenças e padrões mentais.")

        tab1, tab2, tab3 = st.tabs(["🔄 Reframing","⚓ Ancoragem","⏳ Linha do Tempo"])

        with tab1:
            st.markdown("**Reframing — mude o significado, mude a experiência**")
            col1, col2 = st.columns(2)
            with col1:
                crenca    = st.text_area("Crença ou pensamento limitante:", height=100,
                    value=st.session_state.crencas_limitantes,
                    placeholder="ex: não sou bom o suficiente, nunca consigo terminar o que começo...")
                situacao  = st.text_input("Situação onde isso aparece:",
                    placeholder="ex: quando vou apresentar algo no trabalho, quando conheço pessoas novas...")
            with col2:
                impacto   = st.text_input("Como isso impacta sua vida:",
                    placeholder="ex: me paralisa, me faz desistir, me faz procrastinar...")
                objetivo_r= st.text_input("O que você quer sentir/acreditar no lugar:",
                    placeholder="ex: confiança, leveza, certeza de que sou capaz...")

            if st.button("🔄 GERAR TÉCNICA DE REFRAMING"):
                if crenca.strip():
                    with st.spinner("Aplicando técnica de reframing..."):
                        prompt = (
                            f"Aplique a técnica de Reframing de PNL para a crença: '{crenca}'.\n"
                            f"Situação: {situacao}. Impacto: {impacto}. Objetivo: {objetivo_r}.\n\n"
                            f"ESTRUTURA:\n\n"
                            f"🔄 REFRAMING: '{crenca}'\n\n"
                            f"🔍 ANÁLISE DA CRENÇA:\n"
                            f"[De onde essa crença provavelmente veio — origem provável]\n"
                            f"[Para que ela 'serviu' no passado — intenção positiva original]\n"
                            f"[Como ela está te limitando agora]\n\n"
                            f"🔄 REFRAMING DE CONTEÚDO:\n"
                            f"[5 formas diferentes de interpretar a mesma situação — perspectivas alternativas]\n\n"
                            f"🔄 REFRAMING DE CONTEXTO:\n"
                            f"[Em que contexto essa crença seria útil ou verdadeira?]\n\n"
                            f"💬 NOVA CRENÇA PROPOSTA:\n"
                            f"[A crença reprogramada — específica, positiva e crível]\n\n"
                            f"🗣️ DIÁLOGO INTERNO REPROGRAMADO:\n"
                            f"[Como responder quando o pensamento limitante aparecer — script exato]\n\n"
                            f"🏋️ EXERCÍCIO PRÁTICO (faça agora):\n"
                            f"[Técnica de 5 minutos para começar a instalar a nova crença]\n\n"
                            f"📅 PRÁTICA DIÁRIA (21 dias):\n"
                            f"[O que fazer todos os dias para consolidar a reprogramação]"
                        )
                        res = mente_ia(prompt, "Especialista em Reframing de PNL. Seja específico e prático.")
                        salvar_sessao("PNL", f"Reframing: {crenca[:40]}", res)
                        st.session_state['reframe_temp'] = res
                        st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Descreva a crença limitante.")

            if st.session_state.get('reframe_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar técnica (.txt)", data=st.session_state['reframe_temp'],
                        file_name="reframing_pnl.txt", mime="text/plain", use_container_width=True)
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_ref", use_container_width=True):
                        st.session_state.conteudos_salvos.append({
                            'tipo': 'PNL — Reframing', 'tema': crenca[:40] if 'crenca' in dir() else '',
                            'conteudo': st.session_state['reframe_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        with tab2:
            st.markdown("**Ancoragem — crie um gatilho físico para estados emocionais poderosos**")
            col1, col2 = st.columns(2)
            with col1:
                estado_anc = st.selectbox("Estado emocional que quer ancorar:", [
                    "Confiança máxima","Foco total","Calma profunda","Motivação intensa",
                    "Alegria e leveza","Coragem","Clareza mental","Amor próprio",
                ])
                ancora_fis = st.selectbox("Âncora física (gatilho):", [
                    "Apertar o polegar e indicador","Tocar o pulso","Fazer um punho",
                    "Tocar o ombro","Pressionar dois dedos na palma","Criar sua própria",
                ])
            with col2:
                momento    = st.text_area("Descreva um momento em que você sentiu esse estado intensamente:", height=100,
                    placeholder="ex: o dia que apresentei meu projeto e fui muito elogiado, quando ganhei a competição...")

            if st.button("⚓ CRIAR PROTOCOLO DE ANCORAGEM"):
                if momento.strip():
                    with st.spinner("Criando sua âncora..."):
                        prompt = (
                            f"Crie um protocolo completo de Ancoragem de PNL.\n"
                            f"Estado a ancorar: {estado_anc}. Âncora física: {ancora_fis}.\n"
                            f"Memória de referência: {momento}.\n\n"
                            f"ESTRUTURA:\n\n"
                            f"⚓ ANCORAGEM: {estado_anc.upper()}\n"
                            f"Âncora física: {ancora_fis}\n\n"
                            f"🧠 COMO FUNCIONA:\n"
                            f"[Explicação simples da neurociência por trás da ancoragem]\n\n"
                            f"📋 PROTOCOLO PASSO A PASSO:\n\n"
                            f"ETAPA 1 — PREPARAÇÃO (2 min):\n[O que fazer antes de começar]\n\n"
                            f"ETAPA 2 — ACESSAR O ESTADO (5 min):\n"
                            f"[Como reviver intensamente a memória de {momento[:30]}...]\n"
                            f"[Script de visualização para intensificar o estado]\n\n"
                            f"ETAPA 3 — INSTALAR A ÂNCORA (no pico):\n"
                            f"[Exatamente quando e como aplicar {ancora_fis}]\n"
                            f"[Como calibrar o timing perfeito]\n\n"
                            f"ETAPA 4 — TESTAR A ÂNCORA:\n"
                            f"[Como verificar se a ancoragem funcionou]\n\n"
                            f"ETAPA 5 — REFORÇAR (próximos 7 dias):\n"
                            f"[Como fortalecer a âncora com repetição]\n\n"
                            f"⚡ COMO USAR NO DIA A DIA:\n"
                            f"[Quando e como disparar a âncora para máximo resultado]\n\n"
                            f"🔧 SE NÃO FUNCIONAR:\n"
                            f"[Ajustes e alternativas]"
                        )
                        res = mente_ia(prompt)
                        salvar_sessao("PNL", f"Ancoragem: {estado_anc}", res)
                        st.session_state['ancora_temp'] = res
                        st.markdown(f"<div class='card-purple'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Descreva o momento de referência.")

            if st.session_state.get('ancora_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar protocolo (.txt)", data=st.session_state['ancora_temp'],
                        file_name="ancoragem_pnl.txt", mime="text/plain", use_container_width=True)
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_anc", use_container_width=True):
                        st.session_state.conteudos_salvos.append({
                            'tipo': 'PNL — Ancoragem', 'tema': estado_anc if 'estado_anc' in dir() else '',
                            'conteudo': st.session_state['ancora_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        with tab3:
            st.markdown("**Linha do Tempo — ressignifique o passado e programe o futuro**")
            col1, col2 = st.columns(2)
            with col1:
                evento_lt  = st.text_area("Evento do passado que ainda te afeta:", height=80,
                    placeholder="ex: rejeição na escola, fracasso num negócio, crítica que me machucou...")
                emocao_lt  = st.text_input("Emoção que você sente ao lembrar:",
                    placeholder="ex: vergonha, medo, raiva, tristeza...")
            with col2:
                futuro_lt  = st.text_area("Que futuro você quer programar:", height=80,
                    placeholder="ex: me ver em 1 ano confiante, bem-sucedido, em paz comigo mesmo...")
                obj_lt     = st.text_input("Qual mudança você quer nessa emoção:",
                    placeholder="ex: transformar vergonha em aprendizado, medo em coragem...")

            if st.button("⏳ GERAR TÉCNICA DE LINHA DO TEMPO"):
                if evento_lt.strip():
                    with st.spinner("Preparando técnica de linha do tempo..."):
                        prompt = (
                            f"Crie uma técnica de Linha do Tempo de PNL.\n"
                            f"Evento: {evento_lt}. Emoção atual: {emocao_lt}.\n"
                            f"Futuro desejado: {futuro_lt}. Mudança buscada: {obj_lt}.\n\n"
                            f"ESTRUTURA:\n\n"
                            f"⏳ LINHA DO TEMPO — RESSIGNIFICAÇÃO\n\n"
                            f"🧠 ENTENDENDO A TÉCNICA:\n"
                            f"[Como a mente armazena memórias e como podemos ressignificá-las]\n\n"
                            f"PARTE 1 — RESSIGNIFICANDO O PASSADO:\n\n"
                            f"Passo 1 — Dissociação: [como observar o evento de fora, sem reviver]\n"
                            f"Passo 2 — Nova perspectiva: [como o {st.session_state.usuario} de hoje veria esse evento]\n"
                            f"Passo 3 — Recurso: [qual recurso você tinha mas não percebia naquele momento]\n"
                            f"Passo 4 — Mensagem: [o que aprender e extrair de positivo]\n"
                            f"Passo 5 — Integração: [como guardar essa nova versão da memória]\n\n"
                            f"PARTE 2 — PROGRAMANDO O FUTURO:\n\n"
                            f"[Script de visualização do futuro desejado — vívido e sensorial]\n"
                            f"[Como 'instalar' esse futuro na sua linha do tempo mental]\n\n"
                            f"🏋️ EXERCÍCIO COMPLETO (30 min):\n"
                            f"[Protocolo passo a passo para fazer essa sessão sozinho]\n\n"
                            f"⚠️ IMPORTANTE:\n"
                            f"[Cuidados — quando buscar apoio profissional]"
                        )
                        res = mente_ia(prompt)
                        salvar_sessao("PNL", f"Linha do Tempo: {evento_lt[:40]}", res)
                        st.session_state['lt_temp'] = res
                        st.markdown(f"<div class='card-blue'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Descreva o evento que quer ressignificar.")

            if st.session_state.get('lt_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar técnica (.txt)", data=st.session_state['lt_temp'],
                        file_name="linha_do_tempo_pnl.txt", mime="text/plain", use_container_width=True)
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_lt", use_container_width=True):
                        st.session_state.conteudos_salvos.append({
                            'tipo': 'PNL — Linha do Tempo', 'tema': evento_lt[:40] if 'evento_lt' in dir() else '',
                            'conteudo': st.session_state['lt_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

    # ========================
    # AFIRMAÇÕES PERSONALIZADAS
    # ========================
    elif st.session_state.pagina == "Afirmacoes":
        st.header("💬 Afirmações Personalizadas")
        st.markdown("Afirmações criadas para o SEU problema real — não as genéricas que todo mundo usa.")

        col1, col2 = st.columns(2)
        with col1:
            area_af    = st.selectbox("Área da vida:", [
                "Autoestima e amor próprio","Confiança e coragem","Prosperidade e abundância",
                "Relacionamentos e amor","Saúde e corpo","Carreira e sucesso",
                "Paz interior e equilíbrio","Foco e produtividade",
            ])
            problema_af= st.text_area("Descreva seu problema ou bloqueio real:", height=100,
                value=st.session_state.maior_bloqueio,
                placeholder="ex: me sinto inferior às outras pessoas, tenho medo de ser julgado...")
        with col2:
            qtd_af     = st.slider("Quantidade de afirmações:", 5, 20, 10)
            formato_af = st.radio("Formato:", ["Afirmações no presente","Afirmações em 'Eu sou'","Perguntas afirmativas (por que sou?)"], horizontal=True)
            uso_af     = st.selectbox("Quando vai usar:", [
                "Ao acordar (manhã)","Antes de dormir (noite)","Durante o dia (várias vezes)",
                "Em momentos de crise","Antes de situações desafiadoras",
            ])

        if st.button("💬 GERAR MINHAS AFIRMAÇÕES"):
            if problema_af.strip():
                with st.spinner("Criando suas afirmações personalizadas..."):
                    prompt = (
                        f"Crie {qtd_af} afirmações personalizadas para {st.session_state.usuario}.\n"
                        f"Área: {area_af}. Problema real: {problema_af}.\n"
                        f"Formato: {formato_af}. Uso: {uso_af}.\n\n"
                        f"REGRAS OBRIGATÓRIAS:\n"
                        f"- NUNCA use afirmações genéricas como 'Eu sou feliz' ou 'Eu mereço o melhor'\n"
                        f"- Cada afirmação deve responder diretamente ao problema '{problema_af}'\n"
                        f"- Use linguagem específica, pessoal e crível — a pessoa deve conseguir acreditar\n"
                        f"- Progresso gradual: começa mais suave e vai ficando mais forte\n\n"
                        f"FORMATO:\n\n"
                        f"💬 SUAS AFIRMAÇÕES — {area_af.upper()}\n"
                        f"Criadas especificamente para: {problema_af[:50]}...\n\n"
                        f"[Liste as {qtd_af} afirmações numeradas]\n\n"
                        f"📋 PROTOCOLO DE USO ({uso_af}):\n"
                        f"[Como usar essas afirmações especificamente nesse horário]\n"
                        f"[Quantas vezes repetir, em qual tom, com qual emoção]\n\n"
                        f"🧠 POR QUE ESSE FORMATO FUNCIONA:\n"
                        f"[Neurociência por trás da repetição afirmativa — simples e claro]\n\n"
                        f"⚠️ ERROS COMUNS:\n"
                        f"[O que a maioria faz errado com afirmações e como evitar]\n\n"
                        f"📈 COMO SABER SE ESTÁ FUNCIONANDO:\n"
                        f"[Sinais de que as afirmações estão reprogramando o subconsciente]"
                    )
                    res = mente_ia(prompt)
                    salvar_sessao("Afirmações", area_af, res)
                    st.session_state['afirm_temp'] = res
                    st.markdown(f"<div class='card-green'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Descreva seu bloqueio ou problema real.")

        if st.session_state.get('afirm_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar afirmações (.txt)", data=st.session_state['afirm_temp'],
                    file_name="afirmacoes_personalizadas.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_afirm", use_container_width=True):
                    st.session_state.conteudos_salvos.append({
                        'tipo': 'Afirmações', 'tema': area_af if 'area_af' in dir() else '',
                        'conteudo': st.session_state['afirm_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

    # ========================
    # PROTOCOLO DO SONO
    # ========================
    elif st.session_state.pagina == "Sono":
        st.header("😴 Protocolo do Sono")
        st.markdown("Rotina noturna completa para dormir bem e acordar descansado todos os dias.")

        col1, col2 = st.columns(2)
        with col1:
            problema_sono = st.multiselect("Seus problemas com o sono:", [
                "Demoro para pegar no sono","Acordo no meio da noite","Durmo mas não descanso",
                "Pensamentos acelerados na hora de dormir","Pesadelos frequentes",
                "Acordar muito cedo","Ansiedade noturna","Uso de celular até tarde",
            ], default=["Demoro para pegar no sono"])
            horario_deitar = st.selectbox("Horário que quer dormir:", ["21h","22h","22h30","23h","23h30","0h"])
        with col2:
            horario_acordar = st.selectbox("Horário que precisa acordar:", ["5h","5h30","6h","6h30","7h","7h30","8h"])
            ambiente_sono   = st.text_input("Seu ambiente de quarto:", placeholder="ex: barulhento, muito claro, quente, compartilhado...")
            rotina_atual_sono = st.text_input("O que você faz antes de dormir hoje:", placeholder="ex: fico no celular, assisto série, trabalho até tarde...")

        if st.button("😴 GERAR MEU PROTOCOLO DO SONO"):
            with st.spinner("Criando seu protocolo de sono..."):
                problemas = ", ".join(problema_sono) if problema_sono else "dificuldade geral para dormir"
                prompt = (
                    f"Crie um protocolo completo para melhorar o sono.\n"
                    f"Problemas: {problemas}.\n"
                    f"Quer dormir às: {horario_deitar}. Acorda às: {horario_acordar}.\n"
                    f"Ambiente: {ambiente_sono or 'não informado'}.\n"
                    f"Rotina atual: {rotina_atual_sono or 'não informada'}.\n\n"
                    f"ESTRUTURA:\n\n"
                    f"😴 PROTOCOLO DO SONO PERSONALIZADO\n"
                    f"Meta: dormir às {horario_deitar} e acordar às {horario_acordar} descansado\n\n"
                    f"🧠 POR QUE VOCÊ NÃO DORME BEM:\n"
                    f"[Análise honesta dos problemas '{problemas}' e suas causas]\n\n"
                    f"🌅 ROTINA MATINAL (para dormir bem à noite):\n"
                    f"[O que fazer de manhã impacta o sono — ações específicas]\n\n"
                    f"🌙 ROTINA NOTURNA — {horario_deitar} MENOS 2 HORAS:\n"
                    f"[Cronograma hora a hora até a hora de dormir]\n\n"
                    f"🛏️ RITUAL DOS 10 MINUTOS ANTES DE DORMIR:\n"
                    f"[Sequência exata de ações para preparar o cérebro para o sono]\n\n"
                    f"🧘 TÉCNICA DE RELAXAMENTO PARA DORMIR:\n"
                    f"[Script de respiração ou body scan para usar na cama]\n\n"
                    f"😰 SE VOCÊ ACORDAR NO MEIO DA NOITE:\n"
                    f"[Protocolo específico para cada problema listado]\n\n"
                    f"📵 HIGIENE DIGITAL:\n"
                    f"[Regras específicas para o uso do celular e telas]\n\n"
                    f"🛏️ OTIMIZAÇÃO DO AMBIENTE:\n"
                    f"[Como melhorar o quarto para o sono — específico para '{ambiente_sono}']\n\n"
                    f"📅 RESULTADO ESPERADO:\n"
                    f"[O que muda em 7, 14 e 30 dias seguindo esse protocolo]"
                )
                res = mente_ia(prompt)
                salvar_sessao("Sono", f"Protocolo: {horario_deitar}-{horario_acordar}", res)
                st.session_state['sono_temp'] = res
                st.markdown(f"<div class='card-blue'>{res}</div>", unsafe_allow_html=True)

        if st.session_state.get('sono_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar protocolo (.txt)", data=st.session_state['sono_temp'],
                    file_name="protocolo_sono.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_sono", use_container_width=True):
                    st.session_state.conteudos_salvos.append({
                        'tipo': 'Protocolo do Sono', 'tema': f"{horario_deitar}-{horario_acordar}" if 'horario_deitar' in dir() else '',
                        'conteudo': st.session_state['sono_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

    # ========================
    # GESTÃO DE ANSIEDADE
    # ========================
    elif st.session_state.pagina == "Ansiedade":
        st.header("😰 Gestão de Ansiedade")
        st.markdown("Técnicas de respiração, grounding e protocolos para momentos de crise.")

        st.markdown("""<div style="background:#FFF1F2;border:1px solid #FDA4AF;border-radius:10px;
        padding:10px 14px;margin-bottom:16px;font-size:0.85em;color:#1A1A2E;">
        ⚠️ <strong>Importante:</strong> Este conteúdo é para bem-estar geral. Em casos de ansiedade severa,
        transtorno de pânico ou crises frequentes, procure um psicólogo ou psiquiatra.
        </div>""", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🌬️ Técnicas de Respiração","🌍 Grounding e Protocolo de Crise"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                nivel_ans = st.select_slider("Nível de ansiedade agora:", options=[
                    "Leve (1-3)","Moderada (4-6)","Intensa (7-8)","Muito intensa (9-10)"
                ])
                tipo_resp = st.selectbox("Técnica de respiração:", [
                    "Respiração 4-7-8 (para dormir e acalmar)","Respiração diafragmática (base)",
                    "Respiração quadrada (box breathing)","Respiração coerente (5-5)",
                    "Respiração alternada (ioga)","Técnica mais indicada para meu caso",
                ])
            with col2:
                contexto_ans = st.text_input("Em que situação costuma sentir ansiedade:",
                    placeholder="ex: antes de reuniões, em locais cheios, ao receber críticas...")
                duracao_resp = st.selectbox("Tempo disponível:", ["2 minutos","5 minutos","10 minutos","15 minutos"])

            if st.button("🌬️ GERAR PROTOCOLO DE RESPIRAÇÃO"):
                with st.spinner("Criando seu protocolo de respiração..."):
                    prompt = (
                        f"Crie um protocolo completo de respiração para ansiedade.\n"
                        f"Nível atual: {nivel_ans}. Técnica: {tipo_resp}.\n"
                        f"Contexto de ansiedade: {contexto_ans}. Tempo: {duracao_resp}.\n\n"
                        f"ESTRUTURA:\n\n"
                        f"🌬️ PROTOCOLO DE RESPIRAÇÃO\n"
                        f"Técnica: {tipo_resp} | Para: {nivel_ans}\n\n"
                        f"🧠 COMO ESSA TÉCNICA FUNCIONA NO CÉREBRO:\n"
                        f"[Neurociência simples — como a respiração acalma o sistema nervoso]\n\n"
                        f"📋 PROTOCOLO PASSO A PASSO:\n\n"
                        f"ANTES DE COMEÇAR:\n[Posição, olhos, onde fazer]\n\n"
                        f"A TÉCNICA (com timer):\n"
                        f"[Instruções detalhadas — inspire por X, segure por X, expire por X]\n"
                        f"[Quantas rodadas fazer em {duracao_resp}]\n"
                        f"[O que visualizar ou focar durante]\n\n"
                        f"APÓS A TÉCNICA:\n[O que fazer nos 2 minutos seguintes]\n\n"
                        f"⚡ VERSÃO DE EMERGÊNCIA (30 segundos):\n"
                        f"[Para quando a ansiedade pega de surpresa no contexto '{contexto_ans}']\n\n"
                        f"📅 PRÁTICA PREVENTIVA:\n"
                        f"[Como usar essa técnica antes que a ansiedade apareça]"
                    )
                    res = mente_ia(prompt)
                    salvar_sessao("Ansiedade", f"Respiração: {tipo_resp[:30]}", res)
                    st.session_state['resp_temp'] = res
                    st.markdown(f"<div class='card-teal'>{res}</div>", unsafe_allow_html=True)

            if st.session_state.get('resp_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar protocolo (.txt)", data=st.session_state['resp_temp'],
                        file_name="respiracao_ansiedade.txt", mime="text/plain", use_container_width=True)
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_resp", use_container_width=True):
                        st.session_state.conteudos_salvos.append({
                            'tipo': 'Respiração', 'tema': tipo_resp[:40] if 'tipo_resp' in dir() else '',
                            'conteudo': st.session_state['resp_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                tipo_crise = st.selectbox("Tipo de crise mais frequente:", [
                    "Ansiedade generalizada","Ataque de pânico","Overthinking (pensamentos acelerados)",
                    "Crise de choro","Paralisia por medo","Dissociação (se sentir fora do corpo)",
                ])
                gatilho    = st.text_input("Principal gatilho:", placeholder="ex: conflito com alguém, notícias ruins, solidão...")
            with col2:
                suporte    = st.text_input("O que já ajudou você antes:", placeholder="ex: música, ligar para alguém, caminhar...")

            if st.button("🌍 GERAR PROTOCOLO DE CRISE"):
                with st.spinner("Criando seu protocolo de emergência..."):
                    prompt = (
                        f"Crie um protocolo de grounding e gestão de crise.\n"
                        f"Tipo de crise: {tipo_crise}. Gatilho: {gatilho}.\n"
                        f"O que já ajudou: {suporte or 'não informado'}.\n\n"
                        f"ESTRUTURA:\n\n"
                        f"🌍 PROTOCOLO DE EMERGÊNCIA — {tipo_crise.upper()}\n\n"
                        f"⚡ TÉCNICA DOS 5-4-3-2-1 (GROUNDING IMEDIATO):\n"
                        f"[Adaptada especificamente para {tipo_crise}]\n"
                        f"5 coisas que você VÊ: [exemplos contextualizados]\n"
                        f"4 coisas que você pode TOCAR: [exemplos]\n"
                        f"3 coisas que você OUVE: [exemplos]\n"
                        f"2 coisas que você CHEIRA: [exemplos]\n"
                        f"1 coisa que você SENTE no paladar: [exemplos]\n\n"
                        f"🚨 PROTOCOLO DOS PRIMEIROS 10 MINUTOS DE CRISE:\n"
                        f"Minuto 1-2: [ação imediata]\n"
                        f"Minuto 3-5: [técnica de respiração específica]\n"
                        f"Minuto 6-10: [grounding e ancoragem]\n\n"
                        f"💬 O QUE DIZER PARA SI MESMO (diálogo interno de crise):\n"
                        f"[Frases específicas para {tipo_crise} — que realmente acalmam]\n\n"
                        f"📲 PLANO DE AÇÃO PÓS-CRISE:\n"
                        f"[O que fazer nas horas seguintes para se recuperar]\n\n"
                        f"🛡️ PREVENÇÃO — IDENTIFICAR O GATILHO '{gatilho}':\n"
                        f"[Como perceber que a crise está chegando antes de começar]\n\n"
                        f"📞 QUANDO BUSCAR AJUDA PROFISSIONAL:\n"
                        f"[Sinais claros de que precisa de apoio especializado]"
                    )
                    res = mente_ia(prompt)
                    salvar_sessao("Ansiedade", f"Protocolo de crise: {tipo_crise}", res)
                    st.session_state['crise_temp'] = res
                    st.markdown(f"<div class='card-orange'>{res}</div>", unsafe_allow_html=True)

            if st.session_state.get('crise_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar protocolo (.txt)", data=st.session_state['crise_temp'],
                        file_name="protocolo_crise.txt", mime="text/plain", use_container_width=True)
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_crise", use_container_width=True):
                        st.session_state.conteudos_salvos.append({
                            'tipo': 'Protocolo de Crise', 'tema': tipo_crise if 'tipo_crise' in dir() else '',
                            'conteudo': st.session_state['crise_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

    # ========================
    # VISUALIZAÇÃO CRIATIVA
    # ========================
    elif st.session_state.pagina == "Visualizacao":
        st.header("🎯 Visualização Criativa")
        st.markdown("Scripts de visualização do futuro que você quer construir — vívido, sensorial e poderoso.")

        col1, col2 = st.columns(2)
        with col1:
            futuro_vis = st.text_area("Descreva o futuro que você quer visualizar:", height=120,
                value=st.session_state.objetivo_mental,
                placeholder="ex: me ver daqui 1 ano com meu negócio funcionando, em paz, com saúde, amado...")
            area_vis   = st.selectbox("Área principal da visualização:", [
                "Vida profissional e financeira","Saúde e corpo","Relacionamentos e amor",
                "Paz interior e felicidade","Conquista de um objetivo específico","Vida completa e integrada",
            ])
        with col2:
            tempo_vis  = st.selectbox("Horizonte de tempo:", ["3 meses","6 meses","1 ano","3 anos","5 anos","10 anos"])
            duracao_vis= st.selectbox("Duração da sessão:", ["5 minutos","10 minutos","15 minutos","20 minutos"])
            intensidade= st.radio("Intensidade:", ["Suave e tranquila","Intensa e motivadora","Profunda e transformadora"], horizontal=True)

        if st.button("🎯 GERAR VISUALIZAÇÃO CRIATIVA"):
            if futuro_vis.strip():
                with st.spinner("Criando sua visualização..."):
                    prompt = (
                        f"Crie um script de visualização criativa completo.\n"
                        f"Futuro desejado: {futuro_vis}.\n"
                        f"Área: {area_vis}. Horizonte: {tempo_vis}.\n"
                        f"Duração: {duracao_vis}. Intensidade: {intensidade}.\n"
                        f"Nome do usuário: {st.session_state.usuario}.\n\n"
                        f"ESTRUTURA:\n\n"
                        f"🎯 VISUALIZAÇÃO: {area_vis.upper()}\n"
                        f"Horizonte: {tempo_vis} | Duração: {duracao_vis}\n\n"
                        f"🧠 COMO A VISUALIZAÇÃO REPROGRAMA O CÉREBRO:\n"
                        f"[Neurociência — por que o cérebro não distingue o vivido do imaginado intensamente]\n\n"
                        f"PREPARAÇÃO (2 min):\n"
                        f"[Como se preparar — respiração, posição, intenção]\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━━\n"
                        f"SCRIPT DA VISUALIZAÇÃO:\n"
                        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"[Script completo em 1ª pessoa, no presente, ultra-detalhado]\n"
                        f"[Use todos os sentidos: o que VÊ, OUVE, SENTE no corpo, CHEIRA, SABOREIA]\n"
                        f"[Inclua: onde você está, como está vestido, quem está ao seu lado]\n"
                        f"[Como você se sente por dentro — emoções específicas]\n"
                        f"[O que as pessoas dizem para você, como elas te veem]\n"
                        f"[Um momento específico de conquista no seu futuro de {tempo_vis}]\n"
                        f"[Intensidade: {intensidade}]\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"ANCORAGEM DA VISUALIZAÇÃO:\n"
                        f"[Como guardar essa imagem e emoção no corpo]\n\n"
                        f"📅 PRÁTICA:\n"
                        f"[Frequência ideal e como usar no dia a dia para máximo resultado]\n\n"
                        f"📝 DIÁRIO DA VISUALIZAÇÃO:\n"
                        f"[O que anotar após cada sessão para acelerar a manifestação]"
                    )
                    res = mente_ia(prompt, "Especialista em visualização criativa e lei da atração. Crie um script cinematográfico, vívido e emocionante.")
                    salvar_sessao("Visualização", area_vis, res)
                    st.session_state['vis_temp'] = res
                    st.markdown(f"<div class='card-dark'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Descreva o futuro que você quer visualizar.")

        if st.session_state.get('vis_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar visualização (.txt)", data=st.session_state['vis_temp'],
                    file_name="visualizacao_criativa.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_vis", use_container_width=True):
                    st.session_state.conteudos_salvos.append({
                        'tipo': 'Visualização', 'tema': area_vis if 'area_vis' in dir() else '',
                        'conteudo': st.session_state['vis_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

    # ========================
    # DIÁRIO MENTAL
    # ========================
    elif st.session_state.pagina == "Diario":
        st.header("📖 Diário Mental")
        st.markdown("Reflexões guiadas para autoconhecimento profundo — com prompts personalizados pela IA.")

        tab1, tab2 = st.tabs(["✍️ Escrever Hoje","📚 Entradas Anteriores"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                tipo_diario = st.selectbox("Tipo de reflexão de hoje:", [
                    "Reflexão do dia (como foi meu dia)","Gratidão profunda","Autoconhecimento",
                    "Processamento emocional","Planejamento do eu futuro",
                    "Perdão e cura","Crenças e padrões","Livre (IA escolhe pelo meu perfil)",
                ])
                estado_hoje = st.select_slider("Como você está agora:", options=[
                    "Muito mal 😔","Mal 😟","Neutro 😐","Bem 🙂","Muito bem 😁"
                ])
            with col2:
                evento_hoje = st.text_area("O que aconteceu de significativo hoje:", height=80,
                    placeholder="ex: tive uma briga, recebi uma notícia boa, me senti inseguro em algo...")

            if st.button("📖 GERAR PROMPTS DO DIÁRIO"):
                with st.spinner("Criando seus prompts personalizados..."):
                    prompt = (
                        f"Crie prompts de diário mental personalizados.\n"
                        f"Tipo: {tipo_diario}. Estado: {estado_hoje}.\n"
                        f"Evento do dia: {evento_hoje or 'não informado'}.\n"
                        f"Maior bloqueio: {st.session_state.maior_bloqueio or 'não informado'}.\n\n"
                        f"ESTRUTURA:\n\n"
                        f"📖 DIÁRIO MENTAL — {tipo_diario.upper()}\n"
                        f"Data: {datetime.now().strftime('%d/%m/%Y')} | Estado: {estado_hoje}\n\n"
                        f"✍️ SEUS PROMPTS DE HOJE (responda com calma, sem julgamento):\n\n"
                        f"[Crie 7-10 prompts profundos e específicos para {tipo_diario}]\n"
                        f"[Cada prompt deve ser uma pergunta aberta que leva à introspecção]\n"
                        f"[Adapte ao estado '{estado_hoje}' e ao evento '{evento_hoje}']\n"
                        f"[Progressão: do mais fácil ao mais profundo]\n\n"
                        f"💡 DICA DE ESCRITA:\n"
                        f"[Como escrever sem censura — técnica do fluxo de consciência]\n\n"
                        f"🌱 INSIGHT PARA FECHAR:\n"
                        f"[Uma reflexão ou perspectiva para encerrar a sessão do diário]\n\n"
                        f"⏰ TEMPO SUGERIDO: [quanto tempo dedicar a esse diário hoje]"
                    )
                    res = mente_ia(prompt)
                    st.session_state['diario_prompts'] = res
                    st.markdown(f"<div class='card-pink'>{res}</div>", unsafe_allow_html=True)

            if st.session_state.get('diario_prompts'):
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### ✍️ Escreva aqui sua reflexão:")
                reflexao = st.text_area("Sua reflexão de hoje:", height=200,
                    placeholder="Escreva livremente, sem julgamento. Isso é só seu...")

                col_sv, col_dl = st.columns(2)
                with col_sv:
                    if st.button("💾 Salvar entrada no diário", use_container_width=True):
                        if reflexao.strip():
                            st.session_state.diario_entradas.append({
                                'data':     datetime.now().strftime('%d/%m/%Y %H:%M'),
                                'tipo':     tipo_diario if 'tipo_diario' in dir() else '',
                                'estado':   estado_hoje if 'estado_hoje' in dir() else '',
                                'prompts':  st.session_state.get('diario_prompts', ''),
                                'reflexao': reflexao,
                            })
                            salvar_sessao("Diário", tipo_diario if 'tipo_diario' in dir() else 'Reflexão', reflexao[:60])
                            st.success("📖 Entrada salva no seu diário!")
                            st.rerun()
                        else:
                            st.warning("Escreva sua reflexão antes de salvar.")
                with col_dl:
                    if reflexao.strip():
                        entrada_txt = f"DIÁRIO MENTAL — {datetime.now().strftime('%d/%m/%Y')}\n\nPROMPTS:\n{st.session_state.get('diario_prompts','')}\n\nMINHA REFLEXÃO:\n{reflexao}"
                        st.download_button("📋 Baixar entrada (.txt)", data=entrada_txt,
                            file_name=f"diario_{datetime.now().strftime('%d%m%Y')}.txt",
                            mime="text/plain", use_container_width=True)

        with tab2:
            if not st.session_state.diario_entradas:
                st.info("Nenhuma entrada no diário ainda. Comece escrevendo sua primeira reflexão!")
            else:
                st.markdown(f"**{len(st.session_state.diario_entradas)} entrada(s) no seu diário**")
                for i, entrada in enumerate(reversed(st.session_state.diario_entradas)):
                    idx_real = len(st.session_state.diario_entradas) - 1 - i
                    with st.expander(f"📖 {entrada['data']} — {entrada['tipo']} — {entrada['estado']}"):
                        st.markdown("**Prompts:**")
                        st.markdown(f"<div class='card-pink' style='font-size:0.85em;'>{entrada['prompts'][:500]}...</div>", unsafe_allow_html=True)
                        st.markdown("**Sua reflexão:**")
                        st.markdown(f"<div class='card'>{entrada['reflexao']}</div>", unsafe_allow_html=True)
                        if st.button("🗑️ Remover", key=f"del_diario_{i}"):
                            st.session_state.diario_entradas.pop(idx_real)
                            st.rerun()

    # ========================
    # SALVOS E PROGRESSO
    # ========================
    elif st.session_state.pagina == "Salvos":
        st.header("❤️ Conteúdos Salvos e Progresso")

        # MÉTRICAS
        total      = len(st.session_state.historico_sessoes)
        salvos     = len(st.session_state.conteudos_salvos)
        meditacoes = st.session_state.sessoes_meditacao
        diario     = len(st.session_state.diario_entradas)
        tipos = {}
        for s in st.session_state.historico_sessoes:
            tipos[s['tipo']] = tipos.get(s['tipo'], 0) + 1

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Sessões realizadas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{meditacoes}</div><div>Meditações 🧘</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{diario}</div><div>Entradas no diário</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{salvos}</div><div>Conteúdos salvos</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('PNL',0)}</div><div>Sessões de PNL</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # CONTEÚDOS SALVOS
        if st.session_state.conteudos_salvos:
            st.markdown("### ❤️ Seus Conteúdos Favoritos")
            tipos_s = list(set(c['tipo'] for c in st.session_state.conteudos_salvos))
            filtro  = st.selectbox("Filtrar por tipo:", ["Todos"] + tipos_s)

            conts_f = [
                c for c in st.session_state.conteudos_salvos
                if filtro == "Todos" or c['tipo'] == filtro
            ]

            for i, item in enumerate(reversed(conts_f)):
                idx_real = len(st.session_state.conteudos_salvos) - 1 - i
                with st.expander(f"❤️ [{item['tipo']}] {item['tema']} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'],
                            file_name=f"{item['tipo'].lower().replace(' ','_')}.txt",
                            mime="text/plain", key=f"dl_salvo_{i}")
                    with col_del:
                        if st.button("🗑️", key=f"del_salvo_{i}"):
                            st.session_state.conteudos_salvos.pop(idx_real)
                            st.rerun()
        else:
            st.info("Nenhum conteúdo salvo ainda. Realize sessões e salve os que mais te tocarem.")

        # HISTÓRICO COMPLETO
        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.historico_sessoes:
            st.markdown("### 📊 Histórico Completo")
            col_f, col_ex = st.columns([3, 1])
            with col_f:
                filtro_h = st.selectbox("Filtrar histórico:", ["Todos"] + list(tipos.keys()), key="filtro_hist")
            with col_ex:
                st.markdown("<br>", unsafe_allow_html=True)
                hist_txt = "\n\n".join(
                    f"[{s['data']}] {s['tipo']} — {s['tema']}\n{s['conteudo']}\n{'─'*40}"
                    for s in st.session_state.historico_sessoes
                )
                st.download_button("⬇️ Exportar TXT", data=hist_txt,
                    file_name="historico_mente_poderosa.txt", mime="text/plain")

            for i, item in enumerate(reversed(st.session_state.historico_sessoes)):
                if filtro_h != "Todos" and item['tipo'] != filtro_h:
                    continue
                idx_real = len(st.session_state.historico_sessoes) - 1 - i
                with st.expander(f"[{item['tipo']}] {item['tema']} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_sv, col_del = st.columns([3, 1])
                    with col_sv:
                        if st.button("❤️ Salvar", key=f"sv_hist_{i}"):
                            st.session_state.conteudos_salvos.append(item.copy())
                            st.success("Salvo!")
                    with col_del:
                        if st.button("🗑️", key=f"del_hist_{i}"):
                            st.session_state.historico_sessoes.pop(idx_real)
                            st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Limpar Todo o Histórico"):
                st.session_state.historico_sessoes = []
                st.rerun()

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Mente Poderosa — Neurolinguística, Meditação e Reprogramação Mental com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
