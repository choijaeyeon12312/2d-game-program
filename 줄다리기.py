import pygame
import sys
import random
from tkinter import Tk, messagebox
import subprocess

# 초기화
pygame.init()

# 게임 설정
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# 색상
white = (255, 255, 255)
black = (0, 0, 0)
brown = (150, 75, 0)

# 배경 이미지 로드 및 크기 조정
background = pygame.image.load("track.1.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# 캐릭터 이미지 로드 및 크기 조정
character1_img = pygame.transform.scale(pygame.image.load("캐릭터 1.png"), (50, 50))
character2_img = pygame.transform.scale(pygame.image.load("캐릭터2.오.png"), (50, 50))

# 원 설정
circle_radius1 = 50
circle_x1 = random.randint(circle_radius1, screen_width - circle_radius1)
circle_y1 = random.randint(circle_radius1, screen_height - circle_radius1)

circle_radius2 = 50
circle_x2 = random.randint(circle_radius2, screen_width - circle_radius2)
circle_y2 = random.randint(circle_radius2, screen_height - circle_radius2)

# 점수
score1 = 0
score2 = 0

# 줄의 초기 x 위치
line_x = screen_width // 2

# 글꼴 설정
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

def show_winner(player):
    root = Tk()
    root.withdraw()
    messagebox.showinfo("승리", f"플레이어 {player}가 승리했습니다!")
    root.destroy()
    subprocess.run(["python", "박터트리기.py"])  # 박터트리기.py 실행

def move_line(target_x):
    global line_x
    while line_x != target_x:
        if line_x < target_x:
            line_x += 5
        elif line_x > target_x:
            line_x -= 5

        # 화면 업데이트
        screen.blit(background, (0, 0))

        # 캐릭터 이미지 그리기
        for i in range(5):
            screen.blit(character1_img, (100 + i * 60, screen_height - 100))
            screen.blit(character2_img, (800 + i * 60, screen_height - 100))

        # 원 그리기
        pygame.draw.circle(screen, white, (circle_x1, circle_y1), circle_radius1)
        pygame.draw.circle(screen, white, (circle_x2, circle_y2), circle_radius2)

        # 원 안에 텍스트 그리기
        q_text = small_font.render('Q', True, black)
        comma_text = small_font.render('<', True, black)
        screen.blit(q_text, (circle_x1 - q_text.get_width() // 2, circle_y1 - q_text.get_height() // 2))
        screen.blit(comma_text, (circle_x2 - comma_text.get_width() // 2, circle_y2 - comma_text.get_height() // 2))

        # 점수 표시
        score_text1 = font.render(f"플레이어 1 점수: {score1}", True, black)
        score_text2 = font.render(f"플레이어 2 점수: {score2}", True, black)
        screen.blit(score_text1, (10, 10))
        screen.blit(score_text2, (screen_width - 300, 10))

        # 줄 그리기
        line_y = screen_height - 70
        pygame.draw.line(screen, brown, (line_x - 500, line_y), (line_x + 500, line_y), 5)

        pygame.display.flip()
        clock.tick(60)

# 점수 계산 함수
def calculate_score(radius):
    return max(1, 51 - radius)  # 원의 크기에 따른 점수 계산

# 시작 화면 처리
def start_screen(screen, background):
    button_img = pygame.image.load("게임방법.줄다리기.png")  # 버튼 이미지 파일 경로
    button_img = pygame.transform.scale(button_img, (500, 400))  # 버튼 이미지 크기 조정
    button_rect = button_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))  # 버튼 위치 설정

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 버튼 클릭 체크
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_x, mouse_y):  # 버튼 영역 클릭
                    running = False  # 게임 시작

        # 화면에 배경 그리기
        screen.fill(white)
        screen.blit(background, (0, 0))  # 배경 그림
        screen.blit(button_img, button_rect)  # 버튼 그림
        pygame.display.flip()

# 게임 루프
def game_loop():
    global score1, score2, line_x, circle_radius1, circle_radius2, circle_x1, circle_y1, circle_x2, circle_y2
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # 플레이어 1 (Q 키) - Q만 눌렀을 때
        if keys[pygame.K_q]:
            if circle_radius1 <= 50:
                score1 += calculate_score(circle_radius1)
                circle_radius1 = 50
                circle_x1 = random.randint(circle_radius1, screen_width - circle_radius1)
                circle_y1 = random.randint(circle_radius1, screen_height - circle_radius1)
                line_x -= 20

        # 플레이어 2 (, 키) - ,만 눌렀을 때
        if keys[pygame.K_COMMA]:
            if circle_radius2 <= 50:
                score2 += calculate_score(circle_radius2)
                circle_radius2 = 50
                circle_x2 = random.randint(circle_radius2, screen_width - circle_radius2)
                circle_y2 = random.randint(circle_radius2, screen_height - circle_radius2)
                line_x += 20

        # 동시에 Q와 , 키가 눌렸을 때 - 각 키를 개별적으로 처리
        if keys[pygame.K_q] and keys[pygame.K_COMMA]:
            if circle_radius1 <= 50:
                score1 += calculate_score(circle_radius1)
                circle_radius1 = 50
                circle_x1 = random.randint(circle_radius1, screen_width - circle_radius1)
                circle_y1 = random.randint(circle_radius1, screen_height - circle_radius1)
                line_x -= 20

            if circle_radius2 <= 50:
                score2 += calculate_score(circle_radius2)
                circle_radius2 = 50
                circle_x2 = random.randint(circle_radius2, screen_width - circle_radius2)
                circle_y2 = random.randint(circle_radius2, screen_height - circle_radius2)
                line_x += 20

        # 화면 업데이트
        screen.blit(background, (0, 0))

        # 캐릭터 이미지 그리기
        for i in range(5):
            screen.blit(character1_img, (100 + i * 60, screen_height - 100))
            screen.blit(character2_img, (800 + i * 60, screen_height - 100))

        # 원 그리기
        pygame.draw.circle(screen, white, (circle_x1, circle_y1), circle_radius1)
        pygame.draw.circle(screen, white, (circle_x2, circle_y2), circle_radius2)

        # 원 안에 텍스트 그리기
        q_text = small_font.render('Q', True, black)
        comma_text = small_font.render('<', True, black)
        screen.blit(q_text, (circle_x1 - q_text.get_width() // 2, circle_y1 - q_text.get_height() // 2))
        screen.blit(comma_text, (circle_x2 - comma_text.get_width() // 2, circle_y2 - comma_text.get_height() // 2))

        # 점수 표시
        score_text1 = font.render(f"플레이어 1 점수: {score1}", True, black)
        score_text2 = font.render(f"플레이어 2 점수: {score2}", True, black)
        screen.blit(score_text1, (10, 10))
        screen.blit(score_text2, (screen_width - 300, 10))

        if abs(score1 - score2) >= 40:
            if score1 > score2:
                move_line(0)
                show_winner(1)
            else:
                move_line(screen_width)
                show_winner(2)
            running = False

        # 줄 그리기
        line_y = screen_height - 70
        pygame.draw.line(screen, brown, (line_x - 500, line_y), (line_x + 500, line_y), 5)

        pygame.display.flip()

        # 원 크기 조절
        circle_radius1 -= 0.5
        circle_radius2 -= 0.5
        if circle_radius1 <= 0:
            circle_radius1 = 50
            circle_x1 = random.randint(circle_radius1, screen_width - circle_radius1)
            circle_y1 = random.randint(circle_radius1, screen_height - circle_radius1)
        if circle_radius2 <= 0:
            circle_radius2 = 50
            circle_x2 = random.randint(circle_radius2, screen_width - circle_radius2)
            circle_y2 = random.randint(circle_radius2, screen_height - circle_radius2)

        clock.tick(30)

# 게임 시작 화면
start_screen(screen, background)

# 게임 루프 시작
game_loop()

# 프로그램 종료
pygame.quit()
sys.exit()
