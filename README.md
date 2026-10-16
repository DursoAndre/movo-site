# Movo: landing page

Site estático de https://movoapp.com.br (HTML/CSS/JS sem build).

- `index.html` é gerado por `_src/build.py` a partir de `_src/template.html` (rode `python3 _src/build.py` depois de editar o template).
- Os depoimentos da página são exemplos fictícios e ficam ocultos; só aparecem com `?depoimentos=1`. Trocar por reais (com autorização) antes de mostrar.
- O botão "Começar grátis" aponta para o endereço atual do app (`APP` em `_src/build.py`); trocar quando o app mudar de domínio.
- `privacidade.html` e `termos.html` são cópias das páginas do app.
