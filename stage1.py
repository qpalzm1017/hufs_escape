import pygame
import sys
from pygame.locals import *

def run(DISPLAYSURF, clock, selected_gender):
    # =========================
    # 화면 설정
    # =========================
    WIDTH = 800
    HEIGHT = 600
    pygame.display.set_caption("외대탈출 ROUND 1")

    # =========================
    # 폰트
    # =========================
    font = pygame.font.Font("font/Galmuri11-Bold.ttf", 35)

    # =========================
    # 이미지 불러오기
    # =========================
    background = pygame.image.load("image/stage1_bg.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    professor_side = pygame.image.load("image/professor_side.png").convert_alpha()
    professor_front = pygame.image.load("image/professor_front.png").convert_alpha()
    professor_side = pygame.transform.scale(professor_side, (180, 220))
    professor_front = pygame.transform.scale(professor_front, (180, 220))

    student_img = pygame.image.load("image/student_img.png").convert_alpha()
    student_img = pygame.transform.scale(student_img, (180, 180))

    gameover_img = pygame.image.load("image/stage3_gameover.png").convert()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    # =========================
    # 캐릭터 이미지
    # =========================
    male_run1 = pygame.image.load("image/male_run.png").convert_alpha()
    male_run2 = pygame.image.load("image/male_run2.png").convert_alpha()
    female_run1 = pygame.image.load("image/female_run.png").convert_alpha()
    female_run2 = pygame.image.load("image/female_run2.png").convert_alpha()

    male_run1 = pygame.transform.scale(male_run1, (100,100))
    male_run2 = pygame.transform.scale(male_run2, (100,100))
    female_run1 = pygame.transform.scale(female_run1, (100,100))
    female_run2 = pygame.transform.scale(female_run2, (100,100))

    # =========================
    # 변수
    # =========================
    scene = "game"
    frame_index = 0
    animation_timer = 0
    animation_speed = 200

    start_x = WIDTH
    start_y = HEIGHT
    game_started = False

    professor_state = "side"
    professor_timer = 0
    SIDE_TIME = 1200
    FRONT_TIME = 2000

    last_mouse_pos = (0, 0)
    front_grace_timer = 0
    FRONT_GRACE_TIME = 200

    professor_pos = (500, 200)
    student_positions = [(70, 320), (310, 320), (570, 320)]

    student_rects = [
        pygame.Rect(85, 350, 130, 130),
        pygame.Rect(330, 350, 130, 130),
        pygame.Rect(590, 350, 130, 130)
    ]
    door_rect = pygame.Rect(60, 130, 90, 260)

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
                    professor_state = "side"
                    professor_timer = 0
                    front_grace_timer = 0 
                    pygame.mouse.set_pos((start_x,start_y))
                    last_mouse_pos = (start_x,start_y)
                    game_started = False

        pygame.mouse.set_visible(False)
        mx, my = pygame.mouse.get_pos()
        player_rect = pygame.Rect(mx - 20, my - 20, 40, 40)

        # =========================
        # 게임 화면
        # =========================
        if scene == "game":
            if not game_started:
                pygame.mouse.set_pos((start_x, start_y))
                last_mouse_pos = (start_x, start_y)
                game_started = True

            DISPLAYSURF.blit(background, (0,0))

            professor_timer += dt
            if professor_state == "side":
                if professor_timer >= SIDE_TIME:
                    professor_state = "front"
                    professor_timer = 0
                    front_grace_timer = 0
            else:
                if professor_timer >= FRONT_TIME:
                    professor_state = "side"
                    professor_timer = 0

            if professor_state == "side":
                professor_img = professor_side
            else:
                professor_img = professor_front

            DISPLAYSURF.blit(professor_img, professor_pos)

            for pos in student_positions:
                DISPLAYSURF.blit(student_img, pos)

            for rect in student_rects:
                if player_rect.colliderect(rect):
                    scene = "gameover"

            if professor_state == "front":
                front_grace_timer += dt
                if front_grace_timer >= FRONT_GRACE_TIME:
                    if (mx, my) != last_mouse_pos:
                        scene = "gameover"

            last_mouse_pos = (mx, my)

            # 문 충돌 시 다음 스테이지로 넘어갑니다
            if player_rect.colliderect(door_rect):
                return "stage2"

            animation_timer += dt
            if animation_timer >= animation_speed:
                animation_timer = 0
                frame_index = (frame_index + 1) % 2

            if selected_gender == "male":
                if frame_index == 0: player_img = male_run1
                else: player_img = male_run2
            else:
                if frame_index == 0: player_img = female_run1
                else: player_img = female_run2

            DISPLAYSURF.blit(player_img, (mx - 50, my - 50))

        # =========================
        # 게임오버
        # =========================
        elif scene == "gameover":
            DISPLAYSURF.blit(gameover_img, (0,0))
            retry_text = font.render("PRESS ANY KEY TO RETRY", True, (255,255,255))
            retry_rect = retry_text.get_rect(center=(400,520))
            DISPLAYSURF.blit(retry_text, retry_rect)

        pygame.display.update()
