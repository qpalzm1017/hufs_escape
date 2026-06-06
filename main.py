import pygame, sys
from pygame.locals import *

# =========================
# 스테이지 파일 불러오기 
# (주의: 각 stage 파일들의 코드가 def run(): 안에 들어있어야 여기서 바로 실행되지 않습니다!)
# =========================
import stage1
import stage2
import stage3
import stage4
import stage5
import stage6
import stage7

pygame.init()

# =========================
# 화면 설정
# =========================
WIDTH = 800
HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("외대탈출")

clock = pygame.time.Clock()

# =========================
# 화면 전환용 페이드 아웃/인 함수
# =========================
def fade_transition():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 15):
        fade.set_alpha(alpha)
        DISPLAYSURF.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(15)

# =========================
# 이미지 불러오기
# =========================
background = pygame.image.load("image/start_background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

male_img = pygame.image.load("image/male_select.png").convert_alpha()
male_img = pygame.transform.scale(male_img, (150, 250))

female_img = pygame.image.load("image/female_select.png").convert_alpha()
female_img = pygame.transform.scale(female_img, (150, 250))

# =========================
# 폰트
# =========================
title_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 70)
font = pygame.font.Font("font/Galmuri11-Bold.ttf", 28)
small_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 20)

# =========================
# 변수
# =========================
scene = "start"

player_name = ""
selected_gender = None
input_active = True

# 캐릭터 선택 박스
male_rect = pygame.Rect(170, 230, 150, 250)
female_rect = pygame.Rect(480, 230, 150, 250)

# =========================
# 마스터 게임 루프
# =========================
while True:

    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # =========================
        # 시작 화면 이벤트
        # =========================
        if scene == "start":
            if event.type == MOUSEBUTTONDOWN:
                scene = "setting"

        # =========================
        # 설정 화면 이벤트
        # =========================
        elif scene == "setting":
            # 이름 입력
            if event.type == KEYDOWN:
                if input_active:
                    if event.key == K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == K_RETURN:
                        # 이름과 성별 선택이 완료되면 스테이지 1로 진입합니다.
                        if player_name != "" and selected_gender != None:
                            scene = "stage1"
                    else:
                        if len(player_name) < 10:
                            player_name += event.unicode

            # 성별 선택
            if event.type == MOUSEBUTTONDOWN:
                if male_rect.collidepoint(event.pos):
                    selected_gender = "male"
                if female_rect.collidepoint(event.pos):
                    selected_gender = "female"

    # =====================================================
    # 시작 화면 렌더링
    # =====================================================
    if scene == "start":
        pygame.mouse.set_visible(True)
        DISPLAYSURF.blit(background, (0, 0))

        title = title_font.render("외대탈출", True, (255,255,255))
        title_rect = title.get_rect(center=(400,120))
        DISPLAYSURF.blit(title, title_rect)

        current_time = pygame.time.get_ticks()
        if (current_time // 500) % 2 == 0:
            text = small_font.render(">> PRESS THE MOUSE BUTTON <<", True, (255,255,255))
            text_rect = text.get_rect(center=(400,520))
            DISPLAYSURF.blit(text, text_rect)

    # =====================================================
    # 설정 화면 렌더링
    # =====================================================
    elif scene == "setting":
        pygame.mouse.set_visible(True)
        DISPLAYSURF.fill((30,30,30))

        name_text = font.render(f"이름(영어로 입력) : {player_name}", True, (255,255,255))
        DISPLAYSURF.blit(name_text, (50,50))

        guide_text = small_font.render("성별 선택 후 ENTER 를 누르면 시작", True, (180,180,180))
        DISPLAYSURF.blit(guide_text, (50,90))

        info1 = small_font.render("교수님을 피해 외대를 탈출하세요.", True, (255,255,255))
        info2 = small_font.render("마우스로 이동할 수 있습니다.", True, (255,255,255))
        DISPLAYSURF.blit(info1, (50,140))
        DISPLAYSURF.blit(info2, (50,170))

        DISPLAYSURF.blit(male_img, (170,230))
        DISPLAYSURF.blit(female_img, (480,230))

        if selected_gender == "male":
            pygame.draw.rect(DISPLAYSURF, (0,255,0), male_rect, 5)
        if selected_gender == "female":
            pygame.draw.rect(DISPLAYSURF, (0,255,0), female_rect, 5)

    # =====================================================
    # 각 스테이지 게임 화면 순차 연결
    # =====================================================
    elif scene == "stage1":
        fade_transition()
        scene = stage1.run(DISPLAYSURF, clock, selected_gender)

    elif scene == "stage2":
        fade_transition()
        scene = stage2.run(DISPLAYSURF, clock, selected_gender)

    elif scene == "stage3":
        fade_transition()
        scene = stage3.run(DISPLAYSURF, clock, selected_gender)

    elif scene == "stage4":
        fade_transition()
        scene = stage4.run(DISPLAYSURF, clock, selected_gender)

    elif scene == "stage5":
        fade_transition()
        scene = stage5.run(DISPLAYSURF, clock, selected_gender)

    elif scene == "stage6":
        fade_transition()
        scene = stage6.run(DISPLAYSURF, clock, selected_gender)

    elif scene == "stage7":
        fade_transition()
        scene = stage7.run(DISPLAYSURF, clock, selected_gender)

    # =====================================================
    # 게임 최종 클리어 화면
    # =====================================================
    elif scene == "game_clear":
        DISPLAYSURF.fill((0, 0, 0))
        clear_text = title_font.render("외대 탈출 성공!", True, (255, 255, 255))
        clear_rect = clear_text.get_rect(center=(400, 300))
        DISPLAYSURF.blit(clear_text, clear_rect)

    pygame.display.update()
