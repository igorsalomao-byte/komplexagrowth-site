# -*- coding: utf-8 -*-
"""Gera o site da Komplexa Growth (HTML estático para GitHub Pages).

Uso, na raiz do site:   python _build/build.py
Pastas e arquivos que começam com "_" não são publicados pelo GitHub Pages.

- STAGING = True  -> noindex em todas as páginas, robots.txt bloqueando tudo e sem CNAME
                     (revisão em igorsalomao-byte.github.io/komplexagrowth-site/).
- STAGING = False -> versão de produção em komplexagrowth.com (index, CNAME, sitemap aberto).
- CASES: preencher com números reais. Campo com None aparece marcado como "a preencher".
"""
import io, os, json, html

STAGING = True
SITE = 'https://komplexagrowth.com'
FORM = 'https://komplexa-pricing.vercel.app/f/komplexagrowth'
WHATS = '5512987084407'
WHATS_TXT = 'Olá! Vim pelo site da Komplexa Growth e quero conversar sobre o marketing e o comercial da minha empresa.'
EMAIL = 'contato@komplexagrowth.com'
TEL = '(12) 98708-4407'
INSTA = 'https://www.instagram.com/komplexagrowth/'
FACE = 'https://www.facebook.com/komplexagrowth'
HOTEIS = 'https://komplexahoteis.com/'
CNPJ = '63.097.480/0001-70'
ENDERECO = 'Rua dos Piquiroes, 40, Sala 312, Parque Residencial Aquarius, São José dos Campos, SP, CEP 12.246-020'
HOJE = '2026-10-01'

# Cases Growth. Troque cada None pelo dado real (texto curto). Exemplo:
#   'segmento': 'Clínica de saúde', 'numero': '3,2x', 'resultado': 'em agendamentos vindos de anúncio', 'periodo': '4 meses de projeto'
CASES = [
    {'nome': 'Daga Agrinavi', 'segmento': None, 'numero': None, 'resultado': None, 'periodo': None},
    {'nome': 'Preservar Portas', 'segmento': None, 'numero': None, 'resultado': None, 'periodo': None},
    {'nome': 'Clínica Vasconcelos', 'segmento': None, 'numero': None, 'resultado': None, 'periodo': None},
    {'nome': 'Pleno Saber', 'segmento': None, 'numero': None, 'resultado': None, 'periodo': None},
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = lambda s: html.escape(s, quote=False)
A = lambda s: html.escape(s, quote=True)


def cta(pos):
    return f'{FORM}?utm_source=komplexagrowth&amp;utm_medium=site&amp;utm_content={pos}'


def whats():
    from urllib.parse import quote
    return f'https://wa.me/{WHATS}?text={quote(WHATS_TXT)}'


SETA = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'

LOGO_PATHS = [
    'M45.8247 36.6514C47.5271 36.6514 49.1676 37.1817 50.5604 38.211L89.22 66.5651C90.9533 67.844 92.0985 69.7156 92.439 71.8679C92.7795 74.0202 92.2533 76.1413 90.9843 77.8881C89.4366 80.0092 87.0842 81.2257 84.4533 81.2257C81.8223 81.2257 81.1104 80.6954 79.7176 79.6661L41.0581 51.3119C39.3247 50.033 38.1795 48.1615 37.839 46.0092C37.4985 43.8569 38.0247 41.7358 39.2938 39.989C40.8414 37.8679 43.1938 36.6514 45.8247 36.6514ZM45.8247 29.1651C41.0581 29.1651 36.3223 31.3798 33.289 35.5908C28.2747 42.5468 29.7914 52.3101 36.6938 57.3633L75.3533 85.7174C78.1081 87.745 81.2962 88.7119 84.4533 88.7119C89.22 88.7119 93.9557 86.4973 96.989 82.2862C102.003 75.3303 100.487 65.567 93.5842 60.5138L54.9247 32.1596C52.17 30.1321 48.9819 29.1651 45.8247 29.1651Z',
    'M69.1938 7.48624C70.8961 7.48624 72.5366 8.01651 73.9295 9.04587L79.47 13.1009C83.0604 15.7211 83.8652 20.8055 81.2342 24.4239L76.4985 30.9743L64.4581 22.1468C60.8676 19.5266 60.0628 14.4422 62.6938 10.8239C64.2414 8.70275 66.5938 7.48624 69.2247 7.48624M69.1938 0C64.4271 0 59.6914 2.21468 56.658 6.42569C51.6438 13.3816 53.1604 23.145 60.0628 28.1982L78.108 41.4239L87.2081 28.822C92.2223 21.8661 90.7057 12.1027 83.8033 7.04954L78.2628 2.99449C75.508 0.966969 72.32 0 69.1628 0H69.1938Z',
    'M15.4914 14.4422C17.1938 14.4422 18.8342 14.9725 20.2271 16.0018C21.9604 17.2807 23.1057 19.1523 23.4462 21.3046C23.7866 23.4569 23.2604 25.578 21.9914 27.3248C20.4438 29.4459 18.0914 30.6624 15.4604 30.6624C12.8295 30.6624 12.1176 30.1321 10.7247 29.1028C8.9914 27.8239 7.84615 25.9523 7.50568 23.8C7.1652 21.6477 7.69139 19.5266 8.96044 17.7798C10.5081 15.6587 12.8604 14.4422 15.4914 14.4422ZM15.4914 6.95597C10.7247 6.95597 5.98901 9.17064 2.95567 13.3817C-2.05861 20.3376 -0.541946 30.1009 6.36043 35.1541C9.1152 37.1817 12.3033 38.1486 15.4604 38.1486C20.2271 38.1486 24.9628 35.9339 27.9962 31.7229C33.0104 24.767 31.4938 15.0037 24.5914 9.95046C21.8366 7.92294 18.6485 6.95597 15.4914 6.95597Z',
    'M23.3533 65.3174L35.3937 74.145C38.9842 76.7652 39.789 81.8495 37.158 85.4679C35.6104 87.589 33.258 88.8055 30.6271 88.8055C27.9961 88.8055 27.2842 88.2752 25.8914 87.2459L20.3509 83.1908C16.7604 80.5706 15.9557 75.4863 18.5866 71.8679L23.3223 65.3174M21.7128 54.8367L12.6128 67.4385C7.59851 74.3945 9.11518 84.1578 16.0176 89.211L21.558 93.2661C24.3128 95.2936 27.5009 96.2606 30.658 96.2606C35.4247 96.2606 40.1604 94.0459 43.1937 89.8349C48.208 82.8789 46.6914 73.1156 39.789 68.0624L21.7438 54.8367H21.7128Z',
]


def logo(uid):
    paths = ''.join(f'<path d="{d}"/>' for d in LOGO_PATHS)
    return (f'<svg viewBox="0 0 100 97" aria-hidden="true"><defs><linearGradient id="lg{uid}" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="97" x2="100" y2="0"><stop offset="0" stop-color="#24D5FF"/><stop offset="1" stop-color="#1670C3"/>'
            f'</linearGradient></defs><g fill="url(#lg{uid})">{paths}</g></svg>')


ICO = {
    'anuncio': '<path d="M3 10v4a1 1 0 001 1h3l5 4V5L7 9H4a1 1 0 00-1 1z"/><path d="M16 9a4 4 0 010 6"/><path d="M19 6a8 8 0 010 12"/>',
    'filtro': '<path d="M4 5h16l-6 7.5V19l-4 1.5v-8L4 5z"/>',
    'lead': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0113 0"/><path d="M16 11l2 2 4-4"/>',
    'chat': '<path d="M20.5 12a8.5 8.5 0 01-12.4 7.5L3.5 21l1.6-4.5A8.5 8.5 0 1120.5 12z"/><path d="M8.5 11h7M8.5 14h4"/>',
    'venda': '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.5"/>',
    'alvo': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><path d="M4 20L20 4"/>',
    'fio': '<path d="M4 7h7a3 3 0 010 6H7a3 3 0 000 6h13"/><circle cx="20" cy="19" r="1.2"/><circle cx="4" cy="7" r="1.2"/>',
    'olho': '<path d="M3 3l18 18"/><path d="M10.6 5.1A10.4 10.4 0 0122 12a17.5 17.5 0 01-3.2 3.9M6.6 6.6A17.8 17.8 0 002 12s3.6 7 10 7a9.9 9.9 0 004.5-1.1"/><path d="M9.9 9.9a3 3 0 004.2 4.2"/>',
}


def ico(nome):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICO[nome]}</svg>'


