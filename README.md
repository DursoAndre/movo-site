# Movo: landing page

Site estático de https://movoapp.com.br (HTML/CSS/JS sem build).

- `index.html` é gerado por `_src/build.py` a partir de `_src/template.html` (rode `python3 _src/build.py` depois de editar o template).
- Os depoimentos da página são exemplos fictícios e ficam ocultos; só aparecem com `?depoimentos=1`. Trocar por reais (com autorização) antes de mostrar.
- O botão "Começar grátis" aponta para o endereço atual do app (`APP` em `_src/build.py`); trocar quando o app mudar de domínio.
- `privacidade.html` e `termos.html` são cópias das páginas do app.

## Links universais (.well-known)

- `.well-known/assetlinks.json` (Android) e `.well-known/apple-app-site-association` (iPhone) fazem os links `https://movoapp.com.br/convite/...` abrirem o app. O `.nojekyll` na raiz faz o GitHub Pages servir a pasta `.well-known`.
- Team ID da conta Apple Developer: `NJ86VHJQ47` (appID `NJ86VHJQ47.br.com.movoapp.app`), preenchido em 10/11/2026.
- O arquivo não tem extensão; o GitHub Pages o serve como `application/octet-stream`. A Apple aceita (lê o JSON mesmo assim), mas fica registrado. Deve responder 200 direto, sem redirecionamento. Depois de publicar, conferir com `curl -sI https://movoapp.com.br/.well-known/apple-app-site-association`.
- A Apple guarda o arquivo em cache pela CDN dela; mudanças podem levar horas para valer no aparelho.
