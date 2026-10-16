import re, os
APP = "https://dursoandre.github.io/meu-treino/"
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