def head(title, desc, canonical, extra=''):
    robots = 'noindex, nofollow' if STAGING else 'index, follow, max-image-preview:large, max-snippet:-1'
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=" js";setTimeout(function(){{if(!window.__animReady)document.documentElement.className+=" no-anim"}},2500)</script>
<title>{E(title)}</title>
<meta name="description" content="{A(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{A(title)}">
<meta property="og:description" content="{A(desc)}">
<meta property="og:image" content="{SITE}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Komplexa Growth">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#081525">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=Fraunces:ital,wght@1,400;1,500&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
{extra}</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
'''


def header(home=True):
    p = '' if home else 'index.html'
    links = [('#metodo', 'Método'), ('#servicos', 'Serviços'), ('#cases', 'Cases'), ('#hotelaria', 'Hotelaria'), ('#duvidas', 'Dúvidas')]
    nav = ''.join(f'<a href="{p}{h}">{t}</a>' for h, t in links)
    return f'''<header class="hdr">
  <div class="wrap">
    <a class="logo" href="{'#topo' if home else 'index.html'}" aria-label="Komplexa Growth, início">{logo('h')}<span class="logo-txt"><b>Komplexa</b><span>Growth</span></span></a>
    <nav class="nav" aria-label="Principal">{nav}</nav>
    <a class="btn btn-primary hdr-cta" href="{cta('header')}" target="_blank" rel="noopener">Solicitar diagnóstico</a>
    <button class="burger" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="mnav"><span></span></button>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="Menu">
  {nav}
  <a class="btn btn-primary" href="{cta('menu')}" target="_blank" rel="noopener">Solicitar diagnóstico {SETA}</a>
</nav>
'''


def footer(home=True):
    p = '' if home else 'index.html'
    return f'''<footer class="ft">
  <div class="wrap">
    <div class="ft-grid">
      <div>
        <a class="logo" href="{'#topo' if home else 'index.html'}" aria-label="Komplexa Growth">{logo('f')}<span class="logo-txt"><b>Komplexa</b><span>Growth</span></span></a>
        <p>Marketing e comercial para empresas de serviços, do anúncio à venda fechada.</p>
      </div>
      <div class="ft-col">
        <h4>Navegação</h4>
        <a href="{p}#metodo">Método</a><a href="{p}#servicos">Serviços</a><a href="{p}#cases">Cases</a><a href="{p}#duvidas">Dúvidas</a>
        <a href="{HOTEIS}" target="_blank" rel="noopener">Komplexa Hotéis</a>
      </div>
      <div class="ft-col">
        <h4>Contato</h4>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="{whats()}" target="_blank" rel="noopener">WhatsApp {TEL}</a>
        <a href="{INSTA}" target="_blank" rel="noopener">Instagram @komplexagrowth</a>
        <a href="{FACE}" target="_blank" rel="noopener">Facebook</a>
      </div>
      <div class="ft-col">
        <h4>Legal</h4>
        <a href="termos-de-uso.html">Termos de Uso</a>
        <a href="politica-de-privacidade.html">Política de Privacidade</a>
      </div>
    </div>
    <div class="ft-base">
      <span>© <span id="ano">2026</span> Komplexa Growth · CNPJ {CNPJ}</span>
      <span>{E(ENDERECO)}</span>
    </div>
  </div>
