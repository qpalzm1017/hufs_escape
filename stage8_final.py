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
pygame.display.set_caption("외대탈출 ROUND 8")
clock = pygame.time.Clock()

# =========================
# 폰트
# =========================
font = pygame.font.Font("font/Galmuri11-Bold.ttf", 35)
large_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 60)

# =========================
# 기본 설정 및 상태 변수
# =========================
selected_gender = "male"
scene = "game"
game_started = False

# =========================
# 이미지 로드 및 크기 조절
# =========================
background = pygame.image.load("image/crosswalk.jpeg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background.set_alpha(150)

# ★ 버스 크기 대폭 확대 (360x180)
try:
    bus_img = pygame.image.load("image/bus.png").convert_alpha()
    bus_img = pygame.transform.scale(bus_img, (360, 180))
except:
    bus_img = None

# ★ 버스정류장 이미지 로드 (가지고 계신 파일명/경로로 수정해주세요!)
try:
    # 캡처화면의 정류장 비율에 맞게 적절히 크기 조절 (예: 100x200)
    stop_img = pygame.image.load("image/bus_stop.png").convert_alpha() 
    stop_img = pygame.transform.scale(stop_img, (150, 200))
except:
    stop_img = None

# 캐릭터 이미지
male_run1 = pygame.transform.scale(pygame.image.load("image/male_run.png").convert_alpha(), (100, 100))
male_run2 = pygame.transform.scale(pygame.image.load("image/male_run2.png").convert_alpha(), (100, 100))
female_run1 = pygame.transform.scale(pygame.image.load("image/female_run.png").convert_alpha(), (100, 100))
female_run2 = pygame.transform.scale(pygame.image.load("image/female_run2.png").convert_alpha(), (100, 100))

gameover_img = pygame.image.load("image/stage8_gameover.png").convert()
gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

# 애니메이션 변수
frame_index = 0
animation_timer = 0
animation_speed = 200
start_x, start_y = 700, 520  # 우측 하단 인도 위에서 시작

# =========================
# 게임 리셋 함수
# =========================
def reset_game():
    global bus_x, bus_y, bus_speed, bus_stopped, result_text
    
    # 버스가 커졌으므로 더 왼쪽 바깥(-400)에서 여유롭게 출발
    bus_x = -400
    bus_y = 150           # 도로 높이에 맞춰 약간 조정
    bus_speed = 1.5       # ★ 속도를 기존보다 훨씬 느리게 변경
    bus_stopped = False
    result_text = ""

reset_game()

# ★ 버스정류장 위치를 화면 오른쪽 끝으로 이동
stop_x = 680
stop_y = 130
# 정류장 히트박스 (이미지가 없을 때 대비용 및 판정용)
stop_rect = pygame.Rect(stop_x, stop_y, 100, 200)

# =========================
# 게임 루프
# =========================
while True:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if scene == "gameover" and event.type == KEYDOWN:
            scene = "game"
            game_started = False
            reset_game()

    # 캐릭터 마우스 조작
    pygame.mouse.set_visible(False)
    mx, my = pygame.mouse.get_pos()
    player_rect = pygame.Rect(mx - 30, my - 30, 60, 60)

    # =====================
    # 1. 게임 플레이 씬
    # =====================
    if scene == "game":
        if not game_started:
            pygame.mouse.set_pos((start_x, start_y))
            game_started = True
            reset_game()

        DISPLAYSURF.fill((255, 255, 255))
        DISPLAYSURF.blit(background, (0, 0))

        # ---------------------
        # 버스정류장 그리기
        # ---------------------
        if stop_img:
            DISPLAYSURF.blit(stop_img, (stop_x, stop_y))
        else:
            # 정류장 이미지 로드 실패 시 대체 그래픽
            pygame.draw.rect(DISPLAYSURF, (50, 50, 50), stop_rect)
            pygame.draw.rect(DISPLAYSURF, (30, 144, 255), (stop_x, stop_y, 100, 40))

        # ---------------------
        # 버스 이동 및 정차 로직
        # ---------------------
        if not bus_stopped:
            bus_x += bus_speed
            # 큼직해진 버스의 앞머리가 정류장 위치에 도달하면 멈춤
            if bus_x + 300 >= stop_x:
                bus_x = stop_x - 300
                bus_speed = 0
                bus_stopped = True

        # 버스 출력 및 히트박스 설정 (커진 크기 360x180 반영)
        bus_rect = pygame.Rect(bus_x, bus_y, 360, 180)
        if bus_img:
            DISPLAYSURF.blit(bus_img, (bus_x, bus_y))
        else:
            pygame.draw.rect(DISPLAYSURF, (255, 0, 0), bus_rect)

        # ---------------------
        # 조건별 충돌 판정
        # ---------------------
        if player_rect.colliderect(bus_rect):
            if not bus_stopped:
                result_text = "당신은 버스에 치였습니다!"
                scene = "gameover"
            else:
                scene = "stage8"

        # ---------------------
        # 캐릭터 애니메이션
        # ---------------------
        animation_timer += dt
        if animation_timer >= animation_speed:
            animation_timer = 0
            frame_index = (frame_index + 1) % 2

        if selected_gender == "male":
            player_img = male_run1 if frame_index == 0 else male_run2
        else:
            player_img = female_run1 if frame_index == 0 else female_run2
        
        DISPLAYSURF.blit(player_img, (mx - 50, my - 50))


        # # [디버그 확인용] 필요 없으시면 지우셔도 됩니다.
        # pygame.draw.rect(DISPLAYSURF, (0, 0, 255), player_rect, 1)

    # =====================
    # 2. 게임오버 / 클리어 씬 (동일)
    # =====================
    elif scene == "gameover":
        DISPLAYSURF.blit(gameover_img, (0, 0))
        if result_text:
            retry_text = font.render("PRESS ANY KEY TO RETRY", True, (255, 255, 255))
        DISPLAYSURF.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, 520))

    elif scene == "stage8":
        DISPLAYSURF.fill((20, 20, 40))
        clear_text = font.render("외대 탈출 성공!", True, (255, 255, 255))
        DISPLAYSURF.blit(clear_text, (WIDTH // 2 - clear_text.get_width() // 2, 320))

    pygame.display.update()