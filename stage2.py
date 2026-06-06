import pygame
import sys
from pygame.locals import *

def run(DISPLAYSURF, clock, selected_gender):
    # =========================
    # 화면 설정
    # =========================
    WIDTH = 800
    HEIGHT = 600
    pygame.display.set_caption("외대탈출 ROUND 2")

    # =========================
    # 폰트
    # =========================
    font = pygame.font.Font("font/Galmuri11-Bold.ttf", 35)

    # =========================
    # 이미지 불러오기
    # =========================
    closed_bg = pygame.image.load("image/hall_1.png").convert()
    closed_bg = pygame.transform.scale(closed_bg, (WIDTH, HEIGHT))

    open_bg = pygame.image.load("image/hall_2.png").convert()
    open_bg = pygame.transform.scale(open_bg, (WIDTH, HEIGHT))

    # ★ 게임오버 이미지 (단일 이미지로 수정)
    gameover_img = pygame.image.load("image/Stage2_fail.png").convert()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    male_run1 = pygame.image.load("image/male_run.png").convert_alpha()
    male_run2 = pygame.image.load("image/male_run2.png").convert_alpha()
    male_run1 = pygame.transform.scale(male_run1, (100,100))
    male_run2 = pygame.transform.scale(male_run2, (100,100))

    female_run1 = pygame.image.load("image/female_run.png").convert_alpha()
    female_run2 = pygame.image.load("image/female_run2.png").convert_alpha()
    female_run1 = pygame.transform.scale(female_run1, (100,100))
    female_run2 = pygame.transform.scale(female_run2, (100,100))

    # =========================
    # 변수
    # =========================
    scene = "game"
    frame_index = 0
    animation_timer = 0
    animation_speed = 200

    player_x = 80
    player_y = 520
    elevator_open = False
    gameover_timer = 0

    elevator_rect = pygame.Rect(420, 135, 130, 180)
    stairs_rect = pygame.Rect(620, 100, 145, 190)

    pygame.mouse.set_pos((80,520))

    # =========================
    # 게임 루프
    # =========================
    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if scene == "gameover":
                if event.type == KEYDOWN:
                    scene = "game"
                    elevator_open = False
                    gameover_timer = 0
                    pygame.mouse.set_pos((80,520))

        pygame.mouse.set_visible(False)

        mx, my = pygame.mouse.get_pos()
        player_x = mx
        player_y = my

        player_rect = pygame.Rect(player_x - 20, player_y - 20, 40, 40)

        if scene == "game":
            if player_rect.colliderect(elevator_rect):
                elevator_open = True

            if not elevator_open:
                if player_rect.colliderect(stairs_rect):
                    return "stage3"

            if elevator_open:
                DISPLAYSURF.blit(open_bg, (0,0))
                gameover_timer += dt
                if gameover_timer >= 2000:
                    scene = "gameover"
            else:
                DISPLAYSURF.blit(closed_bg, (0,0))

            hint_text = font.render("엘레베이터를 타볼까?", True, (255, 0, 0))
            hint_rect = hint_text.get_rect(center=(400, 40))
            DISPLAYSURF.blit(hint_text, hint_rect)

            animation_timer += dt
            if animation_timer >= animation_speed:
                animation_timer = 0
                if frame_index == 0: frame_index = 1
                else: frame_index = 0

            if selected_gender == "male":
                if frame_index == 0: player_img = male_run1
                else: player_img = male_run2
            elif selected_gender == "female":
                if frame_index == 0: player_img = female_run1
                else: player_img = female_run2

            DISPLAYSURF.blit(player_img, (player_x - 50, player_y - 50))

        elif scene == "gameover":
            # ★ 단일 이미지 출력
            DISPLAYSURF.blit(gameover_img, (0,0))
                
            gameover_text = font.render("PRESS ANY KEY TO RETRY", True, (0,0,0))
            text_rect = gameover_text.get_rect(center=(400,520))
            DISPLAYSURF.blit(gameover_text, text_rect)

        pygame.display.update()
