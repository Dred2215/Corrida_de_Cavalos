import random
import asyncio
import pygame
import menu

def main():
    pygame.init()

    # Defina as cores
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # Inicialize a tela
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Corrida de Cavalos")

    # Variáveis do jogo
    cavalos = {
        1: 0,
        2: 0,
        3: 0,
        4: 0
    }

    ordem_chegada = []
    posicao_atual = {cavalo: 0 for cavalo in cavalos.keys()}
    posicao_evento = 0
    numero_evento = 0
    evento_ativado = False

    

    # Variável para rastrear o estado das apostas
    global apostas_encerradas
    apostas_encerradas = False
    # Variável para controlar o estado da tela de apostas
    tela_apostas_ativa = False

    # Variável para rastrear o estado da corrida
    corrida_terminou = False

    # Variáveis para rastrear o evento
    evento_ocorrendo = False
    numero_sorteado_evento = 0
    numero_evento_ocorrendo = 0
    ultimo_numero_sorteado = None

    # Variável para rastrear os cavalos que receberam apostas
    cavalos_com_apostas = set()
    cavalos_ja_apostados = set()

    # Lista de retângulos dos botões de aposta
    global botoes_aposta1, botoes_aposta2
    botoes_aposta1 = []
    botoes_aposta2 = []

    # Adicione esta variável para rastrear o número de doses de cada cavalo
    doses_cavalos = {cavalo: 0 for cavalo in cavalos.keys()}

    

    # Função para a tela de apostas
    def tela_apostas():
        font = pygame.font.Font(None, 72)
        
        global tela_apostas_ativa, apostas_encerradas  # Declare as variáveis globais

        if apostas_encerradas:
            # Se as apostas já estiverem encerradas, não permita acessar a tela de apostas
            return

        # Variável para controlar o estado da tela de apostas
        tela_apostas_ativa = True

        # Retângulo do botão "Encerrar Apostas"
        encerrar_apostas_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 80)

        # Listas para rastrear cavalos que receberam apostas e os botões de aposta
        cavalos_apostados = []

        running_apostas = True
        while running_apostas:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_apostas = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, cavalo in enumerate(cavalos):
                        if botoes_aposta1[i].collidepoint(event.pos):
                            if cavalo not in cavalos_apostados:
                                print(f"Você apostou no Cavalo {cavalo} - Aposta 1")
                                cavalos_apostados.append(cavalo)
                                # Adicione 1 dose ao cavalo correspondente
                                doses_cavalos[cavalo] += 1
                            else:
                                print(f"O Cavalo {cavalo} já recebeu uma aposta. Escolha outro cavalo.")
                        elif botoes_aposta2[i].collidepoint(event.pos):
                            if cavalo not in cavalos_apostados:
                                print(f"Você apostou no Cavalo {cavalo} - Aposta 2")
                                cavalos_apostados.append(cavalo)
                                # Adicione 2 doses ao cavalo correspondente
                                doses_cavalos[cavalo] += 2
                            else:
                                print(f"O Cavalo {cavalo} já recebeu uma aposta. Escolha outro cavalo.")
                    if encerrar_apostas_rect.collidepoint(event.pos):
                        if len(cavalos_apostados) == len(cavalos):
                            tela_apostas_ativa = False
                            # Defina apostas_encerradas como True quando todas as apostas forem feitas
                            apostas_encerradas = True
                            print("Apostas encerradas:", apostas_encerradas)  # Adiciona o print aqui
                        else:
                            print("Aposte em todos os cavalos antes de encerrar as apostas.")

            # Desenhe a tela de apostas
            screen.fill(WHITE)

            # Desenhe os nomes dos cavalos e os botões de aposta ao lado de cada um
            for i, cavalo in enumerate(cavalos):
                if cavalo not in cavalos_apostados:
                    nome_cavalo_text = font.render(f"Cavalo {cavalo}", True, BLACK)
                    nome_cavalo_rect = nome_cavalo_text.get_rect(center=(SCREEN_WIDTH // 2.1, 140 + i * 120))
                    screen.blit(nome_cavalo_text, nome_cavalo_rect)

                    # Retângulos dos botões de aposta 1 e 2
                    botao_aposta1_rect = pygame.Rect(SCREEN_WIDTH // 2 + 100, 100 + i * 120, 80, 80)
                    botao_aposta2_rect = pygame.Rect(SCREEN_WIDTH // 2 + 220, 100 + i * 120, 80, 80)

                    # Adicione os retângulos à lista de botões de aposta
                    botoes_aposta1.append(botao_aposta1_rect)
                    botoes_aposta2.append(botao_aposta2_rect)

                    pygame.draw.rect(screen, RED, botao_aposta1_rect)
                    pygame.draw.rect(screen, RED, botao_aposta2_rect)

                    numero_text1 = font.render("1", True, WHITE)
                    numero_text_rect1 = numero_text1.get_rect(center=botao_aposta1_rect.center)
                    screen.blit(numero_text1, numero_text_rect1)

                    numero_text2 = font.render("2", True, WHITE)
                    numero_text_rect2 = numero_text2.get_rect(center=botao_aposta2_rect.center)
                    screen.blit(numero_text2, numero_text_rect2)

            # Desenhe o botão "Encerrar Apostas" na parte inferior da tela
            encerrar_apostas_rect = pygame.Rect(SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT - 100, 500, 50)

            # Desenhe o retângulo do botão "Encerrar Apostas" com a cor desejada
            pygame.draw.rect(screen, RED, encerrar_apostas_rect)

            # Renderize o texto "Encerrar Apostas" usando a fonte desejada
            encerrar_apostas_text = font.render("Encerrar Apostas", True, WHITE)

            # Centralize o texto no retângulo do botão
            encerrar_apostas_text_rect = encerrar_apostas_text.get_rect(center=encerrar_apostas_rect.center)

            # Desenhe o texto na tela
            screen.blit(encerrar_apostas_text, encerrar_apostas_text_rect)
            pygame.display.flip()

            # Verifique se a tela de apostas deve ser encerrada
            if not tela_apostas_ativa:
                return  # Retorna à tela principal

        # Quando sair da tela de apostas, retorne à tela principal
        return

    # Função para desenhar a tela
    def desenhar_tela():
        screen.fill(WHITE)

        if not corrida_terminou:
            # Desenhe os cavalos
            desenhar_cavalos()
            # Desenhe os botões
            desenhar_botao()
            desenhar_botao_apostas()
            # Exiba a mensagem do dado
            if evento_ocorrendo:
                exibir_mensagem_dado()
        else:
            # Tela de resultados
            desenhar_resultados()
            # Botão de reinício
            desenhar_botao_reinicio()

        pygame.display.flip()

    # Função para desenhar os cavalos
    def desenhar_cavalos():
        font = pygame.font.Font(None, 36)
        cavalos_disponiveis = [cavalo for cavalo in cavalos.keys() if cavalo not in ordem_chegada]
        for i, cavalo in enumerate(cavalos_disponiveis):
            retangulo = pygame.Rect(100, 100 + i * 120, 100 + posicao_atual[cavalo] * 80, 80)
            pygame.draw.rect(screen, RED, retangulo)
            numero_text = font.render(str(cavalo), True, BLACK)
            numero_text_rect = numero_text.get_rect(center=(retangulo.centerx, retangulo.centery - 60))
            screen.blit(numero_text, numero_text_rect)
            classificacao_posicao_text = font.render(f"({len(ordem_chegada) + 1}/{posicao_atual[cavalo]})", True, BLACK)
            classificacao_posicao_text_rect = classificacao_posicao_text.get_rect(center=(retangulo.centerx, retangulo.centery))
            screen.blit(classificacao_posicao_text, classificacao_posicao_text_rect)

    # Função para desenhar o botão "Dado"
    def desenhar_botao():
        font = pygame.font.Font(None, 36)
        botao_rect = pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, 500, 200, 80))
        text = font.render("Dado", True, WHITE)
        text_rect = text.get_rect(center=botao_rect.center)
        screen.blit(text, text_rect)
        
        # Exibir o último número sorteado acima do botão do dado
        if ultimo_numero_sorteado is not None:
            numero_sorteado_text = font.render(f"Dado Sorteou: {ultimo_numero_sorteado}", True, BLACK)
            numero_sorteado_rect = numero_sorteado_text.get_rect(center=(botao_rect.centerx, botao_rect.centery - 90))
            screen.blit(numero_sorteado_text, numero_sorteado_rect)

    # Função para desenhar o botão "Apostas"
    def desenhar_botao_apostas():
        font = pygame.font.Font(None, 36)
        botao_rect = pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, 600, 200, 80))
        text = font.render("Apostas", True, WHITE)
        text_rect = text.get_rect(center=botao_rect.center)
        screen.blit(text, text_rect)

    # Função para exibir a mensagem do dado quando o evento ocorrer
    def exibir_mensagem_dado():
        font = pygame.font.Font(None, 36)
        mensagem = f"DADO EVENTO: N° {numero_sorteado_evento}"
        mensagem_text = font.render(mensagem, True, RED)
        screen.blit(mensagem_text, (SCREEN_WIDTH - mensagem_text.get_width() - 700, 10))  

        if evento_ocorrendo:
            numero_evento_text = font.render(f"EVENTO ATIVADO: O cavalo {numero_sorteado_evento}, retrocede uma casa", True, RED)
            screen.blit(numero_evento_text, (SCREEN_WIDTH - numero_evento_text.get_width() - 510, 40))

    def distribuir_e_consumir_doses(ordem_chegada, doses_cavalos):
        if len(ordem_chegada) < 4:
            return doses_cavalos  # Não há classificação suficiente para distribuir/consumir doses

        primeiro_lugar = ordem_chegada[0]
        segundo_lugar = ordem_chegada[1]
        terceiro_lugar = ordem_chegada[2]
        quarto_lugar = ordem_chegada[3]

        # Distribuir doses com base na classificação final
        doses_cavalos[terceiro_lugar] += (doses_cavalos[primeiro_lugar] * 2)
        doses_cavalos[quarto_lugar] += (doses_cavalos[primeiro_lugar] * 2) + (doses_cavalos[segundo_lugar])

        # Consumir doses com base na classificação final
        doses_consumidas_terceiro = doses_cavalos[terceiro_lugar]
        doses_consumidas_quarto = doses_cavalos[quarto_lugar]

        # Atualizar o número de doses dos cavalos
        doses_cavalos[terceiro_lugar] = doses_consumidas_terceiro
        doses_cavalos[quarto_lugar] = doses_consumidas_quarto

        return doses_cavalos

    # Função para desenhar os resultados
    def desenhar_resultados():
        font = pygame.font.Font(None, 36)
        text = font.render("Resultados Finais", True, RED)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 10))
        
        ordem_chegada.sort(key=lambda cavalo: posicao_atual[cavalo])

        for i, cavalo in enumerate(ordem_chegada, start=1):
            nome_cavalo = f"Cavalo {cavalo}"
            classificacao = f"{i}º lugar"
            doses = f"Doses: {doses_cavalos[cavalo]}"
            
            if i <= 2:
                resultado_texto = f"{nome_cavalo}: {classificacao}, Doses: {0}"
                resultado_render = font.render(resultado_texto, True, RED)
                screen.blit(resultado_render, (SCREEN_WIDTH // 2 - resultado_render.get_width() // 2, 50 + i * 40))
            else:
                resultado_texto = f"{nome_cavalo}: {classificacao}, {doses}"
                resultado_render = font.render(resultado_texto, True, RED)
                screen.blit(resultado_render, (SCREEN_WIDTH // 2 - resultado_render.get_width() // 2, 50 + i * 40))


    # Função para desenhar o botão de reinício
    def desenhar_botao_reinicio():
        font = pygame.font.Font(None, 36)
        botao_rect = pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, 500, 200, 80))
        reiniciar_texto = font.render("Reiniciar", True, WHITE)
        text_rect = reiniciar_texto.get_rect(center=botao_rect.center)
        screen.blit(reiniciar_texto, text_rect)

    # Função para processar o evento de lançamento de dados
    def processar_lancamento_dados(doses_cavalos):
        nonlocal posicao_evento, numero_evento, evento_ativado, evento_ocorrendo, numero_sorteado_evento, numero_evento_ocorrendo, ultimo_numero_sorteado
        cavalos_disponiveis = [cavalo for cavalo in cavalos.keys() if cavalo not in ordem_chegada]
        
        # Verifique se TODOS os cavalos têm doses apostadas
        if any(doses_cavalos[cavalo] == 0 for cavalo in cavalos_disponiveis):
            print("Aposte pelo menos uma dose para TODOS os cavalos antes de girar o dado.")
            return
        
        numero_sorteado = random.choice(cavalos_disponiveis)
        print(f"O dado sorteou o número {numero_sorteado}")
        ultimo_numero_sorteado = numero_sorteado

        cavalo_sorteado = numero_sorteado
        posicao_atual[cavalo_sorteado] += 1

        for cavalo, posicao in posicao_atual.items():
            if posicao == 5 and cavalo not in ordem_chegada:
                ordem_chegada.append(cavalo)
                print(f"\nCavalo {cavalo} chegou em {len(ordem_chegada)}º lugar!")

        if all(posicao_atual[cavalo] >= posicao_evento + 1 for cavalo in cavalos) and not evento_ativado:
            cavalos_afetados = [c for c in list(cavalos.keys()) if c not in ordem_chegada]
            if cavalos_afetados:
                cavalo_retroceder = random.choice(cavalos_afetados)
                print(f"Evento {numero_evento}: Dado sorteou o número {cavalo_retroceder} - Cavalo {cavalo_retroceder} retrocede uma casa!")
                posicao_atual[cavalo_retroceder] -= 1
                evento_ativado = True
                evento_ocorrendo = True
                numero_sorteado_evento = cavalo_retroceder
                numero_evento_ocorrendo = numero_evento

        if evento_ativado and all(posicao_atual[cavalo] >= posicao_evento + 1 for cavalo in cavalos):
            posicao_evento += 1
            evento_ativado = False
            numero_evento += 1

        # Verificar se todos os cavalos completaram o percurso
        if all(posicao_atual[cavalo] >= 5 for cavalo in cavalos):
            nonlocal corrida_terminou
            corrida_terminou = True
            evento_ocorrendo = False

        # Chame a função para distribuir e consumir doses com base na ordem de chegada
        doses_cavalos = distribuir_e_consumir_doses(ordem_chegada, doses_cavalos)

    # Função para reiniciar o jogo
    def reiniciar_jogo():
        # nonlocal corrida_terminou, posicao_evento, numero_evento, evento_ativado, evento_ocorrendo, numero_sorteado_evento, numero_evento_ocorrendo, ultimo_numero_sorteado
        # corrida_terminou = False
        # posicao_evento = 0
        # numero_evento = 0
        # evento_ativado = False
        # evento_ocorrendo = False
        # numero_sorteado_evento = 0
        # numero_evento_ocorrendo = 0
        # ultimo_numero_sorteado = None
        # for cavalo in cavalos.keys():
        #     posicao_atual[cavalo] = 0
        #     doses_cavalos[cavalo] = 0  # Zere os contadores de doses
        # ordem_chegada.clear()
        # cavalos_ja_apostados.clear()
        # global tela_apostas_ativa  # Defina a variável global como False ao reiniciar
        # tela_apostas_ativa = False
        # global apostas_encerradas
        # apostas_encerradas = False
        menu.main()


    # Loop principal do jogo
    running = True
    tela_apostas_ativa = False  # Variável para controlar se a tela de apostas está ativa

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not corrida_terminou:
                if SCREEN_WIDTH // 2 - 100 <= event.pos[0] <= SCREEN_WIDTH // 2 + 100:
                    if 500 <= event.pos[1] <= 580:
                        if apostas_encerradas:
                            processar_lancamento_dados(doses_cavalos)
                            desenhar_tela()
                    elif 600 <= event.pos[1] <= 680 and not apostas_encerradas and not tela_apostas_ativa:
                        tela_apostas_ativa = True
            elif event.type == pygame.MOUSEBUTTONDOWN and corrida_terminou:
                if SCREEN_WIDTH // 2 - 100 <= event.pos[0] <= SCREEN_WIDTH // 2 + 100 and 500 <= event.pos[1] <= 580:
                    reiniciar_jogo()
                    desenhar_tela()

        if tela_apostas_ativa:
            tela_apostas()
            tela_apostas_ativa = False

        desenhar_tela()

        asyncio.sleep(0)
        if not running:
            pygame.quit()
            return

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
