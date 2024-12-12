import pygame
import sys
import subprocess

# 초기화
pygame.init()

# 게임 설정
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('시작화면')
clock = pygame.time.Clock()

# 색상
white = (255, 255, 255)
black = (0, 0, 0)

# 글꼴 설정
font = pygame.font.SysFont(None, 48)

# 버튼 이미지 로드 및 크기 조정
button_img = pygame.image.load("시작.png")
button_img = pygame.transform.scale(button_img, (300, 100))

# 버튼 설정
button_width = button_img.get_width()
button_height = button_img.get_height()
button_x = (screen_width - button_width) // 2
button_y = (screen_height - button_height) // 2

# 배경 이미지 로드 및 크기 조정
background = pygame.image.load("track.1.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# 캐릭터 이미지 로드 및 크기 조정
character1_img = pygame.transform.scale(pygame.image.load("image.png"), (200, 200))
character2_img = pygame.transform.scale(pygame.image.load("캐릭터 2.png"), (200, 200))

# 타이틀 이미지 로드 및 크기 조정
title_img = pygame.image.load("로고.png")
title_img = pygame.transform.scale(title_img, (472, 262))

def draw_start_screen():
    screen.blit(background, (0, 0))  # 배경 이미지 그리기

    # 캐릭터 이미지 그리기
    screen.blit(character1_img, (100, 300))
    screen.blit(character2_img, (1000, 300))

    # 타이틀 이미지 그리기
    screen.blit(title_img, (button_x - 150, button_y - 250))

    # 버튼 이미지 그리기
    screen.blit(button_img, (button_x, button_y))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # 버튼 클릭 여부 확인
    if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
        if click[0] == 1:
            return True  # 버튼 클릭 시 True 반환

    pygame.display.flip()
    return False  # 버튼이 클릭되지 않으면 False 반환

def main():
    running = True
    game_started = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_started:
            game_started = draw_start_screen()
        else:

            subprocess.run(["python", "계주.py"])
            # 게임이 끝나면 종료
            running = False

        clock.tick(30)

if __name__ == "__main__":
    main()
