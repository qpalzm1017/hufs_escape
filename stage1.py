import pygame
import sys
import random
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
    # 이미지 로드
    # =========================
    # 1. 배경
    background = pygame.image.load("image/Stage2_강의실 배경.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # 2. 교수님 (전면/후면)
    prof_front = pygame.image.load("image/Stage2_교수님 객체_전면.png").convert_alpha()
    prof_back = pygame.image.load("image/Stage2_교수님 객체_후면.png").convert_alpha()

    prof_size = (80, 150)
    prof_front = pygame.transform.scale(prof_front, prof_size)
    prof_back = pygame.transform.scale(prof_back, prof_size)
    
    prof_pos = (290, 195) 

    # 3. 게임오버 화면 이미지
    fail_img = pygame.image.load("image/Stage2_선택지1.png").convert()
    fail_img = pygame.transform.scale(fail_img, (WIDTH, HEIGHT))

    # 4. 캐릭터 이미지 로드 및 크기 조절
    player_size = (80, 150)
    
    try:
        male_run1 = pygame.image.load("image/male_run_l.png").convert_alpha()
        male_run2 = pygame.image.load("image/male_run2_l.png").convert_alpha()
        female_run1 = pygame.image.load("image/female_run_l.png").convert_alpha()
        female_run2 = pygame.image.load("image/female_run2_l.png").convert_alpha()
    except:
        male_run1 = pygame.image.load("image/male_run.png").convert_alpha()
        male_run2 = pygame.image.load("image/male_run2.png").convert_alpha()
        female_run1 = pygame.image.load("image/female_run.png").convert_alpha()
        female_run2 = pygame.image.load("image/female_run2.png").convert_alpha()

    male_run1 = pygame.transform.scale(male_run1, player_size)
    male_run2 = pygame.transform.scale(male_run2, player_size)
    female_run1 = pygame.transform.scale(female_run1, player_size)
    female_run2 = pygame.transform.scale(female_run2, player_size)

    # =========================
    # 상태 및 변수 설정
    # =========================
    scene = "game"
    game_started = False
    
    # 교수님 시야 및 타이머 변수
    prof_facing_front = False 
    last_turn_time = 0
    
    # ★ 처음 시작할 때 칠판 보는 시간 (0.4초 ~ 0.6초)
    turn_interval = random.randint(400, 600)

    # 시작 위치를 오른쪽 하단으로 변경
    start_x, start_y = 720, 500
    prev_mouse_pos = (start_x, start_y)
    
    # 문 히트박스
    door_rect = pygame.Rect(20, 150, 100, 250)

    # =========================
    # 게임 루프
    # =========================
    while True:
        dt = clock.tick(60)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.event.set_grab(False) # 종료 시 마우스 잠금 해제
                pygame.quit()
                sys.exit()

            # ---------------------
            # 게임오버 씬에서 재시작
            # ---------------------
            if scene == "gameover":
                if event.type == KEYDOWN:
                    scene = "game"
                    prof_facing_front = False
                    last_turn_time = pygame.time.get_ticks()
                    turn_interval = random.randint(800, 1500) # 재시작 시 타이머 타이트하게
                    game_started = False

        pygame.mouse.set_visible(False)
        mx, my = pygame.mouse.get_pos()

        player_rect = pygame.Rect(mx - 40, my - 75, 80, 150)

        # =====================
        # 1. 게임 씬
        # =====================
        if scene == "game":
            if not game_started:
                pygame.mouse.set_pos((start_x, start_y))
                prev_mouse_pos = (start_x, start_y)
                last_turn_time = pygame.time.get_ticks()
                
                # 게임 시작 시 마우스를 창 밖으로 못 나가게 가두기
                pygame.event.set_grab(True) 
                
                game_started = True

            DISPLAYSURF.blit(background, (0, 0))

            # ---------------------
            # 움직임 감지 로직
            # ---------------------
            is_moving = False
            if (mx, my) != prev_mouse_pos:
                is_moving = True
            prev_mouse_pos = (mx, my)

            # ---------------------
            # ★ 교수님 패턴 로직 (난이도 대폭 상승)
            # ---------------------
            if current_time - last_turn_time > turn_interval:
                prof_facing_front = not prof_facing_front
                last_turn_time = current_time
                
                # 앞으로 돌았을 때와 칠판을 볼 때의 시간을 다르게 설정
                if prof_facing_front:
                    # 학생들을 감시하는 시간 (1초 ~ 2.5초)
                    turn_interval = random.randint(1000, 2500)
                else:
                    # 칠판을 보는 시간 (0.4초 ~ 0.5초) 
                    turn_interval = random.randint(400, 500)

            # 교수님 이미지 출력
            if prof_facing_front:
                DISPLAYSURF.blit(prof_front, prof_pos)
            else:
                DISPLAYSURF.blit(prof_back, prof_pos)

            # ---------------------
            # 충돌 및 클리어 판정
            # ---------------------
            if is_moving and prof_facing_front:
                pygame.event.set_grab(False) # 게임오버 시 마우스 잠금 해제
                scene = "gameover"

            # 문에 닿으면 다음 라운드로
            if player_rect.colliderect(door_rect):
                pygame.event.set_grab(False) # 다음 스테이지로 가기 전 마우스 잠금 해제
                return "stage2"

            # ---------------------
            # 캐릭터 이미지 출력
            # ---------------------
            if selected_gender == "male":
                player_img = male_run2 if is_moving else male_run1
            else:
                player_img = female_run2 if is_moving else female_run1

            DISPLAYSURF.blit(player_img, (mx - 40, my - 75))

        # =====================
        # 2. 게임오버 씬
        # =====================
        elif scene == "gameover":
            pygame.mouse.set_visible(True)
            DISPLAYSURF.blit(fail_img, (0, 0))
            
            retry_text = font.render("PRESS ANY KEY TO RETRY", True, (0, 0, 0))
            retry_rect = retry_text.get_rect(center=(WIDTH // 2, 520))
            DISPLAYSURF.blit(retry_text, retry_rect)

        pygame.display.update()
