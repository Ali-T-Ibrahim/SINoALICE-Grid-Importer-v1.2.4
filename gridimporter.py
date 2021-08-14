import numpy as np
import cv2
import pyautogui
import weapons
import pygetwindow as gw
import gspread
import os
import re

def getIndex(pos):
    gridwin = gw.getWindowsWithTitle('MyGrid')[0]
    gx, gy = (gridwin.left, gridwin.top)
    x, y = (pos[0] - gx, pos[1] - gy)

    ###################ROW ONE###################
    if (x>17 and x<63) and (y>350 and y<394):
        return 0

    elif (x>106 and x<158) and (y>350 and y<394):
        return 1

    elif (x>202 and x<253) and (y>350 and y<394):
        return 2

    elif (x>293 and x<338) and (y>350 and y<394):
        return 3

    elif (x>388 and x<435) and (y>350 and y<394):
        return 4
    
    ###################ROW TWO###################
    elif (x>17 and x<63) and (y>444 and y<491):
        return 5

    elif (x>106 and x<158) and (y>444 and y<491):
        return 6

    elif (x>202 and x<253) and (y>444 and y<491):
        return 7

    elif (x>293 and x<338) and (y>444 and y<491):
        return 8

    elif (x>388 and x<435) and (y>444 and y<491):
        return 9

    ###################ROW THREE###################
    elif (x>17 and x<63) and (y>537 and y<582):
        return 10

    elif (x>106 and x<158) and (y>537 and y<582):
        return 11

    elif (x>202 and x<253) and (y>537 and y<582):
        return 12

    elif (x>293 and x<338) and (y>537 and y<582):
        return 13

    elif (x>388 and x<435) and (y>537 and y<582):
        return 14

    ###################ROW FOUR###################
    elif (x>17 and x<63) and (y>628 and y<672):
        return 15

    elif (x>106 and x<158) and (y>628 and y<672):
        return 16

    elif (x>202 and x<253) and (y>628 and y<672):
        return 17

    elif (x>293 and x<338) and (y>628 and y<672):
        return 18

    elif (x>388 and x<435) and (y>628 and y<672):
        return 19

