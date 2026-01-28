import imaplib
import email
import os
from email.header import decode_header

# ========= CONFIGURA ==========
EMAIL = "sf.contasdeconsumo@barueri.sp.gov.br"
SENHA = "Contab.23@"
IMAP_SERVER = "mail.barueri.sp.gov.br"

REMETENTE_ENEL = "brasil.enel.com"
PASTA_DOWNLOAD = "faturas_enel"
# ==============================

os.makedirs(PASTA_DOWNLOAD, exist_ok=True)

def decodificar(texto):
    partes = decode_header(texto)
    resultado = ""
    for parte, enc in partes:
        if isinstance(parte, bytes):
            resultado += parte.decode(enc or "utf-8", errors="ignore")
        else:
            resultado += parte
    return resultado

print("🔌 Conectando ao Zimbra...")

mail = imaplib.IMAP4_SSL(IMAP_SERVER, 993)
mail.login(EMAIL, SENHA)
mail.select("INBOX")

print("📩 Buscando e-mails...")

status, mensagens = mail.search(None, 'ALL')

for num in mensagens[0].split():
    status, dados = mail.fetch(num, "(RFC822)")
    msg = email.message_from_bytes(dados[0][1])

    remetente = msg.get("From", "").lower()
    print("DEBUG remetente:", remetente)

    if REMETENTE_ENEL in remetente:

        for parte in msg.walk():
            content_type = parte.get_content_type()

            if content_type == "application/pdf":
                nome = parte.get_filename()

                if nome:
                    nome = decodificar(nome)
                else:
                    nome = f"fatura_enel_{num.decode()}.pdf"

                caminho = os.path.join(PASTA_DOWNLOAD, nome)

                if not os.path.exists(caminho):

                    with open(caminho, "wb") as f:
                        f.write(parte.get_payload(decode=True))
                    print("✅ Baixado:", nome)
                else:
                    print("⏭️ Já existe:", nome)

mail.logout()
print("🏁 Finalizado.")