</footer>
<script src="assets/js/site.js" defer></script>
</body>
</html>
'''


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + '\n</script>\n'


def ph(valor, rotulo, cls=''):
    """Dado real ou campo marcado como 'a preencher'."""
    if valor:
        return f'<span class="{cls}">{E(valor)}</span>' if cls else E(valor)
    return f'<span class="ph {cls}">[{rotulo}]</span>'


# ======================================================================
# HOME
# ======================================================================
FAQ = [
    ('Para que tipo de empresa a Komplexa Growth trabalha?',
     'Empresas de serviços em que a venda passa por uma conversa: clínicas e consultórios, escolas e cursos, serviços técnicos e '
     'de manutenção, agro, consultorias e serviços B2B. Para hotéis, pousadas e resorts, o atendimento é feito pela Komplexa Hotéis, '
     'o braço da Komplexa dedicado à hotelaria.'),
    ('Vocês cuidam só do marketing ou também do comercial?',
     'Dos dois. O marketing traz e qualifica o contato; a consultoria comercial estrutura o atendimento, o script, o CRM e o '
     'treinamento do time. É essa ligação que permite medir o resultado na venda, e não só no clique.'),
    ('Preciso ter um time comercial?',
     'Não precisa ser grande. Muitas empresas começam com o próprio dono atendendo. O processo é desenhado para o time que existe '
     'hoje e cresce junto com ele.'),
    ('Quem paga a verba de anúncios?',
     'A verba é paga direto ao Google e à Meta, na conta da sua empresa. Contas, dados, site e campanhas ficam no nome da empresa.'),
    ('Como funciona a contratação?',
     'Depois do diagnóstico, você recebe uma proposta com escopo, prazo e investimento definidos para a sua operação. Não existe '
     'pacote pronto: o plano nasce de como a sua empresa vende hoje.'),
    ('Em quanto tempo aparecem resultados?',
     'Depende do ponto de partida e do ciclo de venda do seu serviço. O que muda logo no início é a leitura: com as campanhas no '
     'ar, você passa a ver de onde vem cada contato e cada venda, e as decisões de verba deixam de ser no escuro.'),
]

HOT = [('19x', 'Bahia Bonita', 'hotel boutique', 'de retorno sobre o investimento em mídia'),
       ('7x+', 'Lagamar', 'resort e hotel', 'de retorno sobre o investimento em mídia paga'),
       ('6,5x', 'Pousada Karandá', '', 'de retorno sobre o investimento em mídia paga'),
       ('3,4x', 'Pousada Solar Dona Dora', '', 'de faturamento na baixa temporada'),
       ('60%+', 'Hotel Sunsmart', '', 'das reservas agora são diretas; antes eram 30%')]

DEPO = [
    ('MS', 'Maria Eduarda Silva Macedo', 'Gestora, hotel boutique',
     'Não poderia deixar de registrar minha experiência com a Komplexa Growth. Foi um divisor de águas para nossa ocupação. '
     'Entraram reorganizando nosso funil de reservas do zero, integrando marketing e atendimento de forma cirúrgica. Em menos de 3 '
     'meses já tínhamos dobrado o volume de reservas diretas.'),
    ('FL', 'Fernando Lima', 'Proprietário, pousada',
     'Contratar a Komplexa Growth Marketing foi, sem dúvida, uma das melhores decisões que já tomei para minha pousada. Desde o '
     'primeiro contato, a equipe foi extremamente atenciosa, profissional e comprometida com os resultados. Eles entenderam '
     'exatamente o que eu precisava e entregaram muito mais do que eu esperava.'),
    ('AB', 'Alysson Barbarossi', 'Diretor, hotel',
     'Excelência em tudo. A Komplexa Growth além de ótimo atendimento, tem estratégias que várias agências experientes não tem, o '
     'feeling para hotelaria é baseado em tecnologia e conhecimento real do setor, são completos.'),
]


def home():
    title = 'Komplexa Growth | Marketing e comercial para empresas de serviços'
    desc = ('A Komplexa Growth estrutura o marketing e o comercial de empresas de serviços: traz o cliente certo, qualifica o '
            'contato e prepara o time para fechar, com o resultado medido na venda.')
    org = {'@type': 'ProfessionalService', '@id': f'{SITE}/#organizacao', 'name': 'Komplexa Growth', 'alternateName': 'Komplexa',
           'url': f'{SITE}/', 'logo': f'{SITE}/assets/img/icon-512.png', 'image': f'{SITE}/assets/img/og.jpg',
           'description': desc, 'email': EMAIL, 'telephone': '+55 12 98708-4407', 'taxID': CNPJ,
           'address': {'@type': 'PostalAddress', 'streetAddress': 'Rua dos Piquiroes, 40, Sala 312', 'addressLocality': 'São José dos Campos',
                       'addressRegion': 'SP', 'postalCode': '12246-020', 'addressCountry': 'BR'},
           'areaServed': {'@type': 'Country', 'name': 'Brasil'},
           'knowsAbout': ['marketing para empresas de serviços', 'tráfego pago', 'Google Ads', 'Meta Ads', 'geração de leads qualificados',
                          'consultoria comercial', 'processo comercial', 'CRM', 'landing pages', 'Instagram para empresas'],
           'subOrganization': {'@type': 'Organization', 'name': 'Komplexa Hotéis', 'url': HOTEIS},
           'founder': {'@type': 'Person', 'name': 'Igor Salomão', 'url': 'https://komplexahoteis.com/igor-salomao.html'},
           'sameAs': [INSTA, FACE]}
    graph = {'@context': 'https://schema.org', '@graph': [
        org,
        {'@type': 'WebSite', '@id': f'{SITE}/#site', 'url': f'{SITE}/', 'name': 'Komplexa Growth', 'inLanguage': 'pt-BR',
         'publisher': {'@id': f'{SITE}/#organizacao'}},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]},
    ]}

    passos_pipe = [
        ('anuncio', 'Anúncio', '<small>Google Ads · Pesquisa</small>', 'clique', ''),
        ('filtro', 'Site que qualifica', '<small><span class="chip">Segmento</span><span class="chip">Porte</span><span class="chip">Urgência</span></small>', 'filtro', ''),
        ('lead', 'Lead qualificado no CRM', '<small>Origem registrada, responsável definido</small>', 'contato', ''),
        ('chat', 'Atendimento com script', '<small>Resposta rápida, diagnóstico, proposta</small>', 'conversa', ''),
        ('venda', 'Venda fechada', '<small>Origem: Google Ads · Pesquisa</small>', '✓ venda', ' win'),
    ]
    pipe = ''.join(f'<li class="st{w}"><span class="ic">{ico(i)}</span><div><b>{t}</b>{s}</div>'
                   f'<span class="tag{" ok" if w else ""}">{tg}</span></li>' for i, t, s, tg, w in passos_pipe)

    cases_html = ''.join(f'''
      <article class="case" data-rv="{n % 2 + 1}">
        <div class="case-top"><span class="case-nome">{E(c['nome'])}</span><span class="case-seg">{ph(c['segmento'], 'segmento')}</span></div>
        <span class="case-num{'' if c['numero'] else ' ph'}">{E(c['numero']) if c['numero'] else '[resultado]'}</span>
        <p>{ph(c['resultado'], 'o que mudou, em uma frase')}</p>
        <span class="per">{ph(c['periodo'], 'período')}</span>
      </article>''' for n, c in enumerate(CASES))

    hot_html = ''.join(
        f'<div class="hs{" full" if i == 4 else ""}" data-rv="{i % 3 + 1}"><b>{n}</b><span><strong>{E(q)}</strong>{(" (" + t + ")") if t else ""}: {E(d)}.</span></div>'
        for i, (n, q, t, d) in enumerate(HOT))
    depo_html = ''.join(f'''
      <figure class="dp" data-rv="{i + 1}">
        <blockquote>{E(t)}</blockquote>
        <figcaption><i>{ini}</i><span><b>{E(n)}</b><small>{E(c)}</small></span></figcaption>
      </figure>''' for i, (ini, n, c, t) in enumerate(DEPO))
    faq_html = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ)

    body = f'''{header()}