def findWeapons(gridimg, window, weplist, Sclass, num):

    weapondict = {}
    if Sclass == 'Paladin':
        weapondict.update(weapons.spearsL)
        weapondict.update(weapons.spearsSR)
        weapondict.update(weapons.bowsL)
        weapondict.update(weapons.bowsSR)
        weapondict.update(weapons.swordsL)
        weapondict.update(weapons.swordsSR)
        weapondict.update(weapons.hammersL)
        weapondict.update(weapons.hammersSR)

    elif Sclass == 'Crusher':
        weapondict.update(weapons.hammersL)
        weapondict.update(weapons.hammersSR)
        weapondict.update(weapons.bowsL)
        weapondict.update(weapons.bowsSR)
        weapondict.update(weapons.spearsL)
        weapondict.update(weapons.spearsSR)
        weapondict.update(weapons.swordsL)
        weapondict.update(weapons.swordsSR)

    elif Sclass == 'Breaker':
        weapondict.update(weapons.swordsL)
        weapondict.update(weapons.swordsSR)
        weapondict.update(weapons.spearsL)
        weapondict.update(weapons.spearsSR)
        weapondict.update(weapons.hammersL)
        weapondict.update(weapons.hammersSR)
        weapondict.update(weapons.bowsL)
        weapondict.update(weapons.bowsSR)

    elif Sclass == 'Gunner':
        weapondict.update(weapons.bowsL)
        weapondict.update(weapons.bowsSR)
        weapondict.update(weapons.spearsL)
        weapondict.update(weapons.spearsSR)
        weapondict.update(weapons.hammersL)
        weapondict.update(weapons.hammersSR)
        weapondict.update(weapons.swordsL)
        weapondict.update(weapons.swordsSR)

    elif Sclass == 'Sorcerer':
        weapondict.update(weapons.booksL)
        weapondict.update(weapons.booksSR)
        weapondict.update(weapons.instrumentsL)
        weapondict.update(weapons.instrumentsSR)
        weapondict.update(weapons.orbsL)
        weapondict.update(weapons.orbsSR)
        weapondict.update(weapons.stavesL)
        weapondict.update(weapons.stavesSR)

    elif Sclass == 'Minstrel':
        weapondict.update(weapons.instrumentsL)
        weapondict.update(weapons.instrumentsSR)
        weapondict.update(weapons.booksL)
        weapondict.update(weapons.booksSR)
        weapondict.update(weapons.orbsL)
        weapondict.update(weapons.orbsSR)
        weapondict.update(weapons.stavesL)
        weapondict.update(weapons.stavesSR)

    elif Sclass == 'Cleric':
        weapondict.update(weapons.stavesL)
        weapondict.update(weapons.stavesSR)
        weapondict.update(weapons.orbsL)
        weapondict.update(weapons.orbsSR)
        weapondict.update(weapons.instrumentsL)
        weapondict.update(weapons.instrumentsSR)
        weapondict.update(weapons.booksL)
        weapondict.update(weapons.booksSR)
    
    gridwin = gw.getWindowsWithTitle('MyGrid')[0]
    prog = 0
    progbar = window.FindElement('-PROGRESS-')
    for wep in weapondict:
        #exit requirement
        if len(weplist) == num:
            progbar.UpdateBar(num)
            window.refresh()
            return
        
        img = cv2.imread(r'{}'.format(weapondict[wep][0]))
        width, height = (80, 80)
        gx, gy = (gridwin.left, gridwin.top)

        try:
            pos = pyautogui.locateOnScreen(img, region=(gx, gy+311, gx+490,
                                                gy+696),confidence=0.89)
        except:
            print('A problem has ocurred. Please try again.') 
        else:
            if pos != None:
                prog = prog + 1
                index = getIndex(pos)
                if wep[-2:] == 'LL':
                    weplist.append([wep[:-2], 'L', index])
                elif wep[-2:] == 'SR':
                    weplist.append([wep[:-2], 'SR', index])
                else:
                    weplist.append([wep[:-2], 'L', index])

                wepupdate = []
                for item in weplist:
                    wepupdate.append("{} {}".format(item[0], item[1]))
                x, y = (pos.left, pos.top)
                x = x - gx
                y = y - gy
                top_left = (x+30, y+5)
                gridimg = cv2.circle(gridimg, top_left, 25,(0,0,255), -1)
                cv2.imshow("MyGrid", gridimg)
                cv2.waitKey(1)
                window.FindElement('-WEPBOX-').Update(values=wepupdate)
                progbar.UpdateBar(prog)
                window.refresh()
        
def updateGrid(url, worksheet, weplist, Sclass):

    weplist.sort(key=lambda x: int(x[2]))
    gc = gspread.service_account(filename='f2x097.json')
    sh = gc.open_by_url(url)
    worksheet = sh.worksheet(worksheet)

    endcell = len(weplist)
    wepcells = worksheet.range('B3:B{}'.format(endcell + 2))
    rarcells = worksheet.range('C3:C{}'.format(endcell + 2))

    worksheet.update('C25:E25', Sclass)
    #worksheet.update('C29:E29', stats[0])
    #worksheet.update('C30:E30', stats[1])
    #worksheet.update('C31:E31', stats[2])
    #worksheet.update('C32:E32', stats[3])

    for i, val in enumerate(weplist):
        wepcells[i].value = val[0]
        rarcells[i].value = val[1]
    worksheet.update_cells(wepcells)
    worksheet.update_cells(rarcells)


