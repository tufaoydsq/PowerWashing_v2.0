import re
from django.utils.deprecation import MiddlewareMixin


class AvisoLicencaMiddleware(MiddlewareMixin):
    """
    Middleware que injeta um aviso fixo, chamativo e persistente em TODAS
    as páginas do admin (não some ao trocar de página nem tem botão de
    fechar), lembrando de verificar o pagamento da licença anual do
    sistema (máquinas licenciadas e atualizações).

    Para desativar temporariamente o aviso (ex: assim que o pagamento for
    confirmado), basta comentar a linha do MIDDLEWARE no settings.py ou
    trocar EXIBIR_AVISO para False abaixo.
    """

    EXIBIR_AVISO = True
    PREFIXO_ADMIN = '/admin/'
    TEXTO_AVISO = (
        "⚠️ ATENÇÃO: verifique o pagamento da licença anual do sistema "
        "(máquinas licenciadas e atualizações) ⚠️"
    )

    AVISO_HTML = '''
<div id="aviso-licenca-anual" style="
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 99999;
    background: #d32f2f;
    color: #ffffff;
    text-align: center;
    font-weight: bold;
    padding: 10px 16px;
    font-family: -apple-system, Arial, sans-serif;
    font-size: 14px;
    letter-spacing: 0.3px;
    animation: piscar-aviso-licenca 1.4s infinite;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
">
    {texto}
</div>
<style>
    @keyframes piscar-aviso-licenca {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    body {{ padding-top: 44px !important; }}
</style>
'''

    def process_response(self, request, response):
        if not self.EXIBIR_AVISO:
            return response

        try:
            if not request.path.startswith(self.PREFIXO_ADMIN):
                return response

            user = getattr(request, 'user', None)
            if not user or not user.is_authenticated or not user.is_staff:
                return response

            content_type = response.get('Content-Type', '')
            if 'text/html' not in content_type:
                return response

            if not hasattr(response, 'content'):
                return response

            content = response.content.decode('utf-8')

            if 'aviso-licenca-anual' in content:
                return response

            aviso = self.AVISO_HTML.format(texto=self.TEXTO_AVISO)
            novo_conteudo, n = re.subn(
                r'(<body[^>]*>)', r'\1' + aviso.replace('\\', '\\\\'), content, count=1
            )

            if n:
                response.content = novo_conteudo.encode('utf-8')
                if 'Content-Length' in response:
                    response['Content-Length'] = str(len(response.content))
        except Exception:
            # Nunca deixa o aviso quebrar o carregamento normal da página
            pass

        return response
