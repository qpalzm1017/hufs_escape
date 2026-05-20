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
pygame.display.set_caption("외대탈출 ROUND 3")

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
# main.py에서 받아올 예정
# =========================

selected_gender = "male"

# =========================
# 이미지 불러오기
# =========================

background = pygame.image.load(
    "image/stage3_bg.png"
).convert()

background = pygame.transform.scale(
    background,
    (WIDTH, HEIGHT)
)

# CCTV 이미지
cctv_img = pygame.image.load(
    "image/CCTV.png"
).convert_alpha()

cctv_img = pygame.transform.scale(
    cctv_img,
    (80, 80)
)

# CCTV 불빛 이미지
light_img = pygame.image.load(
    "image/CCTV_light.png"
).convert_alpha()

light_img = pygame.transform.scale(
    light_img,
    (180, 100)
)

# 게임오버 이미지
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

# =========================
# 시작 위치 (오른쪽 하단)
# =========================

start_x = WIDTH - 60
start_y = HEIGHT - 60

game_started = False

# =========================
# CCTV 움직임
# =========================

# 위 CCTV
cctv1_x = 100
cctv1_y = 70
cctv1_direction = 1

# 아래 CCTV
cctv2_x = 500
cctv2_y = 300
cctv2_direction = -1

cctv_speed = 4

LEFT_LIMIT = 100
RIGHT_LIMIT = 550

# =========================
# 문 히트박스
# =========================

door_rect = pygame.Rect(
    130,
    180,
    150,
    160
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
        # 게임오버 재시작
        # =====================

        if scene == "gameover":

            if event.type == KEYDOWN:

                scene = "game"
                game_started = False

                # CCTV 초기화
                cctv1_x = 100
                cctv2_x = 500

                cctv1_direction = 1
                cctv2_direction = -1

    pygame.mouse.set_visible(False)

    mx, my = pygame.mouse.get_pos()

    # 플레이어 히트박스
    player_rect = pygame.Rect(
        mx - 20,
        my - 20,
        40,
        40
    )

    # =========================
    # 게임 화면
    # =========================

    if scene == "game":

        # 처음 시작 위치 강제 지정
        if not game_started:

            pygame.mouse.set_pos(
                (start_x, start_y)
            )

            game_started = True

        DISPLAYSURF.blit(
            background,
            (0,0)
        )

        # =====================
        # CCTV 이동
        # =====================

        cctv1_x += (
            cctv_speed
            * cctv1_direction
        )

        cctv2_x += (
            cctv_speed
            * cctv2_direction
        )

        # 방향 반전

        if cctv1_x >= RIGHT_LIMIT:
            cctv1_direction = -1

        if cctv1_x <= LEFT_LIMIT:
            cctv1_direction = 1

        if cctv2_x >= RIGHT_LIMIT:
            cctv2_direction = -1

        if cctv2_x <= LEFT_LIMIT:
            cctv2_direction = 1

        # =====================
        # CCTV 출력
        # =====================

        DISPLAYSURF.blit(
            cctv_img,
            (cctv1_x, cctv1_y)
        )

        DISPLAYSURF.blit(
            cctv_img,
            (cctv2_x, cctv2_y)
        )

        # =====================
        # 불빛 위치
        # =====================

        light1_x = cctv1_x - 40
        light1_y = cctv1_y + 60

        light2_x = cctv2_x - 40
        light2_y = cctv2_y + 60

        # 불빛 출력

        DISPLAYSURF.blit(
            light_img,
            (light1_x, light1_y)
        )

        DISPLAYSURF.blit(
            light_img,
            (light2_x, light2_y)
        )

        # =====================
        # 불빛 히트박스
        # =====================

        light1_rect = pygame.Rect(
            light1_x,
            light1_y,
            180,
            100
        )

        light2_rect = pygame.Rect(
            light2_x,
            light2_y,
            180,
            100
        )

        # =====================
        # 충돌 판정
        # =====================

        if player_rect.colliderect(
            light1_rect
        ):
            scene = "gameover"

        if player_rect.colliderect(
            light2_rect
        ):
            scene = "gameover"

        # 문 닿기

        if player_rect.colliderect(
            door_rect
        ):
            scene = "stage4"

        # =====================
        # 캐릭터 애니메이션
        # =====================

        animation_timer += dt

        if animation_timer >= animation_speed:

            animation_timer = 0

            if frame_index == 0:
                frame_index = 1
            else:
                frame_index = 0

        # 성별 캐릭터

        if selected_gender == "male":

            if frame_index == 0:
                player_img = male_run1
            else:
                player_img = male_run2

        else:

            if frame_index == 0:
                player_img = female_run1
            else:
                player_img = female_run2

        # 캐릭터 출력

        DISPLAYSURF.blit(
            player_img,
            (mx - 50, my - 50)
        )

        # =====================
        # 히트박스 확인용
        # =====================

        # # 문 히트박스
        # pygame.draw.rect(
        #     DISPLAYSURF,
        #     (0,0,255),
        #     door_rect,
        #     2
        # )

        # # 불빛 히트박스
        # pygame.draw.rect(
        #     DISPLAYSURF,
        #     (255,0,0),
        #     light1_rect,
        #     2
        # )

        # pygame.draw.rect(
        #     DISPLAYSURF,
        #     (255,0,0),
        #     light2_rect,
        #     2
        # )

    # =========================
    # 게임오버 화면
    # =========================

    elif scene == "gameover":

        DISPLAYSURF.blit(
            gameover_img,
            (0,0)
        )

        retry_text = font.render(
            "PRESS ANY KEY TO RETRY",
            True,
            (0,0,0)
        )

        retry_rect = retry_text.get_rect(
            center=(400,520)
        )

        DISPLAYSURF.blit(
            retry_text,
            retry_rect
        )

    # =========================
    # Stage4 임시
    # =========================

    elif scene == "stage4":

        DISPLAYSURF.fill((0,0,0))

        clear_text = font.render(
            "STAGE 4",
            True,
            (255,255,255)
        )

        clear_rect = clear_text.get_rect(
            center=(400,300)
        )

        DISPLAYSURF.blit(
            clear_text,
            clear_rect
        )

    pygame.display.update()