import pygame
import sys
from pygame.locals import *

def run(DISPLAYSURF, clock, selected_gender):
    # =========================
    # 화면 설정
    # =========================
    WIDTH = 800
    HEIGHT = 600
    pygame.display.set_caption("외대탈출 ROUND 3")

    # =========================
    # 폰트 & 반투명 레이어 설정
    # =========================
    font = pygame.font.Font("font/Galmuri11-Bold.ttf", 35)
    light_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    YELLOW_ALPHA = (255, 255, 0, 100) 

    # =========================
    # 이미지 불러오기
    # =========================
    background = pygame.image.load("image/stage3_bg.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    cctv_img = pygame.image.load("image/CCTV.png").convert_alpha()
    cctv_img = pygame.transform.scale(cctv_img, (80, 80))

    # ★ 게임오버 이미지 (성별 분리)
    gameover_img_male = pygame.image.load("image/stage3_fail_male.jpg").convert()
    gameover_img_male = pygame.transform.scale(gameover_img_male, (WIDTH, HEIGHT))

    gameover_img_female = pygame.image.load("image/stage3_fail_female.jpg").convert()
    gameover_img_female = pygame.transform.scale(gameover_img_female, (WIDTH, HEIGHT))

    male_run1 = pygame.image.load("image/male_run.png").convert_alpha()
    male_run2 = pygame.image.load("image/male_run2.png").convert_alpha()
    female_run1 = pygame.image.load("image/female_run.png").convert_alpha()
    female_run2 = pygame.image.load("image/female_run2.png").convert_alpha()

    male_run1 = pygame.transform.scale(male_run1, (100,100))
    male_run2 = pygame.transform.scale(male_run2, (100,100))
    female_run1 = pygame.transform.scale(female_run1, (100,100))
    female_run2 = pygame.transform.scale(female_run2, (100,100))

    # =========================
    # 변수 설정
    # =========================
    scene = "game"
    frame_index = 0
    animation_timer = 0
    animation_speed = 200

    start_x = WIDTH - 60
    start_y = HEIGHT - 60
    game_started = False

    cctv_y = 60
    cctv1_x, cctv1_timer, cctv1_is_on = 40, 0, False
    CCTV1_OFF_TIME, CCTV1_ON_TIME = 300, 800   

    cctv2_x, cctv2_timer, cctv2_is_on = 260, 0, False
    CCTV2_OFF_TIME, CCTV2_ON_TIME = 400, 500   

    cctv3_x, cctv3_timer, cctv3_is_on = 480, 0, False
    CCTV3_OFF_TIME, CCTV3_ON_TIME = 1500, 1500    

    cctv4_x, cctv4_timer, cctv4_is_on = 700, 0, False
    CCTV4_OFF_TIME, CCTV4_ON_TIME = 400, 500    

    door_rect = pygame.Rect(130, 180, 150, 160)
    light1_rect = pygame.Rect(cctv1_x - 60, cctv_y + 60, 200, 480) 
    light2_rect = pygame.Rect(cctv2_x - 60, cctv_y + 60, 200, 480)
    light3_rect = pygame.Rect(cctv3_x - 60, cctv_y + 60, 200, 480)
    light4_rect = pygame.Rect(cctv4_x - 60, cctv_y + 60, 200, 360)

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
                    game_started = False
                    cctv1_timer = cctv2_timer = cctv3_timer = cctv4_timer = 0
                    cctv1_is_on = cctv2_is_on = cctv3_is_on = cctv4_is_on = False

        pygame.mouse.set_visible(False)
        mx, my = pygame.mouse.get_pos()
        player_rect = pygame.Rect(mx - 20, my - 20, 40, 40)

        if scene == "game":
            if not game_started:
                pygame.mouse.set_pos((start_x, start_y))
                mx, my = start_x, start_y
                player_rect = pygame.Rect(mx - 20, my - 20, 40, 40)
                game_started = True

            DISPLAYSURF.blit(background, (0,0))

            cctv1_timer += dt
            cctv2_timer += dt
            cctv3_timer += dt
            cctv4_timer += dt

            if not cctv1_is_on and cctv1_timer >= CCTV1_OFF_TIME:
                cctv1_is_on = True; cctv1_timer = 0
            elif cctv1_is_on and cctv1_timer >= CCTV1_ON_TIME:
                cctv1_is_on = False; cctv1_timer = 0

            if not cctv2_is_on and cctv2_timer >= CCTV2_OFF_TIME:
                cctv2_is_on = True; cctv2_timer = 0
            elif cctv2_is_on and cctv2_timer >= CCTV2_ON_TIME:
                cctv2_is_on = False; cctv2_timer = 0

            if not cctv3_is_on and cctv3_timer >= CCTV3_OFF_TIME:
                cctv3_is_on = True; cctv3_timer = 0
            elif cctv3_is_on and cctv3_timer >= CCTV3_ON_TIME:
                cctv3_is_on = False; cctv3_timer = 0

            if not cctv4_is_on and cctv4_timer >= CCTV4_OFF_TIME:
                cctv4_is_on = True; cctv4_timer = 0
            elif cctv4_is_on and cctv4_timer >= CCTV4_ON_TIME:
                cctv4_is_on = False; cctv4_timer = 0

            light_surface.fill((0, 0, 0, 0))

            if cctv1_is_on:
                pygame.draw.rect(light_surface, YELLOW_ALPHA, light1_rect)
                if player_rect.colliderect(light1_rect): scene = "gameover"
            if cctv2_is_on:
                pygame.draw.rect(light_surface, YELLOW_ALPHA, light2_rect)
                if player_rect.colliderect(light2_rect): scene = "gameover"
            if cctv3_is_on:
                pygame.draw.rect(light_surface, YELLOW_ALPHA, light3_rect)
                if player_rect.colliderect(light3_rect): scene = "gameover"
            if cctv4_is_on:
                pygame.draw.rect(light_surface, YELLOW_ALPHA, light4_rect)
                if player_rect.colliderect(light4_rect): scene = "gameover"

            DISPLAYSURF.blit(light_surface, (0, 0))
            DISPLAYSURF.blit(cctv_img, (cctv1_x, cctv_y))
            DISPLAYSURF.blit(cctv_img, (cctv2_x, cctv_y))
            DISPLAYSURF.blit(cctv_img, (cctv3_x, cctv_y))
            DISPLAYSURF.blit(cctv_img, (cctv4_x, cctv_y))

            if player_rect.colliderect(door_rect):
                return "stage4"

            animation_timer += dt
            if animation_timer >= animation_speed:
                animation_timer = 0
                frame_index = 1 if frame_index == 0 else 0

            if selected_gender == "male":
                player_img = male_run1 if frame_index == 0 else male_run2
            else:
                player_img = female_run1 if frame_index == 0 else female_run2

            DISPLAYSURF.blit(player_img, (mx - 50, my - 50))

        elif scene == "gameover":
            # ★ 깐깐하게 분리한 성별 판정 로직
            if selected_gender == "male":
                DISPLAYSURF.blit(gameover_img_male, (0,0))
            elif selected_gender == "female":
                DISPLAYSURF.blit(gameover_img_female, (0,0))
            else:
                DISPLAYSURF.blit(gameover_img_male, (0,0))

            retry_text = font.render("PRESS ANY KEY TO RETRY", True, (0,0,0))
            retry_rect = retry_text.get_rect(center=(400,520))
            DISPLAYSURF.blit(retry_text, retry_rect)

        pygame.display.update()
