import pygame
import sys
from pygame.locals import *

pygame.init()

# =========================
# 화면 설정
# =========================

WIDTH = 800
HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "외대탈출 ROUND 7"
)

clock = pygame.time.Clock()

# =========================
# 폰트
# =========================

font = pygame.font.Font(
    "font/Galmuri11-Bold.ttf",
    35
)

# =========================
# 성별
# =========================

selected_gender = "male"

# =========================
# 이미지
# =========================

background = pygame.image.load(
    "image/playground.jpeg"
).convert()

background = pygame.transform.scale(
    background,
    (WIDTH, HEIGHT)
)

background.set_alpha(150)

goal_img = pygame.image.load(
    "image/soccer_goal.png"
).convert_alpha()

goal_img = pygame.transform.scale(
    goal_img,
    (500, 320)
)

goalkeeper_img = pygame.image.load(
    "image/goalkeeper.png"
).convert_alpha()

goalkeeper_img = pygame.transform.scale(
    goalkeeper_img,
    (90, 170)
)

ball_img = pygame.image.load(
    "image/soccer_ball.png"
).convert_alpha()

ball_img = pygame.transform.scale(
    ball_img,
    (140, 100)
)

arrow_left = pygame.image.load(
    "image/arrow_left.png"
).convert_alpha()

arrow_center = pygame.image.load(
    "image/arrow_center.png"
).convert_alpha()

arrow_right = pygame.image.load(
    "image/arrow_right.png"
).convert_alpha()

arrow_left = pygame.transform.scale(
    arrow_left,
    (80, 80)
)

arrow_center = pygame.transform.scale(
    arrow_center,
    (80, 80)
)

arrow_right = pygame.transform.scale(
    arrow_right,
    (80, 80)
)

gameover_img = pygame.image.load(
    "image/stage3_gameover.png"
).convert()

gameover_img = pygame.transform.scale(
    gameover_img,
    (WIDTH, HEIGHT)
)

# =========================
# 캐릭터 이미지
# =========================

male_run1 = pygame.image.load(
    "image/male_run.png"
).convert_alpha()

male_run2 = pygame.image.load(
    "image/male_run2.png"
).convert_alpha()

female_run1 = pygame.image.load(
    "image/female_run.png"
).convert_alpha()

female_run2 = pygame.image.load(
    "image/female_run2.png"
).convert_alpha()

male_run1 = pygame.transform.scale(
    male_run1,
    (100,100)
)

male_run2 = pygame.transform.scale(
    male_run2,
    (100,100)
)

female_run1 = pygame.transform.scale(
    female_run1,
    (100,100)
)

female_run2 = pygame.transform.scale(
    female_run2,
    (100,100)
)

# =========================
# 변수
# =========================

scene = "game"

frame_index = 0
animation_timer = 0
animation_speed = 200

start_x = 700
start_y = 520

game_started = False

# =========================
# 골대 위치
# =========================

goal_x = 150
goal_y = 30

# =========================
# 골 판정 히트박스
# =========================

goal_rect = pygame.Rect(
    230,   # x
    90,   # y
    360,   # width
    200    # height
)

# =========================
# 골키퍼
# =========================

goalkeeper_x = 355
goalkeeper_y = 120

goalkeeper_speed = 10
goalkeeper_direction = 1

LEFT_LIMIT = 240
RIGHT_LIMIT = 470

# =========================
# 공
# =========================

ball_x = 330
ball_y = 510

shooting = False
shot_direction = None
shot_speed = 12

# =========================
# 화살표 히트박스
# =========================

left_rect = pygame.Rect(
    220,
    400,
    80,
    80
)

center_rect = pygame.Rect(
    360,
    400,
    80,
    80
)

right_rect = pygame.Rect(
    500,
    400,
    80,
    80
)

# =========================
# 게임 루프
# =========================

