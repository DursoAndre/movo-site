import re, os
APP = "https://app.movoapp.com.br/"
tpl = open('template.html', encoding='utf-8').read()
def pic(m):
    name, alt, mode = m.group(1), m.group(2), m.group(3) or 'lazy'
    attrs = 'fetchpriority="high"' if mode == 'eager' else 'loading="lazy" decoding="async"'
    sizes = '(min-width:1000px) 320px, 62vw'
    return (f'<picture><source type="image/avif" srcset="media/shot-{name}-360.avif 360w, media/shot-{name}-720.avif 720w" sizes="{sizes}">'
            f'<source type="image/webp" srcset="media/shot-{name}-360.webp 360w, media/shot-{name}-720.webp 720w" sizes="{sizes}">'
            f'<img src="media/shot-{name}-720.webp" width="720" height="1558" alt="{alt}" {attrs}></picture>')
tpl = re.sub(r'\{\{pic ([a-z\-]+) "([^"]+)"(?: (eager))?\}\}', pic, tpl)
tpl = tpl.replace('{{APP}}', APP)
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
en_html = en_html.replace('{{APP}}', APP).replace('media/', '../media/').replace('https://movoapp.com.br/../media/', 'https://movoapp.com.br/media/')
for f in ('favicon.svg', 'favicon-32.png', 'apple-touch-icon.png'):
    en_html = en_html.replace(f'href="{f}"', f'href="../{f}"')
en_html = en_html.replace('</style>', '.coach-grid{grid-template-columns:1fr!important}@media(min-width:760px){.coach-grid .cb{display:grid;grid-template-columns:1fr 1fr;gap:12px}}\n</style>', 1)
os.makedirs('../en', exist_ok=True)
open('../en/index.html', 'w', encoding='utf-8').write(en_html)
print('en/index.html', len(en_html.encode()))
