import pygame, sys
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((800, 600))
pygame.display.set_caption('외대탈출')

# 배경 이미지 불러오기
background = pygame.image.load(
    r"C:\Users\seobi\OneDrive\Desktop\외대탈출\start_background.png"
)

# 화면 크기에 맞게 이미지 조절
background = pygame.transform.scale(background, (800, 600))

# 폰트 설정
font = pygame.font.Font(
    r"C:\Users\seobi\OneDrive\Desktop\외대탈출\PressStart2P-Regular.ttf",
    20
)

game_font = pygame.font.Font(
    r"C:\Users\seobi\OneDrive\Desktop\외대탈출\PressStart2P-Regular.ttf",
    40
)

title_font = pygame.font.Font(
    r"C:\Users\seobi\OneDrive\Desktop\외대탈출\Galmuri11-Bold.ttf",
    90
)

# 현재 화면 상태
scene = "start"

clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # 시작 화면에서 마우스 클릭 시 게임 시작
        if scene == "start":
            if event.type == MOUSEBUTTONDOWN:
                scene = "game"

    # 시작 화면
    if scene == "start":

        # 배경 출력
        DISPLAYSURF.blit(background, (0, 0))

        # 현재 시간
        current_time = pygame.time.get_ticks()

        # 0.5초마다 깜빡임
        if (current_time // 500) % 2 == 0:

            text = font.render(
                ">> PRESS THE MOUSE BUTTON <<",
                True,
                (255, 255, 255)
            )

            text_rect = text.get_rect(center=(380, 520))

            DISPLAYSURF.blit(text, text_rect)

        # 게임 제목
        title_text = title_font.render("외대탈출",True,(0, 0, 128))

        title_rect = title_text.get_rect(center=(400, 140))

        DISPLAYSURF.blit(title_text, title_rect)
        

    # 게임 화면
    elif scene == "game":

        DISPLAYSURF.fill((0, 0, 0))

        game_text = game_font.render(
            "GAME START",
            True,
            (255, 255, 255)
        )

        game_rect = game_text.get_rect(center=(400, 300))

        DISPLAYSURF.blit(game_text, game_rect)

    pygame.display.update()
    clock.tick(60)