def getStats():
    gridwin = gw.getWindowsWithTitle('MyGrid')[0]
    gx, gy = (gridwin.left, gridwin.top)
    
    patk = pyautogui.screenshot(region=(gx+252, gy+181,76,30))
    matk = pyautogui.screenshot(region=(gx+252, gy+215,76,30))
    pdef = pyautogui.screenshot(region=(gx+405, gy+184,76,30))
    mdef = pyautogui.screenshot(region=(gx+402, gy+215,76,30))

    patk = np.array(patk)
    matk = np.array(matk)
    pdef = np.array(pdef)
    mdef = np.array(mdef)

    patk = cv2.resize(patk, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    matk = cv2.resize(matk, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    pdef = cv2.resize(pdef, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    mdef = cv2.resize(mdef, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    patk = cv2.cvtColor(patk, cv2.COLOR_BGR2GRAY)
    matk = cv2.cvtColor(matk, cv2.COLOR_BGR2GRAY)
    pdef = cv2.cvtColor(pdef, cv2.COLOR_BGR2GRAY)
    mdef = cv2.cvtColor(mdef, cv2.COLOR_BGR2GRAY)

    patk = cv2.GaussianBlur(patk, (7, 7), 0)
    matk = cv2.GaussianBlur(matk, (7, 7), 0)
    pdef = cv2.GaussianBlur(pdef, (7, 7), 0)
    mdef = cv2.GaussianBlur(mdef, (7, 7), 0) 

    (thresh1, patk) = cv2.threshold(patk, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    (thresh2, matk) = cv2.threshold(matk, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    (thresh3, pdef) = cv2.threshold(pdef, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    (thresh4, mdef) = cv2.threshold(mdef, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    patk = pytesseract.image_to_string(patk, config='--psm 7')
    matk = pytesseract.image_to_string(matk, config='--psm 7')
    pdef = pytesseract.image_to_string(pdef, config='--psm 7')
    mdef = pytesseract.image_to_string(mdef, config='--psm 7')
        
    patk = int(re.sub("[^0-9]", "", patk))
    matk = int(re.sub("[^0-9]", "", matk))
    pdef = int(re.sub("[^0-9]", "", pdef))
    mdef = int(re.sub("[^0-9]", "", mdef))


    if len(str(patk)) < 5:
        patk = pyautogui.screenshot(region=(gx+252, gy+215,76,30))
        patk = np.array(patk)
        patk = cv2.resize(patk, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        patk = cv2.cvtColor(patk, cv2.COLOR_BGR2GRAY)
        patk = cv2.GaussianBlur(patk, (7, 7), 0)
        (thresh2, matk) = cv2.threshold(patk, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        patk = pytesseract.image_to_string(patk, config='--psm 13')
        patk = int(re.sub("[^0-9]", "", patk))

    if len(str(matk)) < 5:
        matk = pyautogui.screenshot(region=(gx+252, gy+215,76,30))
        matk = np.array(matk)
        matk = cv2.resize(matk, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        matk = cv2.cvtColor(matk, cv2.COLOR_BGR2GRAY)
        matk = cv2.GaussianBlur(matk, (7, 7), 0)
        (thresh2, matk) = cv2.threshold(matk, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        matk = pytesseract.image_to_string(matk, config='--psm 13')
        matk = int(re.sub("[^0-9]", "", matk))

    if len(str(pdef)) < 5:
        pdef = pyautogui.screenshot(region=(gx+252, gy+215,76,30))
        pdef = np.array(pdef)
        pdef = cv2.resize(pdef, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        pdef = cv2.cvtColor(pdef, cv2.COLOR_BGR2GRAY)
        pdef = cv2.GaussianBlur(pdef, (7, 7), 0)
        (thresh2, matk) = cv2.threshold(pdef, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        pdef = pytesseract.image_to_string(pdef, config='--psm 13')
        pdef = int(re.sub("[^0-9]", "", pdef))

    if len(str(mdef)) < 5:
        mdef = pyautogui.screenshot(region=(gx+252, gy+215,76,30))
        mdef = np.array(mdef)
        mdef = cv2.resize(mdef, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        mdef = cv2.cvtColor(mdef, cv2.COLOR_BGR2GRAY)
        mdef = cv2.GaussianBlur(mdef, (7, 7), 0)
        (thresh2, matk) = cv2.threshold(mdef, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        mdef = pytesseract.image_to_string(mdef, config='--psm 13')
        mdef = int(re.sub("[^0-9]", "", mdef))
        
    
    return (patk, matk, pdef, mdef)
    

#temp functions to make my life easier
def createDict(rootdir):
    dictionary = {}
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            dictionary[file[:-4]] = [r'{}'.format(os.path.join(subdir, file)), file[-6:-4]]
    return dictionary

def checkDict(wepdict):
    for wep in wepdict:
        img = cv2.imread(r'{}'.format(wepdict[wep][0]))
        if img is None:
            print(wep)
    

    

    
    

    
 

