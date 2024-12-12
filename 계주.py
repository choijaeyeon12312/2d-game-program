import pygame
import sys
import tkinter as tk
from tkinter import messagebox
import threading
import subprocess

def draw_start_screen(screen, background, button_rect, button_img):
    screen.blit(background, (0, 0))  # 배경 이미지 그리기
    screen.blit(button_img, button_rect)  # 버튼 이미지 그리기

    pygame.display.flip()

def start_screen(screen, background):
    button_img = pygame.image.load("게임방법 계주.png")  # 버튼 이미지 파일 경로
    button_img = pygame.transform.scale(button_img, (500, 400))  # 버튼 이미지 크기 조정
    button_rect = button_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    waiting = True
    while waiting:
        draw_start_screen(screen, background, button_rect, button_img)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    waiting = False

        pygame.display.flip()

    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))  # 검은색 배경
        font = pygame.font.SysFont(None, 72)
        text = font.render(str(i), True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1000)  # 1초 대기

    play(screen, background)

def show_message(winner, elapsed_time):
    root = tk.Tk()
    root.withdraw()
    result = messagebox.showinfo("게임 종료", f"{winner}가 이겼습니다! 걸린 시간: {elapsed_time:.2f}초")
    root.destroy()

    if result == "ok":
        subprocess.run(["python", "줄다리기.py"])  # 줄다리기.py 실행

def play(screen, background):
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    character1_img = pygame.image.load("캐릭터 1.png")  # 캐릭터 1 이미지 파일 경로
    character1_img = pygame.transform.scale(character1_img, (50, 50))
    character2_img = pygame.image.load("캐릭터 2.png")  # 캐릭터 2 이미지 파일 경로
    character2_img = pygame.transform.scale(character2_img, (50, 50))

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

    finish_line = pygame.Rect(3000, 400, 10, 2000)  # 결승선의 y 좌표를 400으로, 높이를 2000으로 조정

    scroll_x = 0

    character1_finish_time = None
    character2_finish_time = None

    running = True
    finished = False
    extra_distance = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_w:
                    key_press_times1.append(pygame.time.get_ticks())
                elif event.key == pygame.K_COMMA or event.key == pygame.K_PERIOD:
                    key_press_times2.append(pygame.time.get_ticks())

        # 현재 시간이 얼마인지를 추적
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
            character1.x += 3  # 3의 속도로 이동
            character2.x += 3  # 3의 속도로 이동
            extra_distance += 3

        # 스크롤 위치 업데이트
        if character1.x > screen.get_width() // 2:
            scroll_x = character1.x - screen.get_width() // 2
        elif character2.x > screen.get_width() // 2:
            scroll_x = character2.x - screen.get_width() // 2

        screen.fill(WHITE)

        # 배경 이미지 반복 그리기
        rel_x = scroll_x % background.get_rect().width
        screen.blit(background, (-rel_x, 0))
        if rel_x < screen.get_width():
            screen.blit(background, (screen.get_width() - rel_x, 0))

        screen.blit(character1_img, (character1.x - scroll_x, character1.y))  # 캐릭터 1 이미지 그리기
        screen.blit(character2_img, (character2.x - scroll_x, character2.y))  # 캐릭터 2 이미지 그리기
        pygame.draw.rect(screen, RED, (finish_line.x - scroll_x, finish_line.y, finish_line.width, finish_line.height))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption('계주')
    background = pygame.image.load("track.1.png")
    background = pygame.transform.scale(background, (1200, 600))
    start_screen(screen, background)