<main id="conteudo">

<section class="hero dark grid-bg" id="topo">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow" data-rv>Marketing e comercial para empresas de serviços</span>
      <h1 data-rv="2">Do anúncio à venda fechada, <em>numa operação só.</em></h1>
      <p class="lead" data-rv="3">A Komplexa Growth estrutura o marketing e o comercial da sua empresa: traz o cliente certo, qualifica cada contato e prepara o seu time para fechar. E mede o resultado na venda, não no clique.</p>
      <div class="hero-ctas" data-rv="4">
        <a class="btn btn-primary" href="{cta('hero')}" target="_blank" rel="noopener">Solicitar diagnóstico {SETA}</a>
        <a class="btn btn-ghost" href="#metodo">Ver como funciona</a>
      </div>
      <div class="certs" data-rv="4"><span class="lbl">Certificações</span><span class="cert"><i></i>Google Partner</span><span class="cert"><i></i>HubSpot Certified</span><span class="cert"><i></i>Salesforce Partner</span></div>
    </div>
    <div class="pipe" data-rv="3" aria-label="Exemplo do caminho de um cliente, do anúncio à venda">
      <div class="pipe-top"><b>Da origem à venda</b><span>rastreado</span></div>
      <ol class="steps">{pipe}</ol>
    </div>
  </div>
</section>

<section class="soft" id="problema">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow" data-rv>O problema</span>
      <h2 data-rv="2">O anúncio traz clique. <em>A venda</em> se perde no caminho.</h2>
      <p class="lead" data-rv="3">Na maioria das empresas de serviços, marketing e comercial trabalham separados. A agência entrega relatório de cliques, o time reclama da qualidade dos contatos e ninguém sabe dizer de onde veio a última venda.</p>
    </div>
    <div class="cards3">
      <article class="card" data-rv="1"><span class="n">01</span><span class="ico">{ico('alvo')}</span><h3>Contato que não é cliente</h3><p>Anúncio aberto demais traz curioso, gente fora da sua região e quem só quer preço. O time perde o dia respondendo quem nunca ia comprar.</p></article>
      <article class="card" data-rv="2"><span class="n">02</span><span class="ico">{ico('fio')}</span><h3>Atendimento sem processo</h3><p>Cada pessoa responde de um jeito, o retorno demora e o contato esfria no WhatsApp. O que funciona na mão de um não vira padrão da empresa.</p></article>
      <article class="card" data-rv="3"><span class="n">03</span><span class="ico">{ico('olho')}</span><h3>Investimento sem rastreio</h3><p>Sem ligar o anúncio à venda, a verba é decidida no achismo: corta o que funcionava e mantém o que só gerava clique.</p></article>
    </div>
  </div>
</section>

<section class="dark grid-bg" id="metodo">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow" data-rv>Como funciona</span>
      <h2 data-rv="2">Um método, do diagnóstico <em>à venda medida.</em></h2>
    </div>
    <div class="metodo">
      <div class="passo" data-rv="1"><span class="num">01</span><h3>Diagnóstico</h3><p>Entendemos como a empresa vende hoje: de onde vêm os clientes, como o time atende, onde a venda trava e quanto custa cada cliente novo.</p></div>
      <div class="passo" data-rv="2"><span class="num">02</span><h3>Implantação</h3><p>Colocamos de pé o que falta: site que qualifica, campanhas, criativos, script de atendimento e CRM, tudo ligado do anúncio à venda.</p></div>
      <div class="passo" data-rv="3"><span class="num">03</span><h3>Operação</h3><p>Rodamos e ajustamos toda semana: campanhas, criativos novos e acompanhamento do time comercial nas conversas reais.</p></div>
      <div class="passo" data-rv="4"><span class="num">04</span><h3>Medição na venda</h3><p>Cada venda é ligada à origem. Todo mês você vê quantas vendas e quanto de receita cada canal trouxe, e a verba vai para o que vende.</p></div>
    </div>
    <div class="metodo-nota" data-rv>
      <p><b>Projeto com escopo e prazo definidos na proposta.</b> Um time só responde pelo marketing e pelo comercial, sem jogo de empurra entre agência e vendas.</p>
      <a class="btn btn-primary" href="{cta('metodo')}" target="_blank" rel="noopener">Solicitar diagnóstico {SETA}</a>
    </div>
  </div>
</section>

