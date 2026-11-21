import re, os
APP = "https://app.movoapp.com.br/"
# Lojas. APPSTORE_ID = "Apple ID" do app no App Store Connect (Informações do app). Sem ele, o build para.
APPSTORE_ID = "6833195728"
PLAY_ID = "br.com.movoapp.app"
# Google Play aberto ao público? Enquanto False, a landing mostra só a App Store (decisão do Andre, 21/11/2026).
PLAY_ABERTO = False
if not APPSTORE_ID.isdigit():
    raise SystemExit('build.py: preencha APPSTORE_ID (Apple ID numérico do app)')
APPSTORE = "https://apps.apple.com/br/app/id" + APPSTORE_ID
PLAY = "https://play.google.com/store/apps/details?id=" + PLAY_ID
PLAY_LP = PLAY + "&amp;referrer=utm_source%3Dlp"  # origem: quem instala pela landing
tpl = open('template.html', encoding='utf-8').read()

def sem_play(html, lang):
    """Enquanto o Google Play não abre: tira os botões e as menções à Play."""
    if PLAY_ABERTO:
        return html
    html, n = re.subn(r'<a class="btn ghost store st-and"[^>]*>.*?</a>', '', html)
    assert n == 2, n
    html, n = re.subn(r',"https://play\.google\.com/[^"]*"\]', ']', html)
    assert n == 1, n
    trocas = {
        'pt': [('Na App&nbsp;Store e no Google&nbsp;Play', 'Na App&nbsp;Store'),
               ('Grátis na App Store, no Google Play e no navegador.', 'Grátis na App Store e no navegador.'),
               ('(iPhone) ou no <a href="' + PLAY_LP + '&amp;hl=pt_BR" data-cta="play-faq">Google Play</a> (Android) e entre com o código que chega no seu e-mail.',
                '(iPhone) e entre com o código que chega no seu e-mail. O app para Android chega ao Google Play em breve.'),
               ('Sim, nos apps para iPhone e Android. O Movo traz os treinos que o relógio salva no app Saúde (iPhone) ou no Health Connect (Android).',
                'Sim, no app para iPhone: o Movo traz os treinos que o relógio salva no app Saúde. No Android, isso chega com o app no Google Play, pelo Health Connect.')],
        'en': [('On the App&nbsp;Store and Google&nbsp;Play', 'On the App&nbsp;Store'),
               ('Free on the App Store, Google Play and the web.', 'Free on the App Store and the web.'),
               ('(iPhone) or <a href="' + PLAY_LP.replace('utm_source%3Dlp', 'utm_source%3Dlp-en') + '&amp;hl=en" data-cta="play-faq">Google Play</a> (Android) and sign in with the code sent to your email.',
                '(iPhone) and sign in with the code sent to your email. The Android app is coming soon to Google Play.'),
               ('Yes, in the iPhone and Android apps. Movo brings in the workouts your watch saves to Apple Health (iPhone) or Health Connect (Android).',
                'Yes, in the iPhone app: Movo brings in the workouts your watch saves to Apple Health. On Android, this comes with the Google Play app, through Health Connect.')],
    }[lang]
    for a, b in trocas:
        if html.count(a) != 1:
            raise SystemExit(f'sem_play ({lang}): trecho não achado: {a[:70]}')
        html = html.replace(a, b)
    return html

def pic(m):
    name, alt, mode = m.group(1), m.group(2), m.group(3) or 'lazy'
    attrs = 'fetchpriority="high"' if mode == 'eager' else 'loading="lazy" decoding="async"'
    sizes = '(min-width:1000px) 320px, 62vw'
    return (f'<picture><source type="image/avif" srcset="media/shot-{name}-360.avif 360w, media/shot-{name}-720.avif 720w" sizes="{sizes}">'
            f'<source type="image/webp" srcset="media/shot-{name}-360.webp 360w, media/shot-{name}-720.webp 720w" sizes="{sizes}">'
            f'<img src="media/shot-{name}-720.webp" width="720" height="1558" alt="{alt}" {attrs}></picture>')
