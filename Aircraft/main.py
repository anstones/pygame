#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import random
import codecs
import pygame  
from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("飞机大战")
ic_launcher= pygame.image.load(r"resources/images/ic_launcher.png").convert_alpha()
pygame.display.set_icon(ic_launcher)

background = pygame.image.load(r"resources/images/background.png").convert_alpha()
# 游戏结束背景图
game_over = pygame.image.load(r'resources/images/gameover.png')
# 子弹图片
plane_bullet = pygame.image.load(r'resources/images/bullet.png')
# 飞机图片
player_img1= pygame.image.load(r'resources/images/player1.png')
player_img2= pygame.image.load(r'resources/images/player2.png')
player_img3= pygame.image.load(r'resources/images/player_off1.png')
player_img4= pygame.image.load(r'resources/images/player_off2.png')
player_img5= pygame.image.load(r'resources/images/player_off3.png')
# 敌机图片r
enemy_img1= pygame.image.load(r'resources/images/enemy1.png')
enemy_img2= pygame.image.load(r'resources/images/enemy2.png')
enemy_img3= pygame.image.load(r'resources/images/enemy3.png')
enemy_img4= pygame.image.load(r'resources/images/enemy4.png')


""" 
对文件的操作
写入文本:
传入参数为content，strim，path；content为需要写入的内容，数据类型为字符串。
path为写入的位置，数据类型为字符串。strim写入方式
传入的path需如下定义：path= r’ D:\text.txt’
f = codecs.open(path, strim, 'utf8')中，codecs为包，需要用impor引入。
strim=’a’表示追加写入txt，可以换成’w’，表示覆盖写入。
'utf8'表述写入的编码，可以换成'utf16'等。
"""
def write_txt(content, strim, path):
    f = codecs.open(path, strim, 'utf8')
    f.write(str(content))
    f.close()
"""
读取txt：
表示按行读取txt文件,utf8表 示读取编码为utf8的文件，可以根据需求改成utf16，或者GBK等。
返回的为数组，每一个数组的元素代表一行，
若想返回字符串格式，可以将改写成return ‘\n’.join(lines)
"""
def read_txt(path):
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    return lines


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        for i in range(len(player_rect)):
            self.image.append(player_rect[i].convert_alpha())

        self.rect = player_rect[0].get_rect()
        self.rect.topleft = init_pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False
        
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top =0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs , init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.down_imgs = enemy_down_imgs
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 2
        self.down_index = 0

    def move(self):
        self.rect.top += self.speed