<section id="servicos">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow" data-rv>O que entregamos</span>
      <h2 data-rv="2">Marketing e comercial <em>trabalhando juntos.</em></h2>
      <p class="lead" data-rv="3">Cada empresa recebe o conjunto que faz sentido para a operação dela, definido no diagnóstico.</p>
    </div>
    <div class="serv">
      <article class="sv" data-rv="1"><div class="sv-art"><div class="mini m-site"><div class="bar"><i></i><i></i><i></i></div><div class="q">segmento <b>✓</b></div><div class="q">porte <b>✓</b></div><div class="q">urgência <b>✓</b></div><div class="go">Quero uma proposta</div></div></div>
        <div class="sv-body"><h3>Site que filtra e qualifica</h3><p>Páginas que explicam o serviço, respondem objeções e pedem as informações certas antes do contato. O time recebe quem tem perfil.</p></div></article>
      <article class="sv" data-rv="2"><div class="sv-art"><div class="mini m-ads"><span>Google · Pesquisa <em>intenção</em></span><span>Meta · Feed e Reels <em>perfil</em></span><span>Remarketing <em>retorno</em></span></div></div>
        <div class="sv-body"><h3>Tráfego pago no Google e na Meta</h3><p>Campanhas na conta da sua empresa, para quem já procura o seu serviço e para quem tem o perfil dos seus melhores clientes.</p></div></article>
      <article class="sv" data-rv="3"><div class="sv-art"><div class="mini m-cria"><i></i><i></i><i></i></div></div>
        <div class="sv-body"><h3>Criativos</h3><p>Anúncios em vídeo e imagem feitos para cada etapa da decisão, testados até achar o que traz cliente.</p></div></article>
      <article class="sv" data-rv="1"><div class="sv-art"><div class="mini m-land"><div class="h"></div><div class="s"></div><div class="go">Uma oferta, um botão</div></div></div>
        <div class="sv-body"><h3>Landing pages por oferta</h3><p>Uma página para cada serviço ou campanha, com uma mensagem clara e um único próximo passo.</p></div></article>
      <article class="sv" data-rv="2"><div class="sv-art"><div class="mini m-ig"><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
        <div class="sv-body"><h3>Instagram estruturado</h3><p>Perfil organizado como vitrine: bio, destaques e publicações que mostram por que confiar na sua empresa.</p></div></article>
      <article class="sv" data-rv="3"><div class="sv-art"><div class="mini m-chat"><span class="c">Oi! Vi o anúncio, vocês atendem na minha região?</span><span class="k"><em>script · diagnóstico</em>Atendemos sim. Para indicar o melhor caminho, me conta…</span></div></div>
        <div class="sv-body"><h3>Consultoria comercial</h3><p>Script de atendimento, processo de qualificação, CRM e treinamento do time, para o contato virar venda.</p></div></article>
      <article class="sv wide" data-rv><div class="sv-art"><div class="mini m-rast"><i style="height:38%"></i><i style="height:62%"></i><i style="height:48%"></i><i style="height:86%"></i><span class="lg"><b>Venda por origem</b><span>Google · Meta · Indicação</span></span></div></div>
        <div class="sv-body"><h3>Rastreio até a venda e reunião mensal</h3><p>Da origem do contato à venda fechada. Todo mês você vê o que trouxe cliente, quanto custou cada venda e para onde a verba deve ir.</p></div></article>
    </div>
  </div>
</section>

<section class="dark grid-bg" id="cases">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow" data-rv>Cases</span>
      <h2 data-rv="2">Resultados de <em>empresas de serviços.</em></h2>
    </div>
    <div class="cases">{cases_html}
    </div>
  </div>
</section>

<section class="soft" id="hotelaria">
  <div class="wrap">
    <div class="hot">
      <div>
        <span class="eyebrow" data-rv>Hotelaria</span>
        <h2 data-rv="2">Hotel, pousada ou resort? <em>Conheça a Komplexa Hotéis.</em></h2>
        <p class="lead" data-rv="3">A Komplexa Hotéis é o braço da Komplexa dedicado à hotelaria, com o mesmo método aplicado às reservas diretas. Resultados conferidos no sistema de cada hotel.</p>
        <a class="btn btn-line" href="{HOTEIS}" target="_blank" rel="noopener" data-rv="4">Conhecer a Komplexa Hotéis {SETA}</a>
      </div>
      <div class="hot-stats">{hot_html}</div>
    </div>
    <div class="depo">{depo_html}
    </div>
  </div>
</section>

<section id="para-quem">
  <div class="wrap quem">
    <div>
      <span class="eyebrow" data-rv>Para quem</span>
      <h2 data-rv="2">Para empresas de serviços que <em>vendem por contato.</em></h2>
      <p class="lead" data-rv="3">Quando a venda passa por uma conversa, seja no WhatsApp, por telefone, numa visita ou num orçamento, o marketing sozinho não resolve. É aí que a operação integrada faz diferença.</p>
      <div class="segs" data-rv="4"><span>Clínicas e consultórios</span><span>Escolas e cursos</span><span>Serviços técnicos e manutenção</span><span>Agro</span><span>Consultorias e serviços B2B</span><span>Outros serviços</span></div>
    </div>
    <div class="check" data-rv="2">
      <h3>Faz sentido conversar se:</h3>
      <ul>
        <li>Você investe em anúncio e não sabe quantas vendas vieram dele.</li>
        <li>O time reclama da qualidade dos contatos que chegam.</li>
        <li>As vendas ainda dependem de indicação.</li>
        <li>O WhatsApp enche, mas a agenda e o fechamento não acompanham.</li>
      </ul>
      <a class="btn btn-primary" href="{cta('para-quem')}" target="_blank" rel="noopener">Solicitar diagnóstico {SETA}</a>
    </div>
  </div>
</section>

<section class="soft" id="duvidas">
  <div class="wrap">
    <div class="sec-head center">
      <span class="eyebrow" data-rv>Dúvidas</span>
      <h2 data-rv="2">Perguntas <em>frequentes.</em></h2>
    </div>
    <div class="faq" data-rv="3">{faq_html}</div>
  </div>
</section>

