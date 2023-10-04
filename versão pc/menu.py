import asyncio
import pygame
import CorridaCavalo_facil
import CorridaCavalo_dificil

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

    def desenhar_tela():
            screen.fill(WHITE)

            
            # Desenhe os botões
            desenhar_botao()
            desenhar_botao_apostas()
            # Exiba a mensagem do dado
               
           
            pygame.display.flip()



    # Função para desenhar o botão "Dado"
    def desenhar_botao():
        font = pygame.font.Font(None, 36)
        botao_rect = pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, 500, 200, 80))
        text = font.render("facil", True, WHITE)
        text_rect = text.get_rect(center=botao_rect.center)
        screen.blit(text, text_rect)
        


    # Função para desenhar o botão "Apostas"
    def desenhar_botao_apostas():
        font = pygame.font.Font(None, 36)
        botao_rect = pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, 600, 200, 80))
        text = font.render("dificil", True, WHITE)
        text_rect = text.get_rect(center=botao_rect.center)
        screen.blit(text, text_rect)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if SCREEN_WIDTH // 2 - 100 <= event.pos[0] <= SCREEN_WIDTH // 2 + 100:
                    if 500 <= event.pos[1] <= 580:
                        CorridaCavalo_facil.main()
                    elif 600 <= event.pos[1] <= 680:
                        CorridaCavalo_dificil.main()



        desenhar_tela()

        asyncio.sleep(0)
        if not running:
            pygame.quit()
            return

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())