def startGame():
    # 设置玩家飞机不同状态的图片列表，多张图片展示为动画效果
    player_rect = []
    # 玩家飞机图片
    player_rect.append(player_img1)
    player_rect.append(player_img2)
    # 玩家爆炸图片
    player_rect.append(player_img2)
    player_rect.append(player_img3)
    player_rect.append(player_img4)
    player_rect.append(player_img5)
    player_pos = [200, 600]
    # 初始化玩家飞机
    player = Player(player_rect, player_pos)
    # 子弹图片
    bullet_img = plane_bullet
    # 敌机不同状态的图片列表，多张图片展示为动画效果
    enemy1_img = enemy_img1
    enemy1_rect=enemy1_img.get_rect()
    enemy1_down_imgs = []
    enemy1_down_imgs.append(enemy_img1)
    enemy1_down_imgs.append(enemy_img2)
    enemy1_down_imgs.append(enemy_img3)
    enemy1_down_imgs.append(enemy_img4)
    # 储存敌机
    enemies1 = pygame.sprite.Group()
    # 存储被击毁的飞机，用来渲染击毁动画
    enemies_down = pygame.sprite.Group()
    # 初始化射击及敌机移动频率
    shoot_frequency = 0
    enemy_frequency = 0
    # 玩家飞机被击中后的效果处理
    player_down_index = 16
    # 初始化分数
    score = 0
    # 游戏循环帧率设置
    clock =pygame.time.Clock()
    running = True
    while running:
        screen.fill(0)
        screen.blit(background, (0,0))
        clock.tick(60)

        # 生成子弹，需要控制发射频率
        # 首先判断玩家飞机没有被击中
        if not player.is_hit:
            if shoot_frequency % 15 == 0:
                player.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= 15:
                shoot_frequency = 0
        for bullet in player.bullets:
            # 以固定速度移动子弹
            bullet.move()
            # 移动出屏幕后删除子弹
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        # 显示子弹
        player.bullets.draw(screen)
        # 生成敌机，需要控制生成频率
        if enemy_frequency % 50 == 0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0
        for enemy in enemies1:
            # 移动敌机
            enemy.move()
            # 敌机与玩家飞机碰撞效果处理 两个精灵之间的圆检测
            if pygame.sprite.collide_circle(enemy, player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit = True
                break
            # 移动出屏幕后删除飞机
            if enemy.rect.top < 0:
                enemies1.remove(enemy)
        # 敌机被子弹击中效果处理
        # 将被击中的敌机对象添加到击毁敌机 Group 中，用来渲染击毁动画
        # 方法groupcollide()是检测两个精灵组中精灵们的矩形冲突
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        # 遍历key值 返回的碰撞敌机
        for enemy_down in enemies1_down:
            # 点击销毁的敌机到列表
            enemies_down.add(enemy_down)
        # 绘制玩家飞机
        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            # 更换图片索引使飞机有动画效果
            player.img_index = shoot_frequency // 8
        else:
            # 玩家飞机被击中后的效果处理
            player.img_index = player_down_index // 8
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 47:
                # 击中效果处理完成后游戏结束
                running = False
        # 敌机被子弹击中效果显示
        for enemy_down in enemies_down:
            if enemy_down.down_index == 0:
                pass
            if enemy_down.down_index > 7:
                enemies_down.remove(enemy_down)
                score += 100
                continue
            #显示碰撞图片
            screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
            enemy_down.down_index += 1
        # 显示精灵
        enemies1.draw(screen)
        # 绘制当前得分
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (255, 255, 255))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 获取键盘事件（上下左右按键）
        key_pressed = pygame.key.get_pressed()
        # 处理键盘事件（移动飞机的位置）
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()


def ganeRanking():
    screen2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 绘制背景
    screen2.fill(0)
    screen2.blit(background, (0, 0))
    # 使用系统字体
    xtfont = pygame.font.SysFont('SimHei', 30)
    # 重新开始按钮
    textstart = xtfont.render('排行榜 ', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = 50
    screen.blit(textstart, text_rect)
    # 重新开始按钮
    textstart = xtfont.render('重新开始 ', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 120
    screen2.blit(textstart, text_rect)
    # 获取排行文档内容
    arrayscore = read_txt(r'score.txt')[0].split('mr')
    # 循环排行榜文件显示排行
    for i in range(0, len(arrayscore)):
        # 游戏 Game Over 后显示最终得分
        font = pygame.font.Font(None, 48)
        # 排名重1到10
        k=i+1
        text = font.render(str(k) +"  " +arrayscore[i], True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen2.get_rect().centerx
        text_rect.centery = 80 + 30*k
        # 绘制分数内容
        screen2.blit(text, text_rect)

startGame()

# 判断点击位置以及处理游戏推出
while True:
    for event in pygame.event.get():
        # 关闭页面游戏退出
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # 鼠标单击
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 判断鼠标单击的位置是否为开始按钮位置范围内
            if screen.get_rect().centerx - 70 <= event.pos[0] \
                    and event.pos[0] <= screen.get_rect().centerx + 50 \
                    and screen.get_rect().centery + 100 <= event.pos[1] \
                    and screen.get_rect().centery + 140 >= event.pos[1]:
                # 重新开始游戏
                startGame()
            # 判断鼠标是否单击排行榜按钮
            if screen.get_rect().centerx - 70 <= event.pos[0] \
                    and event.pos[0] <= screen.get_rect().centerx + 50 \
                    and screen.get_rect().centery + 160 <= event.pos[1] \
                    and screen.get_rect().centery + 200 >= event.pos[1]:
                # 显示排行榜
                gameRanking()
    # 更新界面
    pygame.display.update()