<section class="dark grid-bg cta" id="contato">
  <div class="wrap">
    <span class="eyebrow" data-rv>Diagnóstico</span>
    <h2 data-rv="2">Vamos olhar <em>o comercial</em> da sua empresa?</h2>
    <p class="lead" data-rv="3">No diagnóstico, entendemos como a sua empresa vende hoje e mostramos, com os seus números, onde estão as maiores oportunidades. Sem compromisso.</p>
    <div class="hero-ctas" data-rv="4">
      <a class="btn btn-primary" href="{cta('final')}" target="_blank" rel="noopener">Solicitar diagnóstico {SETA}</a>
      <a class="btn btn-ghost" href="{whats()}" target="_blank" rel="noopener">Falar no WhatsApp</a>
    </div>
    <div class="contatos"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{whats()}" target="_blank" rel="noopener">{TEL}</a><a href="{INSTA}" target="_blank" rel="noopener">@komplexagrowth</a></div>
  </div>
</section>

</main>
{footer()}'''
    return head(title, desc, f'{SITE}/', ld(graph)) + body


# ======================================================================
# PÁGINAS DE TEXTO
# ======================================================================
def pagina_texto(slug, titulo, subtitulo, miolo, desc):
    return (head(f'{titulo} | Komplexa Growth', desc, f'{SITE}/{slug}') + header(home=False) + f'''<main id="conteudo">
