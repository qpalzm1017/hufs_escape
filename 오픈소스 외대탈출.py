import pygame, sys
from pygame.locals import *

pygame.init()

# 화면 설정
WIDTH = 800
HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("외대탈출")

clock = pygame.time.Clock()

# =========================
# 이미지 불러오기
# =========================

background = pygame.image.load(
    r"C:\Users\seobi\OneDrive\Desktop\외대탈출\start_background.png"
)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

male_img = pygame.image.load(
    r"C:\Users\seobi\OneDrive\Desktop\외대탈출\male_select.png"
).convert_alpha()
male_img = pygame.transform.scale(male_img, (150, 250))

female_img = pygame.image.load(
    r"C:\Users\seobi\OneDrive\Desktop\외대탈출\female_select.png"
).convert_alpha()
female_img = pygame.transform.scale(female_img, (150, 250))

# =========================
# 폰트
# =========================

title_font = pygame.font.Font(
    r"C:\Users\seobi\OneDrive\Desktop\외대탈출\Galmuri11-Bold.ttf",
    70
)

font = pygame.font.Font(
    r"C:\Users\seobi\OneDrive\Desktop\외대탈출\Galmuri11-Bold.ttf",
    28
)

small_font = pygame.font.Font(
    r"C:\Users\seobi\OneDrive\Desktop\외대탈출\Galmuri11-Bold.ttf",
    20
)

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
# 게임 루프
# =========================

while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # =========================
        # 시작 화면
        # =========================

        if scene == "start":

            if event.type == MOUSEBUTTONDOWN:
                scene = "setting"

        # =========================
        # 설정 화면
        # =========================

        elif scene == "setting":

            # 이름 입력
            if event.type == KEYDOWN:

                if input_active:

                    if event.key == K_BACKSPACE:
                        player_name = player_name[:-1]

                    elif event.key == K_RETURN:

                        if player_name != "" and selected_gender != None:
                            scene = "game"

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
    # 시작 화면
    # =====================================================

    if scene == "start":

        DISPLAYSURF.blit(background, (0, 0))

        # 제목
        title = title_font.render("외대탈출", True, (255,255,255))
        title_rect = title.get_rect(center=(400,120))

        DISPLAYSURF.blit(title, title_rect)

        # 깜빡이는 문구
        current_time = pygame.time.get_ticks()

        if (current_time // 500) % 2 == 0:

            text = small_font.render(
                ">> PRESS THE MOUSE BUTTON <<",
                True,
                (255,255,255)
            )

            text_rect = text.get_rect(center=(400,520))

            DISPLAYSURF.blit(text, text_rect)

    # =====================================================
    # 설정 화면
    # =====================================================

    elif scene == "setting":

        DISPLAYSURF.fill((30,30,30))

        # 이름 입력
        name_text = font.render(
            f"이름(영어로 입력) : {player_name}",
            True,
            (255,255,255)
        )

        DISPLAYSURF.blit(name_text, (50,50))

        guide_text = small_font.render(
            "성별 선택 후 ENTER 를 누르면 시작",
            True,
            (180,180,180)
        )

        DISPLAYSURF.blit(guide_text, (50,90))

        # 게임 설명
        info1 = small_font.render(
            "교수님을 피해 외대를 탈출하세요.",
            True,
            (255,255,255)
        )

        info2 = small_font.render(
            "마우스로 이동할 수 있습니다.",
            True,
            (255,255,255)
        )


        DISPLAYSURF.blit(info1, (50,140))
        DISPLAYSURF.blit(info2, (50,170))


        # 남자 캐릭터
        DISPLAYSURF.blit(male_img, (170,230))

        # 여자 캐릭터
        DISPLAYSURF.blit(female_img, (480,230))

        # 선택 표시
        if selected_gender == "male":
            pygame.draw.rect(DISPLAYSURF, (0,255,0), male_rect, 5)

        if selected_gender == "female":
            pygame.draw.rect(DISPLAYSURF, (0,255,0), female_rect, 5)

    # =====================================================
    # 게임 시작 화면
    # =====================================================

    elif scene == "game":

        DISPLAYSURF.fill((0,0,0))

        start_text = font.render(
            f"{player_name} 게임 시작!",
            True,
            (255,255,255)
        )

        DISPLAYSURF.blit(start_text, (260,260))

    pygame.display.update()
    clock.tick(60)