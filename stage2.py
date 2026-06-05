import pygame
import sys
from pygame.locals import *

pygame.init()

# =========================
# 화면 설정
# =========================

WIDTH = 800
HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("외대탈출 ROUND 2")

clock = pygame.time.Clock()

# =========================
# 폰트
# =========================

font = pygame.font.Font(
    "font/Galmuri11-Bold.ttf",
    35
)

# =========================
# 성별 선택
# main.py에서 값 받아올 예정
# =========================

selected_gender = "male"

# =========================
# 이미지 불러오기
# =========================

# 기본 배경 (엘베 닫힘)
closed_bg = pygame.image.load(
    "image/hall_1.png"
).convert()

closed_bg = pygame.transform.scale(
    closed_bg,
    (WIDTH, HEIGHT)
)

# 엘베 열린 배경
open_bg = pygame.image.load(
    "image/hall_2.png"
).convert()

open_bg = pygame.transform.scale(
    open_bg,
    (WIDTH, HEIGHT)
)

# 게임오버 이미지
gameover_img = pygame.image.load(
    "image/Stage3_gameover (2).png"
).convert()

gameover_img = pygame.transform.scale(
    gameover_img,
    (WIDTH, HEIGHT)
)

# =========================
# 남자 캐릭터 이미지
# =========================

male_run1 = pygame.image.load(
    "image/male_run.png"
).convert_alpha()

male_run2 = pygame.image.load(
    "image/male_run2.png"
).convert_alpha()

male_run1 = pygame.transform.scale(male_run1, (100,100))
male_run2 = pygame.transform.scale(male_run2, (100,100))

# =========================
# 여자 캐릭터 이미지
# =========================

female_run1 = pygame.image.load(
    "image/female_run.png"
).convert_alpha()

female_run2 = pygame.image.load(
    "image/female_run2.png"
).convert_alpha()

female_run1 = pygame.transform.scale(female_run1, (100,100))
female_run2 = pygame.transform.scale(female_run2, (100,100))

# =========================
# 변수
# =========================

scene = "game"

frame_index = 0
animation_timer = 0
animation_speed = 200

# 시작 위치
player_x = 80
player_y = 520

# 엘베 상태
elevator_open = False

# 게임오버 타이머
gameover_timer = 0

# =========================
# 히트박스
# =========================

# 엘베 위치
elevator_rect = pygame.Rect(
    420,
    135,
    130,
    180
)

# 계단 위치
stairs_rect = pygame.Rect(
    620,
    100,
    145,
    190
)

# =========================
# 마우스 시작 위치
# =========================

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

        # =========================
        # 게임오버 상태
        # =========================

        if scene == "gameover":

            if event.type == KEYDOWN:

                scene = "game"

                elevator_open = False
                gameover_timer = 0

                pygame.mouse.set_pos((80,520))

    # =========================
    # 마우스 숨기기
    # =========================

    pygame.mouse.set_visible(False)

    # =========================
    # 마우스 위치
    # =========================

    mx, my = pygame.mouse.get_pos()

    player_x = mx
    player_y = my

    # =========================
    # 플레이어 히트박스
    # =========================

    player_rect = pygame.Rect(
        player_x - 20,
        player_y - 20,
        40,
        40
    )

    # =========================
    # 게임 상태
    # =========================

    if scene == "game":

        # =========================
        # 엘베 충돌
        # =========================

        if player_rect.colliderect(elevator_rect):

            elevator_open = True

        # =========================
        # 계단 충돌
        # =========================

        if not elevator_open:
            if player_rect.colliderect(stairs_rect):

                scene = "stage3"

        # =========================
        # 배경 출력
        # =========================

        if elevator_open:

            DISPLAYSURF.blit(open_bg, (0,0))

            gameover_timer += dt

            # 1초 후 게임오버
            if gameover_timer >= 1000:

                scene = "gameover"

        else:

            DISPLAYSURF.blit(closed_bg, (0,0))

        # =========================
        # 상단 안내 문구
        # =========================

        hint_text = font.render(
        "엘레베이터를 타볼까?",
        True,
        (255, 0, 0))

        hint_rect = hint_text.get_rect(center=(400, 40))

        DISPLAYSURF.blit(
        hint_text,
        hint_rect)

        # =========================
        # 캐릭터 애니메이션
        # =========================

        animation_timer += dt

        if animation_timer >= animation_speed:

            animation_timer = 0

            if frame_index == 0:
                frame_index = 1
            else:
                frame_index = 0

        # =========================
        # 성별별 캐릭터
        # =========================

        if selected_gender == "male":

            if frame_index == 0:
                player_img = male_run1
            else:
                player_img = male_run2

        elif selected_gender == "female":

            if frame_index == 0:
                player_img = female_run1
            else:
                player_img = female_run2

        # =========================
        # 캐릭터 출력
        # =========================

        DISPLAYSURF.blit(
            player_img,
            (player_x - 50, player_y - 50)
        )

    # =========================
    # 게임오버 화면
    # =========================

    elif scene == "gameover":

        DISPLAYSURF.blit(gameover_img, (0,0))

        gameover_text = font.render(
            "PRESS ANY KEY TO RETRY",
            True,
            (0,0,0)
        )

        text_rect = gameover_text.get_rect(center=(400,520))

        DISPLAYSURF.blit(gameover_text, text_rect)

    # =========================
    # 스테이지3 화면
    # =========================

    elif scene == "stage3":

        DISPLAYSURF.fill((0,0,0))

        clear_text = font.render(
            "STAGE 3",
            True,
            (255,255,255)
        )

        text_rect = clear_text.get_rect(center=(400,300))

        DISPLAYSURF.blit(clear_text, text_rect)

    # =========================
    # 히트박스 확인용
    # =========================

    # pygame.draw.rect(
    #     DISPLAYSURF,
    #     (255,0,0),
    #     elevator_rect,
    #     2
    # )

    # pygame.draw.rect(
    #     DISPLAYSURF,
    #     (0,255,0),
    #     stairs_rect,
    #     2
    # )

    pygame.display.update()