<section class="dark grid-bg pg-hero"><div class="wrap"><span class="eyebrow">Komplexa Growth</span><h1>{E(titulo)}</h1><p>{E(subtitulo)}</p></div></section>
<section><div class="wrap"><div class="doc">
{miolo}
</div></div></section>
</main>
''' + footer(home=False))


def lista(itens):
    return '<ul>' + ''.join(f'<li>{E(i)}</li>' for i in itens) + '</ul>'


TERMOS = f'''<h2>1. Aceitação dos Termos</h2>
<p>Ao acessar e utilizar os serviços da Komplexa Growth, você concorda com estes Termos de Uso e com nossa Política de Privacidade. Se você não concorda com qualquer parte destes termos, não deve utilizar nossos serviços.</p>
<h2>2. Descrição dos Serviços</h2>
<p>A Komplexa Growth oferece serviços especializados em marketing digital, estruturação comercial, consultoria estratégica e desenvolvimento de metodologias comerciais para empresas de serviços. Nossos serviços incluem, mas não se limitam a:</p>
{lista(['Consultoria em estratégia comercial', 'Desenvolvimento de processos comerciais', 'Marketing digital e geração de leads qualificados', 'Treinamento e capacitação de equipes comerciais', 'Análise e otimização de funis de vendas'])}
<h2>3. Cadastro e Conta do Usuário</h2>
<p>Para utilizar determinados serviços, você pode precisar criar uma conta e fornecer informações precisas e completas. Você é responsável por:</p>
{lista(['Manter a confidencialidade de suas credenciais de acesso', 'Atualizar suas informações cadastrais quando necessário', 'Notificar imediatamente sobre qualquer uso não autorizado de sua conta', 'Todas as atividades realizadas através de sua conta'])}
<h2>4. Uso Aceitável</h2>
<p>Você concorda em não utilizar nossos serviços para:</p>
{lista(['Violar leis, regulamentos ou direitos de terceiros', 'Transmitir conteúdo ilegal, ofensivo ou prejudicial', 'Interferir no funcionamento adequado dos serviços', 'Tentar acessar áreas restritas sem autorização', 'Copiar, modificar ou distribuir nosso conteúdo sem permissão', 'Utilizar técnicas de engenharia reversa em nossos sistemas'])}
<h2>5. Propriedade Intelectual</h2>
<p>Todo o conteúdo disponibilizado pela Komplexa Growth, incluindo textos, imagens, logos, metodologias, ferramentas, software e materiais de treinamento, é protegido por direitos autorais e outras leis de propriedade intelectual.</p>
<p>É proibida a reprodução, distribuição ou uso comercial de qualquer material sem autorização prévia por escrito da Komplexa Growth.</p>
<h2>6. Contratação de Serviços</h2>
<p>A contratação de nossos serviços está sujeita a proposta comercial específica, que estabelecerá:</p>
{lista(['Escopo detalhado dos serviços', 'Prazos de execução e entrega', 'Valores e formas de pagamento', 'Responsabilidades de ambas as partes', 'Condições de cancelamento e reembolso'])}
<h2>7. Pagamentos e Reembolsos</h2>
<p>Os valores, formas de pagamento e políticas de reembolso serão estabelecidos na proposta comercial específica de cada projeto. Reservamo-nos o direito de suspender serviços em caso de inadimplência.</p>
<h2>8. Confidencialidade</h2>
<p>Ambas as partes se comprometem a manter confidenciais todas as informações privilegiadas compartilhadas durante a prestação dos serviços, incluindo estratégias, dados comerciais, metodologias e informações de clientes.</p>
<h2>9. Resultados e Garantias</h2>
<p>Embora nos esforcemos para entregar os melhores resultados possíveis, não garantimos resultados específicos de vendas ou marketing, pois estes dependem de múltiplos fatores, incluindo execução pelo cliente, condições de mercado e fatores externos.</p>
<p>Garantimos apenas a entrega profissional dos serviços contratados conforme especificado na proposta comercial.</p>
<h2>10. Limitação de Responsabilidade</h2>
<p>A Komplexa Growth não se responsabiliza por:</p>
{lista(['Danos indiretos, incidentais ou consequenciais', 'Perda de lucros ou oportunidades de negócio', 'Resultados obtidos após implementação incorreta de nossas recomendações', 'Falhas em sistemas de terceiros utilizados nos projetos', 'Casos fortuitos ou força maior'])}
<h2>11. Modificações nos Termos</h2>
<p>Reservamo-nos o direito de modificar estes Termos de Uso a qualquer momento. Alterações significativas serão comunicadas por e-mail ou através do site. O uso continuado dos serviços após modificações constitui aceitação dos novos termos.</p>
<h2>12. Rescisão</h2>
<p>Podemos suspender ou encerrar seu acesso aos serviços imediatamente, sem aviso prévio, em caso de violação destes Termos de Uso. Você pode cancelar sua conta a qualquer momento, sujeito às condições contratuais específicas.</p>
<h2>13. Lei Aplicável e Foro</h2>
<p>Estes Termos de Uso são regidos pelas leis da República Federativa do Brasil. Quaisquer disputas serão resolvidas no foro da comarca de São José dos Campos, SP, com exclusão de qualquer outro, por mais privilegiado que seja.</p>
<h2>14. Disposições Gerais</h2>
<p>Se qualquer disposição destes termos for considerada inválida ou inexequível, as demais disposições permanecerão em pleno vigor e efeito.</p>
<p>A falha em exercer qualquer direito previsto nestes termos não constituirá renúncia a tal direito.</p>
<h2>15. Contato</h2>
<p>Para questões sobre estes Termos de Uso, entre em contato conosco pelo e-mail <a href="mailto:{EMAIL}">{EMAIL}</a> ou pelo site www.komplexagrowth.com.</p>
<p>Ao utilizar os serviços da Komplexa Growth, você declara ter lido, compreendido e concordado com estes Termos de Uso em sua totalidade.</p>'''

PRIVACIDADE = f'''<p>A Komplexa Growth ("Komplexa", "nós") adota esta Política de Privacidade para explicar como coletamos, utilizamos, tratamos, armazenamos, compartilhamos e protegemos dados pessoais fornecidos direta ou indiretamente ao interagir com nossos sites, landing pages, formulários, campanhas, plataformas, automações ou qualquer serviço pertencente ao Ecossistema Digital Komplexa ou operado pela Komplexa para seus clientes.</p>
<p>Ao preencher um formulário, acessar nossos sites, contratar nossos serviços ou interagir com qualquer ambiente digital operado por nós, você concorda integralmente com esta Política de Privacidade.</p>
<h2>1. Categorias de Dados Pessoais Coletados</h2>
<p>Podemos coletar diferentes categorias de dados pessoais conforme sua interação conosco ou com clientes atendidos pela Komplexa.</p>
<h3>1.1 Dados Cadastrais</h3>
<p>Incluem informações fornecidas para identificação e contato, tais como nome, e-mail, telefone, endereço, CPF, empresa, cargo, data de nascimento, incluindo, mas não se limitando a outras informações semelhantes fornecidas voluntariamente pelo titular.</p>
<h3>1.2 Dados de Comunicação e Atendimento</h3>
<p>Referem-se às interações realizadas nos canais de comunicação operados por nós ou por clientes, tais como mensagens, histórico de WhatsApp, formulários, registros de atendimento, incluindo, mas não se limitando a dados enviados por texto, áudio, vídeo ou anexos.</p>
<h3>1.3 Dados Comerciais e de Negociação</h3>
<p>Informações relacionadas a intenções de compra, solicitações e transações, tais como orçamento desejado, produtos ou serviços de interesse, histórico de compras, dados fornecidos em propostas e processos comerciais, incluindo, mas não se limitando a registros em CRM.</p>
<h3>1.4 Dados de Navegação e Tecnológicos</h3>
<p>Coletados automaticamente através de cookies, pixels e ferramentas de análise, tais como endereço IP, localização aproximada, UTMs, ID do dispositivo, navegador, páginas acessadas, origem do tráfego, incluindo, mas não se limitando a dados obtidos via dispositivos móveis, redes sociais e integrações.</p>
<h3>1.5 Dados de Comportamento em Campanhas</h3>
<p>Relacionados à interação com anúncios, automações e fluxos de marketing, tais como cliques, visualizações, preenchimento de formulários, engajamento em campanhas, incluindo, mas não se limitando a dados coletados via Meta Ads, Google Ads, TikTok Ads, LinkedIn Ads e similares.</p>
<h3>1.6 Dados Sensíveis (quando aplicável)</h3>
<p>Coletados apenas quando estritamente necessário e mediante consentimento específico, tais como informações de saúde, necessidades especiais ou preferências pessoais, incluindo, mas não se limitando a dados fornecidos espontaneamente pelo titular.</p>
<h2>2. Finalidades do Tratamento de Dados</h2>
<p>O tratamento dos dados pessoais ocorre para viabilizar a operação do Ecossistema Digital Komplexa e dos projetos de clientes atendidos. As principais finalidades incluem:</p>
<h3>2.1 Execução de Campanhas de Marketing</h3>
<p>Segmentação, direcionamento de anúncios, criação de públicos personalizados, retargeting, mensuração e análise de performance.</p>
<h3>2.2 Comunicação e Relacionamento</h3>
<p>Retorno de contato, envio de propostas, agendamentos, atendimento via WhatsApp, nutrição de leads e suporte.</p>
<h3>2.3 Automação e CRM</h3>
<p>Registro de informações em CRM, comunicação automatizada, acompanhamento de atividades e integração entre ferramentas.</p>
<h3>2.4 Melhoria de Experiência e Produto</h3>
<p>Análise de comportamento, testes A/B, otimização de páginas e personalização de conteúdos.</p>
<h3>2.5 Cumprimento de Obrigações Legais e Regulatórias</h3>
<h3>2.6 Proteção do Titular e da Komplexa</h3>
<h2>3. Bases Legais Utilizadas</h2>
<p>O tratamento de dados pode ocorrer com base em:</p>
{lista(['Consentimento', 'Legítimo interesse', 'Execução de contrato', 'Cumprimento de obrigação legal', 'Proteção do crédito', 'Exercício regular de direitos', 'Proteção da vida e segurança'])}
<h2>4. Compartilhamento de Dados</h2>
<p>Podemos compartilhar dados com:</p>
<h3>4.1 Plataformas de Anúncios</h3>
<p>Meta, Google, TikTok, LinkedIn, Pinterest e outras.</p>
<h3>4.2 Ferramentas de Gestão e Automação</h3>
<p>CRM, Supabase, ManyChat, Kommo, RD Station, Google Sheets, n8n, Zapier e sistemas equivalentes.</p>
<h3>4.3 Parceiros e Fornecedores</h3>
<p>Serviços de hospedagem, e-mail, autenticação, segurança, analytics e processamento de dados.</p>
<h3>4.4 Clientes Atendidos pela Komplexa</h3>
<p>Quando o titular preenche um formulário de um cliente, os dados são compartilhados também com esse cliente para fins comerciais e de atendimento.</p>
<h2>5. Transferência Internacional de Dados</h2>
<p>Os dados podem ser transferidos para outros países quando necessárias integrações com plataformas internacionais, sempre observando os requisitos de proteção adequados previstos na LGPD.</p>
<h2>6. Retenção e Armazenamento</h2>
<p>Os dados serão mantidos pelo tempo necessário para cumprir:</p>
{lista(['Finalidades comerciais ou contratuais', 'Obrigações legais', 'Exercício regular de direitos', 'Período de vigência do projeto'])}
<p>Após esse período, poderão ser excluídos ou anonimizados.</p>
<h2>7. Segurança dos Dados</h2>
<p>Adotamos medidas técnicas e administrativas para proteger os dados contra acesso não autorizado, perda, alteração, divulgação ou qualquer forma de tratamento inadequado.</p>
<p>Essas medidas incluem criptografia, controle de acesso, firewalls, backups e monitoramento interno.</p>
<h2>8. Direitos do Titular</h2>
<p>O titular pode solicitar:</p>
{lista(['Acesso aos dados', 'Correção', 'Exclusão', 'Portabilidade', 'Informação sobre compartilhamento', 'Revogação do consentimento', 'Limitação do uso'])}
<p>Para exercer seus direitos, envie um e-mail para <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>9. Atualizações desta Política</h2>
<p>Esta política pode ser atualizada a qualquer momento para refletir melhorias, alterações legais ou mudanças operacionais. As atualizações passam a valer imediatamente após publicação.</p>
<h2>10. Contato do Encarregado (DPO)</h2>
<p>Cauã Dantas, Encarregado de Proteção de Dados. E-mail: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>'''

N404 = f'''<p>O endereço que você abriu não existe ou mudou de lugar.</p>
<p><a href="index.html">Voltar para o início</a> ou <a href="{cta('404')}" target="_blank" rel="noopener">solicitar um diagnóstico</a>.</p>'''


def llms():
    cases = '\n'.join(f"- {c['nome']}" + (f" ({c['segmento']}): {c['numero']} {c['resultado']}" if c['numero'] and c['resultado'] else '')
                      for c in CASES)
    return f'''# Komplexa Growth

