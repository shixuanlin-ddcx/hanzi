import pygame
import sys
import csv
import os

# 初始化 Pygame
pygame.init()

# 设置显示
width, height = 800, 600  # 根据原始屏幕大小调整
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("还原轨迹 - 分笔画")

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)

# 按钮字体
try:
    button_font = pygame.font.SysFont("simhei", 30)  # 使用 SimHei 支持中文
except:
    button_font = pygame.font.SysFont(None, 30)  # 回退到默认字体

# 按钮设置
exit_button_text = button_font.render("退出", True, WHITE)
exit_button_rect = pygame.Rect(width - 100, 10, 80, 40)
exit_button_color = RED

load_button_text = button_font.render("加载", True, WHITE)
load_button_rect = pygame.Rect(width - 200, 10, 80, 40)
load_button_color = GREEN

# 动态加载 CSV 文件
def load_csv(filename):
    stroke_points = []  # 存储分隔后的笔画
    current_stroke = []  # 当前笔画
    
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 检查是否为笔画分隔标记
                if row['timestamp'] == "STROKE_END":
                    if current_stroke and len(current_stroke) > 1:  # 只保存有两个以上点的笔画
                        stroke_points.append(current_stroke)
                    current_stroke = []  # 重置当前笔画
                    continue
                
                try:
                    x = float(row['x'])
                    y = float(row['y'])
                    current_stroke.append((x, y))
                except ValueError:
                    continue
                    
        # 添加最后一笔（如果有效）
        if current_stroke and len(current_stroke) > 1:
            stroke_points.append(current_stroke)
            
        return stroke_points
    except Exception as e:
        print(f"加载CSV文件失败: {e}")
        return []

# 主循环
clock = pygame.time.Clock()
running = True
screen.fill(WHITE)
stroke_points = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button_rect.collidepoint(event.pos):
                running = False
            elif load_button_rect.collidepoint(event.pos):
                print("请确保在相同目录下有一个draw_data_*.csv文件")
                
                # 查找最新的CSV文件
                csv_files = [f for f in os.listdir() if f.startswith('draw_data_') and f.endswith('.csv')]
                if csv_files:
                    csv_files.sort(key=os.path.getmtime, reverse=True)
                    filename = csv_files[0]
                    print(f"加载文件: {filename}")
                    
                    # 加载CSV数据
                    stroke_points = load_csv(filename)
                    
                    # 清屏并重新绘制
                    screen.fill(WHITE)
                    for stroke in stroke_points:
                        if len(stroke) > 1:  # 确保笔画有足够点
                            for i in range(1, len(stroke)):
                                # 绘制线段
                                pygame.draw.line(screen, BLACK, stroke[i-1], stroke[i], 2)
                else:
                    print("未找到draw_data_*.csv文件")

    # 绘制按钮
    pygame.draw.rect(screen, exit_button_color, exit_button_rect)
    screen.blit(exit_button_text, (exit_button_rect.x + 10, exit_button_rect.y + 5))
    pygame.draw.rect(screen, load_button_color, load_button_rect)
    screen.blit(load_button_text, (load_button_rect.x + 10, load_button_rect.y + 5))

    # 更新屏幕
    pygame.display.flip()
    clock.tick(60)

# 清理
pygame.quit()
sys.exit()