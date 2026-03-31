from utils.questions.int_question import int_question
from utils.questions.select_question import select_question
import string
import logging
from datetime import datetime
from pathlib import Path
import time  # ⏱️ controle de tempo


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


def debug(log, nivel, msg):
    """Evita custo de log quando não está em DEBUG"""
    if log.isEnabledFor(logging.DEBUG):
        log_debug(log, msg, nivel)


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
    """Cria matriz vazia"""
    return [["-" for _ in range(qtd_colunas)] for _ in range(qtd_linhas)]


def mostrar_tabuleiro(tabuleiro, qtd_colunas, log):
    """Mostra o tabuleiro formatado"""
    letras = list(string.ascii_uppercase)

    header = "   " + " ".join(letras[:qtd_colunas])
    log.info(header)

    for i, linha in enumerate(tabuleiro, start=1):
        log.info(f"{i:2} " + " ".join(linha))

    log.info("")


# ================= BACKTRACKING =================
def posicionar_rainhas(
    tabuleiro, qtd_linhas, qtd_colunas, qtd_rainhas, log, buscar_todas
):
    """
    Resolve o problema usando BACKTRACKING.

    Estratégia:
    - Tenta colocar uma rainha por linha
    - Usa sets para validar em O(1):
        - colunas usadas
        - diagonais
    """

    resultados = []
    resultados_set = set()

    # 🔥 Estruturas para validação rápida (O(1))
    colunas_usadas = set()
    diag1 = set()  # linha - coluna
    diag2 = set()  # linha + coluna

    def salvar_resultado(rainhas_posicionadas):
        """Evita duplicidade e salva solução"""
        combinacao = tuple(sorted(rainhas_posicionadas))
        if combinacao not in resultados_set:
            log.info(
                f"✔ Solução encontrada {str(len(resultados)+1).rjust(3, '0')}: {rainhas_posicionadas}"
            )
            resultados_set.add(combinacao)
            resultados.append(list(combinacao))

    def pode_posicionar(linha, coluna, nivel):
        """
        Verifica se posição é válida:
        - coluna livre
        - diagonais livres
        """
        if coluna in colunas_usadas:
            debug(log, nivel, f"❌ Coluna ocupada ({linha+1},{coluna+1})")
            return False

        if (linha - coluna) in diag1:
            debug(log, nivel, f"❌ Diagonal ↘ ocupada ({linha+1},{coluna+1})")
            return False

        if (linha + coluna) in diag2:
            debug(log, nivel, f"❌ Diagonal ↗ ocupada ({linha+1},{coluna+1})")
            return False

        debug(log, nivel, f"✅ Válido ({linha+1},{coluna+1})")
        return True

    def colocar(linha, coluna, rainhas_posicionadas, nivel):
        """Coloca rainha e atualiza estado"""
        debug(log, nivel, f"👑 Colocando ({linha+1},{coluna+1})")

        tabuleiro[linha][coluna] = "R"
        rainhas_posicionadas.append((linha, coluna))
        colunas_usadas.add(coluna)
        diag1.add(linha - coluna)
        diag2.add(linha + coluna)

    def remover(linha, coluna, rainhas_posicionadas, nivel):
        """Remove rainha (backtracking)"""
        debug(log, nivel, f"↩ Removendo ({linha+1},{coluna+1})")

        tabuleiro[linha][coluna] = "-"
        rainhas_posicionadas.pop()
        colunas_usadas.remove(coluna)
        diag1.remove(linha - coluna)
        diag2.remove(linha + coluna)

    def backtracking(linha, rainhas_posicionadas, nivel):
        """Função recursiva principal"""
        debug(log, nivel, f"🔍 Nível {nivel+1}")

        # 🎯 condição de parada
        if len(rainhas_posicionadas) == qtd_rainhas:
            salvar_resultado(rainhas_posicionadas)
            return not buscar_todas

        if linha >= qtd_linhas:
            return False

        for coluna in range(qtd_colunas):
            debug(log, nivel, f"➡ Tentando ({linha+1},{coluna+1})")

            if not pode_posicionar(linha, coluna, nivel):
                continue

            colocar(linha, coluna, rainhas_posicionadas, nivel)

            if backtracking(linha + 1, rainhas_posicionadas, nivel + 1):
                return True

            remover(linha, coluna, rainhas_posicionadas, nivel)

        return False

    backtracking(0, [], 0)
    return resultados


# ================= RESULTADOS =================
def mostrar_resultados(resultados, qtd_linhas, qtd_colunas, log):
    letras = list(string.ascii_uppercase)

    for indice, combinacao in enumerate(resultados, start=1):
        tabuleiro = [["-" for _ in range(qtd_colunas)] for _ in range(qtd_linhas)]
        resultado = []

        for linha, coluna in combinacao:
            tabuleiro[linha][coluna] = "R"
            resultado.append(f"{letras[coluna]}{linha+1}")

        log.info(f"\n=== Combinação {str(indice).rjust(3, '0')} : {resultado} ===")

        header = "- " + " ".join(letras[:qtd_colunas])
        log.info(header)

        for i, linha in enumerate(tabuleiro, start=1):
            log.info(f"{i} {' '.join(linha)}")


# ================= MAIN =================
def main():
    modo_debug = select_question(
        content="Modo debug completo? (s/n, padrão:n):",
        allowed_values=["s", "n"],
        default_value="n",
        invalid_message="Opção invalida!.",
    )

    modo_procurar = select_question(
        content="Deseja todas combinações? (s/n, padrão:n):",
        allowed_values=["s", "n"],
        default_value="n",
        invalid_message="Opção invalida!.",
    )

    log = configurar_log(debug=(modo_debug == "s"))

    qtd_linhas, qtd_colunas, qtd_rainhas = faz_perguntas(log)

    tabuleiro = criar_tabuleiro(qtd_linhas, qtd_colunas)

    log.info("Tabuleiro inicial:")
    mostrar_tabuleiro(tabuleiro, qtd_colunas, log)

    # ⏱️ INÍCIO DO TEMPO
    inicio = time.perf_counter()

    resultados = posicionar_rainhas(
        tabuleiro,
        qtd_linhas,
        qtd_colunas,
        qtd_rainhas,
        log,
        buscar_todas=(modo_procurar == "s"),
    )

    # ⏱️ FIM DO TEMPO
    fim = time.perf_counter()

    log.info(f"\nTotal de combinações: {len(resultados)}")
    log.info(f"⏱️ Tempo de execução: {fim - inicio:.6f} segundos")

    mostrar_resultados(resultados, qtd_linhas, qtd_colunas, log)

    log.info("Execução finalizada.")


if __name__ == "__main__":
    main()
