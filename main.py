import secrets
import string

# --- CONFIGURAÇÕES ---
SIMBOLOS_SEGUROS = "!@#$%&*()-_=+[]{}"

def gerar_senha(
    tamanho: int = 16,
    usar_maiusculas: bool = True,
    usar_minusculas: bool = True,
    usar_numeros: bool = True,
    usar_simbolos: bool = True
) -> str:
    """
    Gera uma senha segura e aleatória com base nos critérios fornecidos.
    """
    if not (8 <= tamanho <= 64):
        raise ValueError("A senha deve ter entre 8 e 64 caracteres.")

    # Mapeamento de tipos de caracteres para facilitar a lógica
    opcoes = [
        (usar_maiusculas, string.ascii_uppercase),
        (usar_minusculas, string.ascii_lowercase),
        (usar_numeros, string.digits),
        (usar_simbolos, SIMBOLOS_SEGUROS)
    ]

    caracteres_disponiveis = ""
    senha = []

    # Garante pelo menos um caractere de cada tipo selecionado (Segurança extra!)
    for ativo, grupo in opcoes:
        if ativo:
            caracteres_disponiveis += grupo
            senha.append(secrets.choice(grupo))

    if not caracteres_disponiveis:
        raise ValueError("Pelo menos um tipo de caractere deve ser selecionado.")

    # Preenche o restante do tamanho solicitado
    for _ in range(tamanho - len(senha)):
        senha.append(secrets.choice(caracteres_disponiveis))

    # Embaralha a lista para que os primeiros caracteres não sejam previsíveis
    secrets.SystemRandom().shuffle(senha)

    return ''.join(senha)

def obter_confirmacao(mensagem: str) -> bool:
    """Função auxiliar para validar entradas de Sim ou Não."""
    while True:
        resposta = input(f"{mensagem} (S/N): ").strip().lower()
        if resposta in ('s', 'n'):
            return resposta == 's'
        print("\033[1;91mResposta inválida. Por favor, digite S ou N.\033[0m")

def main():
    print("\n" + "🔐" + " Gerador de Senhas Seguras ".center(40, "═"))
    
    while True:
        # 1. Definição do Tamanho
        try:
            entrada = input("\nQual o tamanho da senha? (8-64, padrão 16): ").strip()
            tamanho = int(entrada) if entrada else 16
            
            if not (8 <= tamanho <= 64):
                print("\033[1;91mErro: O tamanho deve estar entre 8 e 64 caracteres.\033[0m")
                continue
        except ValueError:
            print("\033[1;91mErro: Digite um número válido para o tamanho.\033[0m")
            continue

        # 2. Configuração dos Filtros
        u_maius = obter_confirmacao("Incluir letras MAIÚSCULAS?")
        u_minus = obter_confirmacao("Incluir letras minúsculas?")
        u_num   = obter_confirmacao("Incluir números?")
        u_simb  = obter_confirmacao("Incluir símbolos?")

        if not any([u_maius, u_minus, u_num, u_simb]):
            print("\n\033[1;91mErro: Você deve selecionar pelo menos um tipo de caractere!\033[0m")
            continue

        # 3. Geração e Exibição
        senha_final = gerar_senha(tamanho, u_maius, u_minus, u_num, u_simb)
        
        print("\n" + "─" * 80)
        print(f"Senha Gerada: \033[1;92m{senha_final}\033[0m")
        print("─" * 80)

        # 4. Opção de Reiniciar
        if not obter_confirmacao("\nDeseja gerar outra senha?"):
            print("\n\033[1;94mEncerrando... Mantenha suas contas seguras! 🛡️\033[0m")
            break

if __name__ == "__main__":
    main()
