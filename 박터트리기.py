import pygame
import random
import sys
from tkinter import Tk, messagebox

# 초기화
pygame.init()

# 게임 설정
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('박터트리기 게임')
clock = pygame.time.Clock()

# 색상
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

# 배경 이미지 로드 및 크기 조정
background = pygame.image.load("track.1.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# 버튼 이미지 로드
start_button_img = pygame.image.load("게임방법.박터트리기.png")  # 게임 시작 버튼 이미지
start_button_img = pygame.transform.scale(start_button_img, (500, 400))  # 크기 조정
start_button_rect = start_button_img.get_rect(center=(screen_width // 2, screen_height // 2))  # 버튼 위치 설정

# 중앙에 표시할 두 개의 이미지 로드
character1_img = pygame.image.load("플레이어_1박.png")  # 첫 번째 이미지
character2_img = pygame.image.load("플레이어_2박.png")  # 두 번째 이미지
character1_img = pygame.transform.scale(character1_img, (300, 200))
character2_img = pygame.transform.scale(character2_img, (300, 200))

# 글꼴 설정
font = pygame.font.SysFont(None, 48)

# 초기 점수 및 턴 설정
turns = 6
damage = 25
player1_score = 100
player2_score = 100

# 원 설정
circle_radius1 = 50
circle_radius2 = 50

def show_winner(player):
    root = Tk()
    root.withdraw()
    messagebox.showinfo("승리", f"플레이어 {player}가 승리했습니다!")
    root.destroy()

def draw_circle_and_text(color, text, x, y):
    pygame.draw.circle(screen, color, (x, y), circle_radius1 if color == blue else circle_radius2)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# 게임 시작 화면
def start_screen():
    running = True
    while running:
        screen.fill(white)
        screen.blit(background, (0, 0))  # 배경 이미지 그리기
        screen.blit(start_button_img, start_button_rect)  # 시작 버튼 그리기

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_x, mouse_y):  # 버튼 클릭 체크
                    running = False  # 게임 시작

# 게임 루프
def game_loop():
    global player1_score, player2_score, turns

    running = True
    while running and turns > 0 and player1_score > 0 and player2_score > 0:
        screen.fill(white)  # 배경을 흰색으로 채워서 초기화 (기존 이미지를 지우기 위해)
        screen.blit(background, (0, 0))  # 배경 이미지 그리기

        # 중앙에 두 이미지를 게임 내내 계속 표시
        screen.blit(character1_img, (screen_width // 2 - 200, screen_height // 2 - 100))
        screen.blit(character2_img, (screen_width // 2 + 100, screen_height // 2 - 100))

        # 랜덤 위치와 키 설정
        circle_x1 = random.randint(circle_radius1, screen_width - circle_radius1)
        circle_y1 = random.randint(circle_radius1, screen_height - circle_radius1)
        circle_x2 = random.randint(circle_radius2, screen_width - circle_radius2)
        circle_y2 = random.randint(circle_radius2, screen_height - circle_radius2)
        random_key1 = chr(random.randint(97, 122))  # 랜덤한 소문자 알파벳
        random_key2 = chr(random.randint(97, 122))  # 랜덤한 소문자 알파벳

        # 원과 키 그리기
        draw_circle_and_text(blue, random_key1, circle_x1, circle_y1)
        draw_circle_and_text(red, random_key2, circle_x2, circle_y2)

        pygame.display.flip()

        key_pressed = None
        while key_pressed is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    key_pressed = event.unicode
                    if key_pressed == random_key1:
                        player2_score -= damage
                        turns -= 1
                    elif key_pressed == random_key2:
                        player1_score -= damage
                        turns -= 1

        clock.tick(30)

        # 점수 표시
        score_text1 = font.render(f"플레이어 1 점수: {player1_score}", True, black)
        score_text2 = font.render(f"플레이어 2 점수: {player2_score}", True, black)
        screen.blit(score_text1, (50, 50))
        screen.blit(score_text2, (screen_width - 350, 50))
        pygame.display.flip()

        # 게임 종료 조건
        if player1_score <= 0:
            show_winner(2)
            running = False
        elif player2_score <= 0:
            show_winner(1)
            running = False

        if turns == 0:
            if player1_score > player2_score:
                show_winner(1)
            elif player2_score > player1_score:
                show_winner(2)
            else:
                show_winner("없음 (무승부)")
            running = False

# 게임 시작 화면 호출
start_screen()

# 게임 루프 시작
game_loop()

# 프로그램 종료
pygame.quit()
sys.exit()
