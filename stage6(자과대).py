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
    "외대탈출 ROUND 6"
)

clock = pygame.time.Clock()

# =========================
# 폰트
# =========================

title_font = pygame.font.Font(
    "font/Galmuri11-Bold.ttf",
    40
)

font = pygame.font.Font(
    "font/Galmuri11-Bold.ttf",
    30
)

small_font = pygame.font.Font(
    "font/Galmuri11-Bold.ttf",
    24
)

# =========================
# 성별
# main.py에서 받을 예정
# =========================

selected_gender = "male"

# =========================
# 배경 이미지
# =========================

background = pygame.image.load(
    "image/start_background.png"
).convert_alpha()

background = pygame.transform.scale(
    background,
    (WIDTH, HEIGHT)
)

# 투명도
background.set_alpha(50)

# =========================
# 게임오버 이미지
# =========================

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
# 문제
# =========================

question = "2+5=?"

choices = [
    "17",
    "77",
    "70",
    "7"
]

correct_answer = 3

# =========================
# 답 박스
# =========================

answer_rects = [

    pygame.Rect(
        80, 200,
        130, 90
    ),

    pygame.Rect(
        250, 200,
        130, 90
    ),

    pygame.Rect(
        430, 200,
        130, 90
    ),

    pygame.Rect(
        600, 200,
        130, 90
    )
]

# =========================
# 변수
# =========================

scene = "game"

frame_index = 0
animation_timer = 0
animation_speed = 200

# 시작 위치
start_x = WIDTH - 70
start_y = HEIGHT - 70

game_started = False

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

        # 시작 위치
        if not game_started:

            pygame.mouse.set_pos(
                (start_x, start_y)
            )

            game_started = True

        DISPLAYSURF.fill(
            (255,255,255)
        )

        # 배경
        DISPLAYSURF.blit(
            background,
            (0,0)
        )

        # =====================
        # 문제 출력
        # =====================

        title_text = title_font.render(
            "QUESTION",
            True,
            (0,0,0)
        )

        DISPLAYSURF.blit(
            title_text,
            (280,40)
        )

        question_text = font.render(
            question,
            True,
            (0,0,0)
        )

        DISPLAYSURF.blit(
            question_text,
            (180,150)
        )

        # =====================
        # 답 출력
        # =====================

        for i in range(4):

            pygame.draw.rect(
                DISPLAYSURF,
                (180,180,180),
                answer_rects[i]
            )

            pygame.draw.rect(
                DISPLAYSURF,
                (0,0,0),
                answer_rects[i],
                2
            )

            answer_text = small_font.render(
                f"{i+1}. {choices[i]}",
                True,
                (0,0,0)
            )

            DISPLAYSURF.blit(
                answer_text,
                (
                    answer_rects[i].x + 20,
                    answer_rects[i].y + 30
                )
            )

            # =====================
            # 충돌 판정
            # =====================

            if player_rect.colliderect(
                answer_rects[i]
            ):

                # 정답
                if i == correct_answer:

                    scene = "stage7"
                    break

                # 오답
                else:

                    scene = "gameover"
                    break

        # =====================
        # 캐릭터 애니메이션
        # =====================

        animation_timer += dt

        if animation_timer >= animation_speed:

            animation_timer = 0

            frame_index = (
                frame_index + 1
            ) % 2

        # 성별 선택

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

    # =========================
    # 게임오버
    # =========================

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

        retry_rect = retry_text.get_rect(
            center=(400,520)
        )

        DISPLAYSURF.blit(
            retry_text,
            retry_rect
        )

    # =========================
    # Stage7 임시
    # =========================

    elif scene == "stage7":

        DISPLAYSURF.fill(
            (0,0,0)
        )

        clear_text = title_font.render(
            "자과대 통과",
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