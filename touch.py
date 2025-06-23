import pygame
import csv
import time  # Added missing import
import sys
from datetime import datetime

# 初始化 Pygame
pygame.init()
# 添加笔画分隔逻辑
STROKE_THRESHOLD = 0.3  # 秒
# 获取显示器信息
displays = pygame.display.get_num_displays()
if displays > 1:
    # 如果有副屏，使用副屏全屏显示
    display_index = 1
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=display_index)
else:
    # 使用主屏，设置窗口大小
    pygame.display.set_mode((800, 600))

# 获取屏幕尺寸
screen = pygame.display.get_surface()
width, height = screen.get_size()

# 设置画布
screen.fill((255, 255, 255))  # 白色背景
pygame.display.set_caption("触摸绘制")

# 按钮字体
button_font = pygame.font.SysFont("simhei", 30)  # 使用 SimHei 支持中文

# 退出按钮设置
exit_button_text = button_font.render("退出", True, (255, 255, 255))
exit_button_rect = pygame.Rect(width - 100, 10, 80, 40)
exit_button_color = (255, 0, 0)  # 红色按钮

# 保存按钮设置
save_button_text = button_font.render("保存", True, (255, 255, 255))
save_button_rect = pygame.Rect(width - 200, 10, 80, 40)
save_button_color = (0, 128, 0)  # 绿色按钮

# 存储轨迹数据
draw_data = []
last_pos = None
drawing = False

# 主循环
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.FINGERDOWN:
            # 触摸按下
            x = int(event.x * width)
            y = int(event.y * height)
            # 检查按钮点击
            if exit_button_rect.collidepoint(x, y):
                running = False
            elif save_button_rect.collidepoint(x, y):
                # 保存轨迹到 CSV
                if draw_data:
                    csv_filename = f"draw_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    with open(csv_filename, 'w', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(['x', 'y', 'timestamp'])
                        for x, y, timestamp in draw_data:
                            csv_writer.writerow([x, y, timestamp])
                    draw_data.clear()  # 清空轨迹数据
                    screen.fill((255, 255, 255))  # 清空画布
            else:
                drawing = True
                last_pos = (x, y)
                # 记录触摸点
                timestamp = time.time()
                draw_data.append((x, y, timestamp))

        elif event.type == pygame.FINGERMOTION:
            # 触摸移动
            if drawing:
                x = int(event.x * width)
                y = int(event.y * height)
                if last_pos:
                    # 绘制线条
                    pygame.draw.line(screen, (0, 0, 0), last_pos, (x, y), 2)
                    timestamp = time.time()
                    draw_data.append((x, y, timestamp))
                last_pos = (x, y)

        elif event.type == pygame.FINGERUP:
            # 触摸抬起
            drawing = False
            last_pos = None

    # 绘制按钮
    pygame.draw.rect(screen, exit_button_color, exit_button_rect)
    screen.blit(exit_button_text, (exit_button_rect.x + 10, exit_button_rect.y + 5))
    pygame.draw.rect(screen, save_button_color, save_button_rect)
    screen.blit(save_button_text, (save_button_rect.x + 10, save_button_rect.y + 5))

    # 更新屏幕
    pygame.display.flip()
    clock.tick(60)

# 清理
pygame.quit()
sys.exit()