while True:

    dt = clock.tick(60)

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # =====================
        # 재도전
        # =====================

        if scene == "gameover":

            if event.type == KEYDOWN:

                scene = "game"

                game_started = False
                shooting = False

                goalkeeper_x = 355
                goalkeeper_direction = 1

                ball_x = 330
                ball_y = 520
                shot_direction = None

    pygame.mouse.set_visible(False)

    mx, my = pygame.mouse.get_pos()

    player_rect = pygame.Rect(
        mx - 20,
        my - 20,
        40,
        40
    )

    # =====================
    # 게임
    # =====================

    if scene == "game":

        if not game_started:

            pygame.mouse.set_pos(
                (start_x, start_y)
            )

            game_started = True

        DISPLAYSURF.fill(
            (255,255,255)
        )

        DISPLAYSURF.blit(
            background,
            (0,0)
        )

        # =====================
        # 골대
        # =====================

        DISPLAYSURF.blit(
            goal_img,
            (goal_x, goal_y)
        )

        # =====================
        # 골키퍼 이동
        # =====================

        goalkeeper_x += (
            goalkeeper_speed
            * goalkeeper_direction
        )

        if goalkeeper_x >= RIGHT_LIMIT:
            goalkeeper_direction = -1

        if goalkeeper_x <= LEFT_LIMIT:
            goalkeeper_direction = 1

        goalkeeper_rect = pygame.Rect(
            goalkeeper_x,
            goalkeeper_y,
            90,
            150
        )

        DISPLAYSURF.blit(
            goalkeeper_img,
            (
                goalkeeper_x,
                goalkeeper_y
            )
        )

        # =====================
        # 화살표
        # =====================

        DISPLAYSURF.blit(
            arrow_left,
            (220,400)
        )

        DISPLAYSURF.blit(
            arrow_center,
            (360,400)
        )

        DISPLAYSURF.blit(
            arrow_right,
            (500,400)
        )

        # =====================
        # 공 출력
        # =====================

        DISPLAYSURF.blit(
            ball_img,
            (ball_x, ball_y)
        )

        # =====================
        # 방향 선택
        # =====================

        if not shooting:

            if player_rect.colliderect(
                left_rect
            ):
                shooting = True
                shot_direction = "left"

            elif player_rect.colliderect(
                center_rect
            ):
                shooting = True
                shot_direction = "center"

            elif player_rect.colliderect(
                right_rect
            ):
                shooting = True
                shot_direction = "right"

        # =====================
        # 슛 애니메이션
        # =====================

        if shooting:

            if shot_direction == "left":
                ball_x -= 8
                ball_y -= shot_speed

            elif shot_direction == "center":
                ball_y -= shot_speed

            elif shot_direction == "right":
                ball_x += 8
                ball_y -= shot_speed

            # 공 히트박스
            shot_rect = pygame.Rect(
                ball_x + 30,
                ball_y + 20,
                60,
                60
            )

            # 골키퍼 맞음
            if shot_rect.colliderect(
                goalkeeper_rect
            ):
                scene = "gameover"

            # 골 성공
            elif shot_rect.colliderect(
                goal_rect
            ):
                scene = "stage8"

            # 골대 밖
            elif ball_y < 70:
                scene = "gameover"

        # =====================
        # 캐릭터 애니메이션
        # =====================

        animation_timer += dt

        if animation_timer >= animation_speed:

            animation_timer = 0

            frame_index = (
                frame_index + 1
            ) % 2

        if selected_gender == "male":

            player_img = (
                male_run1
                if frame_index == 0
                else male_run2
            )

        else:

            player_img = (
                female_run1
                if frame_index == 0
                else female_run2
            )

        DISPLAYSURF.blit(
            player_img,
            (mx - 50, my - 50)
        )

        # =====================
        # 히트박스 확인용
        # =====================

        pygame.draw.rect(
            DISPLAYSURF,
            (255,0,0),
            goalkeeper_rect,
            2
        )

        pygame.draw.rect(
            DISPLAYSURF,
            (0,255,0),
            goal_rect,
            2
        )

    # =====================
    # 게임오버
    # =====================

    elif scene == "gameover":

        DISPLAYSURF.blit(
            gameover_img,
            (0,0)
        )

        retry_text = font.render(
            "PRESS ANY KEY TO RETRY",
            True,
            (255,255,255)
        )

        DISPLAYSURF.blit(
            retry_text,
            (180,520)
        )

    # =====================
    # Stage8 임시
    # =====================

    elif scene == "stage8":

        DISPLAYSURF.fill(
            (0,0,0)
        )

        clear_text = font.render(
            "STAGE 8",
            True,
            (255,255,255)
        )

        DISPLAYSURF.blit(
            clear_text,
            (300,280)
        )

    pygame.display.update()