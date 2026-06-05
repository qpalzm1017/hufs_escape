import pygame
import sys
import random
from pygame.locals import *

pygame.init()

# =========================
# 화면 설정
# =========================

WIDTH = 800
HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("외대탈출 ROUND 4")

clock = pygame.time.Clock()

# =========================
# 폰트
# =========================

font = pygame.font.Font(
    "font/Galmuri11-Bold.ttf",
    35
)

small_font = pygame.font.Font(
    "font/Galmuri11-Bold.ttf",
    20
)

# =========================
# 이미지 불러오기
# =========================

# 명수당 배경
background = pygame.image.load(
    "image/Myeongsu_Lake.png"
).convert()

background = pygame.transform.scale(
    background,
    (WIDTH, HEIGHT)
)

# 게임오버 이미지 (이전 스테이지 이미지 재사용)
gameover_img = pygame.image.load(
    "image/stage4_gameover.png"
).convert()

gameover_img = pygame.transform.scale(
    gameover_img,
    (WIDTH, HEIGHT)
)

# =========================
# 동물 이미지 (표지판 크기의 절반 정도)
# =========================

ANIMAL_SIZE = 70

duck_img = pygame.image.load(
    "image/Duck.png"
).convert_alpha()

duck_img = pygame.transform.scale(
    duck_img,
    (ANIMAL_SIZE, ANIMAL_SIZE)
)

otter_img = pygame.image.load(
    "image/Otter.png"
).convert_alpha()

otter_img = pygame.transform.scale(
    otter_img,
    (ANIMAL_SIZE, ANIMAL_SIZE)
)

# =========================
# 변수
# =========================

scene = "game"

# 게임 진행 변수
otter_count = 0
catch_goal = 3

# 스폰 타이머 및 애니메이션 변수
spawn_timer = 0
spawn_cycle = 1000      # 1초 (1000ms)마다 새로 스폰
visible_time = 500      # 0.5초 (500ms)동안 보임
emerge_time = 150       # 0.15초 동안 올라오고/내려감

# 현재 등장한 동물 정보
current_animal = None   # "otter" 또는 "duck"
animal_x = 0
animal_y = 0
is_clickable = False

# 마우스 포인터 표시
pygame.mouse.set_visible(True)

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
        # 마우스 클릭 이벤트 (동물 잡기)
        # =====================

        if scene == "game" and event.type == MOUSEBUTTONDOWN:
            
            if is_clickable and current_animal != None:
                
                # 마우스 좌표
                mx, my = event.pos
                
                # 동물의 현재 히트박스
                animal_rect = pygame.Rect(
                    animal_x,
                    animal_y,
                    ANIMAL_SIZE,
                    ANIMAL_SIZE
                )
                
                # 클릭 성공 시
                if animal_rect.collidepoint(mx, my):
                    
                    if current_animal == "otter":
                        otter_count += 1
                        current_animal = None # 잡으면 즉시 사라짐
                        
                        # 3마리 잡으면 클리어
                        if otter_count >= catch_goal:
                            scene = "stage5"
                            
                    elif current_animal == "duck":
                        scene = "gameover"

        # =====================
        # 게임오버 재시작
        # =====================

        elif scene == "gameover":

            if event.type == KEYDOWN:

                scene = "game"
                otter_count = 0
                spawn_timer = 0
                current_animal = None

    # =========================
    # 게임 화면
    # =========================

    if scene == "game":

        DISPLAYSURF.blit(
            background,
            (0,0)
        )

        # 진행 상황 텍스트
        score_text = font.render(
            f"수달 구조: {otter_count} / {catch_goal}",
            True,
            (255, 255, 255)
        )
        DISPLAYSURF.blit(score_text, (30, 30))

        # =====================
        # 동물 스폰 및 타이머 로직
        # =====================

        spawn_timer += dt

        # 1초 주기가 넘어가면 새로운 위치에 동물 리스폰
        if spawn_timer >= spawn_cycle:
            
            spawn_timer = 0
            
            # 호수 영역 내에서 랜덤한 위치 (명수당 이미지 기준 대략적인 물가)
            animal_x = random.randint(250, 650)
            animal_y = random.randint(350, 480)
            
            # 70% 확률로 수달, 30% 확률로 오리 등장
            # 난이도향상위해 수달 60%확률로 수정함
            if random.randint(1, 10) <= 6:
                current_animal = "otter"
            else:
                current_animal = "duck"

        # =====================
        # 등장 애니메이션 (0.5초 동안만)
        # =====================

        if spawn_timer < visible_time and current_animal != None:
            
            is_clickable = True
            
            # 1. 서서히 올라오기 (0 ~ 150ms)
            if spawn_timer < emerge_time:
                ratio = spawn_timer / emerge_time
                
            # 2. 서서히 내려가기 (350ms ~ 500ms)
            elif spawn_timer > (visible_time - emerge_time):
                ratio = (visible_time - spawn_timer) / emerge_time
                
            # 3. 완전히 나와있는 상태
            else:
                ratio = 1.0
                
            # 비율에 따라 높이 계산
            current_height = int(ANIMAL_SIZE * ratio)
            draw_y = animal_y + (ANIMAL_SIZE - current_height)
            
            # 자르기 영역 (x, y, width, height)
            crop_rect = (0, 0, ANIMAL_SIZE, current_height)
            
            if current_animal == "otter":
                target_img = otter_img
            else:
                target_img = duck_img
                
            # 이미지를 윗부분부터 크롭하여 물에서 나오는 듯한 연출
            DISPLAYSURF.blit(
                target_img,
                (animal_x, draw_y),
                crop_rect
            )
            
        else:
            is_clickable = False

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
    # Stage 5 (클리어) 화면
    # =========================

    elif scene == "stage5":

        DISPLAYSURF.fill((0,0,0))

        clear_text = font.render(
            "STAGE 5 (CLEAR!)",
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
