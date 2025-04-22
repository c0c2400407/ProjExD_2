import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんrectまたは爆弾rect
    戻り値：判定結果タプル（横、縦）
    画面内ならtrue,画面外ならfalse
    """
    yoko, tate = True, True#横と縦の変数
    #yokohanntei

    if rct.left < 0 or WIDTH < rct.right: #画面内だったら
        yoko = False
    #tatehanntei
    if rct.top < 0 or HEIGHT < rct.bottom: #画面内だったら
        tate = False
    return yoko, tate


    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    #こうかとん初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5



    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        #gameover
        #bm_img = pg.image.load("fig/black.png")
        #screen1 = pg.display.set_mode((1100, 650))
        #screen.blit(bm_img, [1100, 650])
        #bm_img = pg.Surface((1100, 650))
        #pg.draw.rect(bm_img, (0, 0, 0), 20,20)
        #bm_rct = bm_img.get_rect()
        #bm_rct.center = 1100, 650
        #screen1.blit(bm_img, bm_rct)
        #screen1 = time.sleep(5)

        #bb_img.set_colorkey((0, 0, 0))

        #pg.rect(bm_img, 0, 1100, 650)


        #こうかとんrectと爆弾rectが重なったら
        if kk_rct.colliderect(bb_rct,):
            font = pg.font.Font(None, 74)  # フォントサイズ74
            screen.fill((0, 0, 0))

            text = font.render("Game Over", True, (255, 255, 255))  # 白いテキスト
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # 中央に配置

            screen.blit(text, text_rect) 
            pg.display.update()
            time.sleep(5) 
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]#合計移動量の蓄積  

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]#左右方向
                sum_mv[1] += mv[1]#上下方向

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):#画面の外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])#画面内に戻す

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)#爆弾の移動


        yoko, tate = check_bound(bb_rct)
        if not yoko:#左右のどちらかにはみ出ていたら
            vx *= -1
        if not tate:#上下方向に
            vy *= -1
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
