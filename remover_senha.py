import os
from pypdf import PdfReader, PdfWriter

# ===== CONFIGURAÇÕES =====
PASTA_ENTRADA = "pdf_com_senha"
PASTA_SAIDA = "pdf_sem_senha"
SENHA_PDF = "46523"
# =========================

def remover_senha_pdf(caminho_entrada, caminho_saida, senha):
    try:
        reader = PdfReader(caminho_entrada)

        if reader.is_encrypted:
            resultado = reader.decrypt(senha)
            if resultado == 0:
                print(f"❌ Senha incorreta: {os.path.basename(caminho_entrada)}")
                return

        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        with open(caminho_saida, "wb") as f:
            writer.write(f)

        print(f"✅ Desbloqueado: {os.path.basename(caminho_entrada)}")

    except Exception as e:
        print(f"❌ Erro em {os.path.basename(caminho_entrada)} → {e}")


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    if not os.path.exists(PASTA_ENTRADA):
        print(f"❌ Pasta '{PASTA_ENTRADA}' não existe.")
        return

    arquivos = [f for f in os.listdir(PASTA_ENTRADA) if f.lower().endswith(".pdf")]

    if not arquivos:
        print("⚠️ Nenhum PDF encontrado na pasta.")
        return

    for arquivo in arquivos:
        entrada = os.path.join(PASTA_ENTRADA, arquivo)
        saida = os.path.join(PASTA_SAIDA, arquivo)

        remover_senha_pdf(entrada, saida, SENHA_PDF)

    print("\n🎉 Processo finalizado!")


if __name__ == "__main__":
    main()
