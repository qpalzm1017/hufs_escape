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
    pygame.display.set_caption("외대탈출 ROUND 4")

    font = pygame.font.Font("font/Galmuri11-Bold.ttf", 35)
    small_font = pygame.font.Font("font/Galmuri11-Bold.ttf", 20)

    # =========================
    # 이미지 불러오기
    # =========================
    background = pygame.image.load("image/Myeongsu_Lake.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    gameover_img = pygame.image.load("image/stage4_gameover.png").convert()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    ANIMAL_SIZE = 70
    duck_img = pygame.image.load("image/Duck.png").convert_alpha()
    duck_img = pygame.transform.scale(duck_img, (ANIMAL_SIZE, ANIMAL_SIZE))

    otter_img = pygame.image.load("image/Otter.png").convert_alpha()
    otter_img = pygame.transform.scale(otter_img, (ANIMAL_SIZE, ANIMAL_SIZE))

    # =========================
    # 변수
    # =========================
    scene = "game"
    otter_count = 0
    catch_goal = 3

    spawn_timer = 0
    spawn_cycle = 1000      
    visible_time = 500      
    emerge_time = 150       

    current_animal = None   
    animal_x = 0
    animal_y = 0
    is_clickable = False

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

            if scene == "game" and event.type == MOUSEBUTTONDOWN:
                if is_clickable and current_animal != None:
                    mx, my = event.pos
                    animal_rect = pygame.Rect(animal_x, animal_y, ANIMAL_SIZE, ANIMAL_SIZE)
                    
                    if animal_rect.collidepoint(mx, my):
                        if current_animal == "otter":
                            otter_count += 1
                            current_animal = None 
                            if otter_count >= catch_goal:
                                return "stage5"
                        elif current_animal == "duck":
                            scene = "gameover"

            elif scene == "gameover":
                if event.type == KEYDOWN:
                    scene = "game"
                    otter_count = 0
                    spawn_timer = 0
                    current_animal = None

        if scene == "game":
            DISPLAYSURF.blit(background, (0,0))
            score_text = font.render(f"수달 구조: {otter_count} / {catch_goal}", True, (255, 255, 255))
            DISPLAYSURF.blit(score_text, (30, 30))

            spawn_timer += dt
            if spawn_timer >= spawn_cycle:
                spawn_timer = 0
                animal_x = random.randint(250, 650)
                animal_y = random.randint(350, 480)
                
                if random.randint(1, 10) <= 6: current_animal = "otter"
                else: current_animal = "duck"

            if spawn_timer < visible_time and current_animal != None:
                is_clickable = True
                
                if spawn_timer < emerge_time:
                    ratio = spawn_timer / emerge_time
                elif spawn_timer > (visible_time - emerge_time):
                    ratio = (visible_time - spawn_timer) / emerge_time
                else:
                    ratio = 1.0
                    
                current_height = int(ANIMAL_SIZE * ratio)
                draw_y = animal_y + (ANIMAL_SIZE - current_height)
                crop_rect = (0, 0, ANIMAL_SIZE, current_height)
                
                if current_animal == "otter": target_img = otter_img
                else: target_img = duck_img
                    
                DISPLAYSURF.blit(target_img, (animal_x, draw_y), crop_rect)
            else:
                is_clickable = False

        elif scene == "gameover":
            DISPLAYSURF.blit(gameover_img, (0,0))
            retry_text = font.render("PRESS ANY KEY TO RETRY", True, (0,0,0))
            retry_rect = retry_text.get_rect(center=(400,520))
            DISPLAYSURF.blit(retry_text, retry_rect)

        pygame.display.update()