> Empresa de marketing e comercial para empresas de serviços no Brasil. Estrutura o marketing e o comercial do cliente, do anúncio à venda fechada: traz o cliente certo, qualifica cada contato, prepara o time para fechar e mede o resultado na venda, não no clique. Sede em São José dos Campos, SP (CNPJ {CNPJ}).

- Site: {SITE}/
- Contato: {EMAIL} · WhatsApp {TEL}
- Diagnóstico: {FORM}
- Instagram: {INSTA}
- Hotelaria: a Komplexa Hotéis ({HOTEIS}) é o braço da Komplexa dedicado a hotéis, pousadas e resorts.

## Para quem

Empresas de serviços em que a venda passa por uma conversa: clínicas e consultórios, escolas e cursos, serviços técnicos e de manutenção, agro, consultorias e serviços B2B.

## Método

1. Diagnóstico: como a empresa vende hoje, de onde vêm os clientes, onde a venda trava e quanto custa cada cliente novo.
2. Implantação: site que qualifica, campanhas, criativos, script de atendimento e CRM, ligados do anúncio à venda.
3. Operação: ajustes semanais nas campanhas, criativos novos e acompanhamento do time comercial.
4. Medição na venda: cada venda ligada à origem, com reunião mensal de resultado.

## Serviços

- Site que filtra e qualifica o contato antes do atendimento
- Tráfego pago no Google e na Meta, na conta da empresa cliente
- Criativos em vídeo e imagem para cada etapa da decisão
- Landing pages por oferta
- Instagram estruturado
- Consultoria comercial: script, processo de qualificação, CRM e treinamento do time
- Rastreio até a venda e relatório mensal

## Clientes

{cases}

## Certificações

Google Partner, HubSpot Certified, Salesforce Partner.
'''


def escreve(nome, conteudo):
    with io.open(os.path.join(ROOT, nome), 'w', encoding='utf-8', newline='\n') as f:
        f.write(conteudo)


if __name__ == '__main__':
    escreve('index.html', home())
    escreve('termos-de-uso.html', pagina_texto('termos-de-uso', 'Termos de Uso', 'Última atualização: 01/10/2026', TERMOS,
                                               'Termos de Uso dos serviços e do site da Komplexa Growth.'))
    escreve('politica-de-privacidade.html', pagina_texto('politica-de-privacidade', 'Política de Privacidade', 'Última atualização: 17/11/2025', PRIVACIDADE,
                                                         'Como a Komplexa Growth coleta, usa, compartilha e protege dados pessoais.'))
    escreve('404.html', pagina_texto('404', 'Página não encontrada', 'Esse endereço não existe mais.', N404, 'Página não encontrada.'))
    escreve('llms.txt', llms())
    escreve('robots.txt', 'User-agent: *\nDisallow: /\n' if STAGING else f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    urls = ['', 'termos-de-uso', 'politica-de-privacidade']
    escreve('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
            ''.join(f'  <url><loc>{SITE}/{u}</loc><lastmod>{HOJE}</lastmod></url>\n' for u in urls) + '</urlset>\n')
    escreve('site.webmanifest', json.dumps({'name': 'Komplexa Growth', 'short_name': 'Komplexa Growth',
                                            'icons': [{'src': 'assets/img/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                                      {'src': 'assets/img/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
                                            'theme_color': '#081525', 'background_color': '#081525', 'display': 'browser'},
                                           ensure_ascii=False, indent=2) + '\n')
    cname = os.path.join(ROOT, 'CNAME')
    if STAGING:
        if os.path.exists(cname):
            os.remove(cname)
    else:
        escreve('CNAME', 'komplexagrowth.com\n')
    faltam = sum(1 for c in CASES for k in ('segmento', 'numero', 'resultado', 'periodo') if not c[k])
    print('site gerado |', 'STAGING (noindex)' if STAGING else 'PRODUÇÃO', '| campos de case a preencher:', faltam)
