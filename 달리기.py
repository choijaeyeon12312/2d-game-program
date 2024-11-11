import pygame
import sys
import tkinter as tk
from tkinter import messagebox
import threading

pygame.init()


screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('달리기 게임')


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


background = pygame.image.load("track.1.png")
background = pygame.transform.scale(background, (4500, 600))


character1 = pygame.Rect(50, 540, 50, 50)
character2 = pygame.Rect(50, 410, 50, 50)
character1_speed = 0
character2_speed = 0
speed_increase1 = 0
speed_increase2 = 0


key_press_times1 = []
key_press_times2 = []


clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()


finish_line = pygame.Rect(3000, 400, 10, 2000)  # 결승선의 y 좌표를 500으로, 높이를 100으로 조정


scroll_x = 0


character1_finish_time = None
character2_finish_time = None

def show_message(winner, elapsed_time):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("게임 종료", f"{winner}가 이겼습니다! 걸린 시간: {elapsed_time:.2f}초")
    root.destroy()


running = True
finished = False
extra_distance = 0
while running:
    screen.fill(WHITE)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_w:
                key_press_times1.append(pygame.time.get_ticks())
            elif event.key == pygame.K_COMMA:
                key_press_times2.append(pygame.time.get_ticks())


    current_time = pygame.time.get_ticks()
    key_press_times1 = [t for t in key_press_times1 if current_time - t < 500]
    key_press_times2 = [t for t in key_press_times2 if current_time - t < 500]
    speed_increase1 = len(key_press_times1)
    speed_increase2 = len(key_press_times2)


    if speed_increase1 > 0:
        character1_speed = 5 + speed_increase1
    else:
        character1_speed = 0

    if speed_increase2 > 0:
        character2_speed = 5 + speed_increase2
    else:
        character2_speed = 0

    character1.x += character1_speed
    character2.x += character2_speed


    if character1.colliderect(finish_line) and character1_finish_time is None:
        character1_finish_time = pygame.time.get_ticks() - start_time  # 첫 번째 캐릭터 도착 시간 기록
    if character2.colliderect(finish_line) and character2_finish_time is None:
        character2_finish_time = pygame.time.get_ticks() - start_time  # 두 번째 캐릭터 도착 시간 기록

    if character1_finish_time is not None and character2_finish_time is not None and not finished:
        finished = True
        if character1_finish_time < character2_finish_time:
            winner = "캐릭터 1"
            elapsed_time = character1_finish_time / 1000
        else:
            winner = "캐릭터 2"
            elapsed_time = character2_finish_time / 1000

        threading.Thread(target=show_message, args=(winner, elapsed_time)).start()


    if finished and extra_distance < 100:
        character1.x += 3  # 1의 속도로 이동
        character2.x += 3  # 1의 속도로 이동
        extra_distance += 3


    if character1.x > screen_width // 2:
        scroll_x = character1.x - screen_width // 2
    elif character2.x > screen_width // 2:
        scroll_x = character2.x - screen_width // 2


    screen.blit(background, (-scroll_x, 0))
    pygame.draw.rect(screen, BLACK, (character1.x - scroll_x, character1.y, character1.width, character1.height))
    pygame.draw.rect(screen, BLUE, (character2.x - scroll_x, character2.y, character2.width, character2.height))  # 두 번째 캐릭터 그리기
    pygame.draw.rect(screen, RED, (finish_line.x - scroll_x, finish_line.y, finish_line.width, finish_line.height))
    pygame.display.flip()

    
    clock.tick(60)

pygame.quit()
sys.exit()
