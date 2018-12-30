#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#・プロジェクト：自動迷路生成・探索
#・作成日：2017/01/?
#
#・自動で迷路を生成する。（穴掘り法）
#・マス目の作成
#・スタック
#-------------------------------------------------------------------------------

import sys, random
sys.setrecursionlimit(10000)
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

NUM = 39
ROUTE = 0
BLOCK = 1
END = 2
PASSED = 3

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.myInit()
        
    def myInit(self):
        self.setGeometry(300, 200, 1200, 1000)
        self.setWindowTitle('Maze')
        self.init = 1
        self.solveInit = 1
        
        self.field = [[BLOCK for i in range(NUM)] for j in range(NUM)] #迷路の初期化
        
        #---graphicsview使うときはここ--------------
        #self.graphicsview = QGraphicsView(self)
        #scene = QGraphicsScene(self.graphicsview)
        #Scene.setSceneRect(10, 10, 500, 500)
        #self.graphicsview.setScene(scene)
        #-------------------------------------------
        
        
        self.sPosX = 0
        self.sPosY = 0
        
        #---ボタン設定----------------------------------
        self.btnCreate = QPushButton('Create', self)
        self.btnCreate.clicked.connect(lambda:self.createMaze(0, 0)) 
        self.btnCreate.move(1000, 50)
        
        self.btnSolve = QPushButton('Solve', self)
        self.btnSolve.clicked.connect(self.solveMaze)
        self.btnSolve.move(1000, 100)
        
        self.btnReset = QPushButton('Reset', self)
        self.btnReset.clicked.connect(self.resetMaze)
        self.btnReset.move(1000, 150)
        
        #self.btnNext = QPushButton('Next', self)
        #self.btnNext.clicked.connect(lambda:self.createMaze(self.sPosX, self.sPosY))
        #self.btnNext.move(800, 200)
        #-----------------------------------------------
        
        self.createMaze(0, 0)
       
    def createMaze(self, sPosX, sPosY):
        #time.sleep(0.1)
        #---最初の動作-----------------------------------
        if self.init == 1:
            #self.startX = random.randint(1, (NUM - 1) / 2) * 2 - 1
            #self.startY = random.randint(1, (NUM - 1)/ 2) * 2 - 1
            self.startX = 1
            self.startY = 1
            self.field[self.startX][self.startY] = ROUTE
            
            self.sPosX = self.startX
            self.sPosY = self.startY
        
            self.digDataX = [self.sPosX]
            self.digDataY = [self.sPosY]
            
            self.init = 0
            self.endDig = 0
            self.digCount = 0
            
            self.update()
            
            return self.createMaze(self.sPosX, self.sPosY)
            
        #-------------------------------------------------
        
        #---穴掘りの部分。方向を一つ決めて、そこから順番に掘れるかどうかを試す。---------------------------------------------------------------------------------------------------------------
        self.direction = random.randint(0, 3) 
        self.count = 0
        
        while self.count < 4:
            if self.direction == 0:
                self.directionX = 0
                self.directionY = 1
            elif self.direction == 1:
                self.directionX = 1
                self.directionY = 0
            elif self.direction == 2:
                self.directionX = 0
                self.directionY = -1
            else:
                self.directionX = -1
                self.directionY = 0
            
            #2マス先がリストの範囲に収まっているか、次にそこが壁かどうか調べて、壁ならそこまで掘る。
            if ((sPosX + self.directionX * 2) >= 0) and ((sPosY + self.directionY * 2) >= 0) and ((sPosX + self.directionX * 2) <= (NUM - 1)) and ((sPosY + self.directionY * 2) <= (NUM - 1)):
                if self.field[sPosX + self.directionX * 2][sPosY + self.directionY * 2] == BLOCK:
                    self.field[sPosX + self.directionX][sPosY + self.directionY] = 0
                    self.field[sPosX + self.directionX * 2][sPosY + self.directionY * 2] = ROUTE

                    #2マス先をスタートにする
                    self.sPosX = sPosX + self.directionX * 2 
                    self.sPosY = sPosY + self.directionY * 2
                    #現在の位置をスタックに
                    self.digDataX.append(self.sPosX)
                    self.digDataY.append(self.sPosY)
                    
                    self.count = 0
                    self.update()
                    
                    self.digCount += 1
        
                    return self.createMaze(self.sPosX, self.sPosY)
                else:
                    self.count += 1
            else:
                self.count += 1
            
            #次の方向に
            self.direction += 1
            
            #directionが3の次は0に戻す
            if self.direction == 4:
                self.direction = 0
        #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
        
        #スタックにある掘り始めの座標から一つ選び、次のスタートにする。
        if len(self.digDataX) > 1:
            self.i = random.randint(0, len(self.digDataX) - 1)
            self.sPosX = self.digDataX[self.i]
            self.sPosY = self.digDataY[self.i]
        
        #print(self.digCount)
        
        #200回以上掘ったら終わり
        if self.digCount > 355:
            print(self.digCount)
            self.endDig = 1
            self.chooseEnd()
            self.update()
            return
            
        else:
            return self.createMaze(self.sPosX, self.sPosY)      
             
    def resetMaze(self):
        self.init = 1
        self.endDig = 0
        
        for x in range(0, NUM):
            for y in range(0, NUM):
                self.field[x][y] = 1
                
        self.update()
    
    #右下3*3マスのうちのどれかをゴールにする
    def chooseEnd(self):
        while 1:
            x = random.randint(NUM - 4, NUM - 2)
            y = random.randint(NUM - 4, NUM - 2)
            if self.field[x][y] == ROUTE:
                self.field[x][y] = END
                self.endX = x
                self.endY = y
                break
    
                
    def chooseDirection(self):
        #---次に穴を掘る方向を決める----------------------
        self.direction = random.randint(1, 4)
        if self.direction == 1:
            self.directionX = 0
            self.directionY = 1
        elif self.direction == 2:
            self.directionX = 1
            self.directionY = 0
        elif self.direction == 3:
            self.directionX = 0
            self.directionY = -1
        else:
            self.directionX = -1
            self.directionY = 0
        #--------------------------------------------------
        
    def solveMaze(self, pPosX, pPosY):
        if self.solveInit == 1:
            self.pPosX = self.startX
            self.pPosY = self.startY
            self.routeDataX = [self.pPosX]
            self.routeDataY = [self.pPosX]
            self.solveInit = 0
            
            return self.solveMaze(self.pPosX, self.pPosY)
            
        self.direction = random.randint(0, 3)
        if self.direction == 0:
            self.directionX = 0
            self.directionY = 1
        elif self.direction == 1:
            self.directionX = 1
            self.directionY = 0
        elif self.direction == 2:
            self.directionX = 0
            self.directionY = -1
        else:
            self.directionX = -1
            self.directionY = 0
            
        while self.count < 4:
            if self.direction == 0:
                self.directionX = 0
                self.directionY = 1
            elif self.direction == 1:
                self.directionX = 1
                self.directionY = 0
            elif self.direction == 2:
                self.directionX = 0
                self.directionY = -1
            else:
                self.directionX = -1
                self.directionY = 0
            
            
            
            if self.field[pPosX + self.directionX][pPosY + self.directionY] == ROUTE:
                self.field[pPosX + self.directionX][pPosY + self.directionY] = PASSED

                #2マス先をスタートにする
                self.pPosX = pPosX + self.directionX 
                self.pPosY = pPosY + self.directionY 
                #現在の位置をスタックに
                self.routeDataX.append(self.pPosX)
                self.routeDataY.append(self.pPosY)
                    
                self.count = 0
                self.update()
       
                return self.solveMaze(self.pPosX, self.pPosY)
            else:
                self.count += 1
            
            
            #次の方向に
            self.direction += 1
            
            #directionが3の次は0に戻す
            if self.direction == 4:
                self.direction = 0
        #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
        
            
        
            
        
        
        
    def paintEvent(self, event):
        painter = QPainter(self) #selfつけたらだめ！
        painter.setPen(Qt.gray)
        painter.setBrush(Qt.black)
         
        for y in range(0, NUM):
            for x in range(0, NUM):
                if self.field[x][y] == BLOCK:
                    painter.drawRect(10 + 21 * x, 10 + 21 * y , 20, 20) #21にしているのは正方形の各辺が重なるとエラーになるから←なりません！！！
        
        #スタート位置を青に塗る
        if self.init == 0:
            painter.setBrush(Qt.blue)
            painter.drawRect(10 + 21 * self.startX, 10 + 21 * self.startY, 20, 20)
        #ゴール位置を赤に塗る
        if self.endDig == 1:
            painter.setBrush(Qt.red)
            painter.drawRect(10 + 21 * self.endX, 10 + 21 * self.endY, 20, 20)
            
            painter.setBrush(Qt.yellow)
            painter.drawRect(14 + 21 * self.startX, 14 + 21 * self.startY, 12, 12)
                    
            #self.painter.fillRect(10, 32 + 21 * j, 20, 20, Qt.black)
            #self.painter.fillRect(409, 32 + 21 * j, 20, 20, Qt.black)
            
if __name__ == "__main__":
    print('start')
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
    