tpl = re.sub(r'\{\{pic ([a-z\-]+) "([^"]+)"(?: (eager))?\}\}', pic, tpl)
tpl = tpl.replace('{{PLAYURL}}', PLAY).replace('{{APPSTORE}}', APPSTORE).replace('{{PLAY}}', PLAY_LP + '&amp;hl=pt_BR').replace('{{APP}}', APP)
tpl = sem_play(tpl, 'pt')
open('../index.html', 'w', encoding='utf-8').write(tpl)
print('index.html', len(tpl.encode()))

# Página de convite: link estável movoapp.com.br/convite/?desafio=CODE (ou ?treinador= / ?prof=) que leva ao app,
# esteja ele em qualquer endereço. Ao migrar o app, só trocar APP acima e rodar este build de novo.
import os
os.makedirs('../convite', exist_ok=True)
conv = open('convite.html', encoding='utf-8').read().replace('{{APP}}', APP)
open('../convite/index.html', 'w', encoding='utf-8').write(conv)
print('convite/index.html', len(conv.encode()))

# Landing em inglês: movoapp.com.br/en/ (pares em en.py). Os links para o app levam ?lang=en, e o app abre em inglês.
from en import PARES
en_html = open('template.html', encoding='utf-8').read()
# Desafio: print próprio em inglês (criar desafio). Treinador: o print só existe em português, então a versão em inglês
# fica sem ele e os cartões ocupam a largura toda (estilo no fim do <head>).
en_html = re.sub(r'\{\{pic desafio "[^"]*"\}\}', '{{pic desafio-en "Creating a challenge in Movo: weekly goal, coffee on the line, simple points or who runs the most."}}', en_html)
en_html = re.sub(r'<div class="media"><div class="phone lime">\{\{pic treinador "[^"]*"\}\}</div></div>\s*', '', en_html)
for pt, en_txt in PARES:
    if pt not in en_html:
        raise SystemExit(f'en.py: trecho não achado no template: {pt[:80]}')
    en_html = en_html.replace(pt, en_txt)
# Prints do app em inglês (media/shot-*-en-*); os que ainda não existem em inglês usam os em português.
for n in ('plano', 'treino', 'origens'):
    en_html = en_html.replace('{{pic ' + n + ' ', '{{pic ' + n + '-en ')
en_html = en_html.replace('{{APP}}?utm_source=lp', '{{APP}}?lang=en&utm_source=lp-en').replace("var u='{{APP}}'", "var u='{{APP}}?lang=en'")
en_html = re.sub(r'\{\{pic ([a-z\-]+) "([^"]+)"(?: (eager))?\}\}', pic, en_html)
en_html = en_html.replace('{{PLAYURL}}', PLAY).replace('{{APPSTORE}}', APPSTORE.replace('/br/app/', '/app/')).replace('{{PLAY}}', PLAY_LP.replace('utm_source%3Dlp', 'utm_source%3Dlp-en') + '&amp;hl=en').replace('{{APP}}', APP).replace('media/', '../media/').replace('https://movoapp.com.br/../media/', 'https://movoapp.com.br/media/')
for f in ('favicon.svg', 'favicon-32.png', 'apple-touch-icon.png'):
    en_html = en_html.replace(f'href="{f}"', f'href="../{f}"')
en_html = en_html.replace('</style>', '.coach-grid{grid-template-columns:1fr!important}@media(min-width:760px){.coach-grid .cb{display:grid;grid-template-columns:1fr 1fr;gap:12px}}\n</style>', 1)
os.makedirs('../en', exist_ok=True)
en_html = sem_play(en_html, 'en')
open('../en/index.html', 'w', encoding='utf-8').write(en_html)
print('en/index.html', len(en_html.encode()))
