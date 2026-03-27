from utils.questions.int_question import int_question
from utils.questions.select_question import select_question
import string
import logging
from datetime import datetime
from pathlib import Path


# ================= LOG =================
def configurar_log(debug=False):
    dt_agora = datetime.now()

    base_dir = Path("logs") / dt_agora.strftime("%Y/%m/%d")
    file_path = base_dir / f"{dt_agora.strftime('%H-%M-%S')}.log"

    base_dir.mkdir(parents=True, exist_ok=True)

    formato = "%(asctime)s - %(levelname)s - %(message)s"

    nivel = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=nivel,
        format=formato,
        handlers=[
            logging.FileHandler(file_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    return logging.getLogger(__name__)


def log_debug(log, mensagem, nivel=0):
    indent = "  " * nivel
    log.debug(f"{indent}{mensagem}")


# ================= INPUT =================
def faz_perguntas(log):
    qtd_linhas = int_question(
        content="Quantas linhas você quer (padrão: 3, minimo: 3):",
        allowed_values={"min": 3},
        default_value=3,
        invalid_message="Valor inválido.",
    )

    qtd_colunas = int_question(
        content="Quantas colunas você quer (padrão: 3, minimo: 3):",
        allowed_values={"min": 3},
        default_value=3,
        invalid_message="Valor inválido.",
    )

    qtd_rainhas = int_question(
        content="Quantas rainhas para testar (padrão: 1, minimo: 1):",
        allowed_values={"min": 1},
        default_value=1,
        invalid_message="Valor inválido.",
    )

    log.info(
        f"Configuração: linhas={qtd_linhas}, colunas={qtd_colunas}, rainhas={qtd_rainhas}"
    )
    return qtd_linhas, qtd_colunas, qtd_rainhas


# ================= TABULEIRO =================
def criar_tabuleiro(qtd_linhas, qtd_colunas):
    return [["-" for _ in range(qtd_colunas)] for _ in range(qtd_linhas)]


def mostrar_tabuleiro(tabuleiro, qtd_colunas, log):
    letras = list(string.ascii_uppercase)

    header = "   " + " ".join(letras[:qtd_colunas])
    log.info(header)

    for i, linha in enumerate(tabuleiro, start=1):
        log.info(f"{i:2} " + " ".join(linha))

    log.info("")


# ================= REGRAS =================
def verifica_colisao_linha(tabuleiro, linha):
    return "R" not in tabuleiro[linha]


def verifica_colisao_coluna(tabuleiro, coluna):
    valores_coluna = [linha[coluna] for linha in tabuleiro]
    return "R" not in valores_coluna


def verifica_colisao_diagonal(rainhas_posicionadas, linha, coluna):
    for r_linha, r_coluna in rainhas_posicionadas:
        if abs(r_linha - linha) == abs(r_coluna - coluna):
            return False
    return True


def pode_posicionar(tabuleiro, rainhas_posicionadas, linha, coluna, log, nivel):
    if tabuleiro[linha][coluna] != "-":
        log_debug(log, f"❌ Ocupado ({linha+1},{coluna+1})", nivel)
        return False

    if not verifica_colisao_linha(tabuleiro, linha):
        log_debug(log, f"❌ Falha linha {linha+1}", nivel)
        return False

    if not verifica_colisao_coluna(tabuleiro, coluna):
        log_debug(log, f"❌ Falha coluna {coluna+1}", nivel)
        return False

    if not verifica_colisao_diagonal(rainhas_posicionadas, linha, coluna):
        log_debug(log, f"❌ Falha diagonal ({linha+1},{coluna+1})", nivel)
        return False

    log_debug(log, f"✅ Válido ({linha+1},{coluna+1})", nivel)
    return True


# ================= BACKTRACK =================
def posicionar_rainhas(
    tabuleiro, qtd_linhas, qtd_colunas, qtd_rainhas, log, buscar_todas
):
    resultados = []
    resultados_set = set()

    def backtracking(nivel, rainhas_posicionadas):
        log_debug(log, f"🔍 Nível {nivel+1} iniciado", nivel)

        if len(rainhas_posicionadas) == qtd_rainhas:
            combinacao = tuple(sorted(rainhas_posicionadas))

            if combinacao not in resultados_set:
                log.info(
                    f"✔ Solução encontrada {str(len(resultados)+1).rjust(3, '0')}: {rainhas_posicionadas}"
                )
                resultados_set.add(combinacao)
                resultados.append(list(combinacao))

            if not buscar_todas:
                return True

            return False

        for linha in range(qtd_linhas):
            for coluna in range(qtd_colunas):

                if pode_posicionar(
                    tabuleiro,
                    rainhas_posicionadas,
                    linha,
                    coluna,
                    log,
                    nivel,
                ):
                    tabuleiro[linha][coluna] = "R"
                    rainhas_posicionadas.append((linha, coluna))

                    parar = backtracking(nivel + 1, rainhas_posicionadas)

                    if parar:
                        return True

                    tabuleiro[linha][coluna] = "-"
                    rainhas_posicionadas.pop()

        return False

    backtracking(0, [])
    return resultados


# ================= RESULTADOS =================
def mostrar_resultados(resultados, qtd_linhas, qtd_colunas, log):
    for indice, combinacao in enumerate(resultados, start=1):
        resultado = []
        tabuleiro = [["-" for _ in range(qtd_colunas)] for _ in range(qtd_linhas)]
        letras = list(string.ascii_uppercase)

        for linha, coluna in combinacao:
            tabuleiro[linha][coluna] = "R"
            # resultado = resultado + [(linha + 1, coluna + 1)]
            resultado = resultado + [f"{letras[coluna]}{linha+1}"]
        # log.info(f"\n=== Combinação {indice} : {resultado} ===")
        log.info(f"\n=== Combinação {str(indice).rjust(3, '0')} : {resultado} ===")

        header = "- " + " ".join(letras[:qtd_colunas])
        log.info(header)

        for i, linha in enumerate(tabuleiro, start=1):
            log.info(f"{i} {' '.join(linha)}")


# ================= MAIN =================
def main():
    modo_debug = select_question(
        content="Modo debug completo? (s/n, padrão:n): ",
        allowed_values=["s", "n"],
        default_value="n",
        invalid_message="Opção invalida!.",
    )
    modo_procurar_combinações = select_question(
        content="Deseja procurar todas as combinações ou só a primeira? (s = todas / n = só 1, padrão:n): ",
        allowed_values=["s", "n"],
        default_value="n",
        invalid_message="Opção invalida!.",
    )
    log = configurar_log(debug=(modo_debug == "s"))

    qtd_linhas, qtd_colunas, qtd_rainhas = faz_perguntas(log)

    tabuleiro = criar_tabuleiro(qtd_linhas, qtd_colunas)

    log.info("Tabuleiro inicial:")
    mostrar_tabuleiro(tabuleiro, qtd_colunas, log)

    resultados = posicionar_rainhas(
        tabuleiro,
        qtd_linhas,
        qtd_colunas,
        qtd_rainhas,
        log,
        buscar_todas=(modo_procurar_combinações == "s"),
    )

    log.info(f"\nTotal de combinações: {len(resultados)}")

    mostrar_resultados(resultados, qtd_linhas, qtd_colunas, log)

    log.info("Execução finalizada.")


if __name__ == "__main__":
    main()
