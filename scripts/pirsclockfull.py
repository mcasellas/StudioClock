 #!/usr/bin/python
import urllib 
import pygame , sys , math, time, os
import RPi.GPIO as GPIO
from pygame.locals import *
os.environ['SDL_VIDEODRIVER']="fbcon"

url_stream = 'http://streaming.enantena.com:8000/radiovoltrega128.mp3'

# Setting up the GPIO and inputs with pull up
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, GPIO.PUD_UP)

pygame.init()
bg = pygame.display.set_mode()

pygame.mouse.set_visible(False)

# Change colour to preference (R,G,B) 255 max value
bgcolour       = (0,     0,   0)
clockcolour    = (255, 255, 255)
ind1colour     = (255, 0,   0  )
ind2colour     = (255, 255, 0  )
ind3colour     = (0,   255, 0  )
ind4colour     = (0,   255, 255)
horaria        = (0,   150, 255)
offcolour      = (16,  16,  16 )
circular = (255, 255, 0  )

# Scaling to the right size for the display
digiclocksize  = int(bg.get_height()/3.5)
digiclockspace = int(bg.get_height()/10.5)
datapetita = int(bg.get_height()/10.5)
dotsize        = int(bg.get_height()/100)
hradius        = bg.get_height()/2.5
secradius      = hradius - (bg.get_height()/26)
indtxtsize     = int(bg.get_height()/5)
indtxtpetit     = int(bg.get_height()/7)
indboxy        = int(bg.get_height()/6)
indboxx        = int(bg.get_width()/2.5)

# Coords of items on display
xclockpos      = int(bg.get_width()*0.2875)
ycenter        = int(bg.get_height()/2)
xtxtpos        = int(bg.get_width()*0.75)
xindboxpos     = int(xtxtpos-(indboxx/2))
ind1y          = int((ycenter*0.4)-(indboxy/2))       
ind2y          = int((ycenter*0.8)-(indboxy/2))
ind3y          = int((ycenter*1.2)-(indboxy/2))
ind4y          = int((ycenter*1.6)-(indboxy/2))
txthmy         = int(ycenter-digiclockspace)
txtsecy        = int(ycenter+digiclockspace)
txtdata        = int(ycenter+int(bg.get_height()/4.5))
txtdia        = int(ycenter-int(bg.get_height()/4.5))

# Fonts  
clockfont     = pygame.font.Font(None,digiclocksize)
indfont       = pygame.font.Font(None,indtxtsize)
indfont1       = pygame.font.Font(None,indtxtpetit)
fontdata       = pygame.font.Font(None,datapetita)

# Indicator text - edit text in quotes to desired i.e. "MIC" will show MIC on display
ind2txt       = indfont.render("MIC ON",True,bgcolour)
ind1txt       = indfont1.render("TEMPS",True,bgcolour)
ind3txt       = indfont1.render("UNITAT MOBIL",True,bgcolour)
ind4txt       = indfont1.render("ERR. STREAM",True,bgcolour)

# Indicator positions
txtposind1 = ind1txt.get_rect(centerx=xtxtpos,centery=ycenter*0.4)
txtposind2 = ind2txt.get_rect(centerx=xtxtpos,centery=ycenter*0.8)
txtposind3 = ind3txt.get_rect(centerx=xtxtpos,centery=ycenter*1.2)
txtposind4 = ind4txt.get_rect(centerx=xtxtpos,centery=ycenter*1.6)

# Parametric Equations of a Circle to get the markers
# 90 Degree ofset to start at 0 seconds marker
# Equation for second markers
def paraeqsmx(smx):
	return xclockpos-(int(secradius*(math.cos(math.radians((smx)+90)))))

def paraeqsmy(smy):
	return ycenter-(int(secradius*(math.sin(math.radians((smy)+90)))))

# Equations for hour markers
def paraeqshx(shx):
	return xclockpos-(int(hradius*(math.cos(math.radians((shx)+90)))))

def paraeqshy(shy):
	return ycenter-(int(hradius*(math.sin(math.radians((shy)+90)))))
	
	
dies = ['Diumenge', 'Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres', 'Dissabte']

punt_horari = 0
code = 2
iniciar = 0
now = 0
start = 0
# This is where pygame does its tricks
while True :
	pygame.display.update()

	bg.fill(bgcolour)

	# Retrieve seconds and turn them into integers
	sectime = int(time.strftime("%S",time.localtime(time.time())))
	
	# To get the dots in sync with the seconds
	secdeg  = (sectime+1)*6

	# Draw second markers
	smx = smy = 0
	
	while smx < secdeg:
		pygame.draw.circle(bg, circular, (paraeqsmx(smx),paraeqsmy(smy)),dotsize)
		smy += 6  # 6 Degrees per second
		smx += 6

    # Draw hour markers
	shx = shy = 0
    
	while shx < 360:
		if shx > 329 and punt_horari == 1 :
			pygame.draw.circle(bg, circular, (paraeqshx(shx),paraeqshy(shy)),dotsize)
		else:
			pygame.draw.circle(bg, clockcolour, (paraeqshx(shx),paraeqshy(shy)),dotsize)
		
		shy += 30  # 30 Degrees per hour
		shx += 30
		
	# Retrieve time for digital clock
	retrievehm    = time.strftime("%H:%M",time.localtime(time.time()))
	retrievesec   = time.strftime("%S",time.localtime(time.time()))
	minut =  int(time.strftime("%M",time.localtime(time.time())))
	
	
	digiclockhm   = clockfont.render(retrievehm,True,clockcolour)
	digiclocksec  = clockfont.render(retrievesec,True,clockcolour)
	digiany  = fontdata.render(time.strftime("%d/%m/%Y"),True,clockcolour)
	digidia  = fontdata.render(dies[int(time.strftime("%w"))],True,clockcolour)
	
	
	# Align it
	txtposhm      = digiclockhm.get_rect(centerx=xclockpos,centery=txthmy)
	txtpossec     = digiclocksec.get_rect(centerx=xclockpos,centery=txtsecy)
	txtposdata     = digiany.get_rect(centerx=xclockpos,centery=txtdata)
	txtposdia     = digidia.get_rect(centerx=xclockpos,centery=txtdia)
	
	pygame.draw.rect(bg, offcolour,(xindboxpos, ind4y, indboxx, indboxy))
	# STREAMING 
	
	if int(retrievesec) == 01:
		code = urllib.urlopen(url_stream).getcode()
	
	if str(code).startswith('2') or str(code).startswith('3') :
		pygame.draw.rect(bg, offcolour,(xindboxpos, ind4y, indboxx, indboxy))
	else:
		if int(retrievesec) % 2: pygame.draw.rect(bg, offcolour,(xindboxpos, ind4y, indboxx, indboxy))
		else: pygame.draw.rect(bg, ind4colour,(xindboxpos, ind4y, indboxx, indboxy))
	
	
	# Mics On
	if GPIO.input(12):
		pygame.draw.rect(bg, offcolour,(xindboxpos, ind2y, indboxx, indboxy))
		iniciar = 0
	else:
		pygame.draw.rect(bg, ind1colour,(xindboxpos, ind2y, indboxx, indboxy))
		if iniciar == 0:
			start = time.time()
			iniciar = 1
	
		now = time.time()
	
	temps = time.strftime("%H:%M:%S",time.gmtime(now-start))

	ind1txt = indfont.render(temps,True,clockcolour)
	pygame.draw.rect(bg, bgcolour,(xindboxpos, ind1y, indboxx, indboxy))
	txtposind1 = ind1txt.get_rect(centerx=xtxtpos,centery=ycenter*0.4)
		
	if GPIO.input(13):
		pygame.draw.rect(bg, offcolour,(xindboxpos, ind3y, indboxx, indboxy))
	else:
		pygame.draw.rect(bg, ind2colour,(xindboxpos, ind3y, indboxx, indboxy))
		
    # S'acosta la horaria 
	if minut == 29 or minut == 59:
		
		ind4txt = indfont.render("HORARIA",True,clockcolour)
		txtposind4 = ind4txt.get_rect(centerx=xtxtpos,centery=ycenter*1.6)
		
		if int(retrievesec) % 2 == 0 :
			pygame.draw.rect(bg, bgcolour,(xindboxpos, ind4y, indboxx, indboxy))
			bgcolour = horaria
			
		else:
			pygame.draw.rect(bg, bgcolour,(xindboxpos, ind4y, indboxx, indboxy))
			bgcolour = (0,   0,   0  )
		
	else:
		
		ind4txt = indfont1.render("ERR. STREAM",True,bgcolour)
		txtposind4 = ind4txt.get_rect(centerx=xtxtpos,centery=ycenter*1.6)
	
	if minut > 54 and minut != 58:
		circular = ind3colour
		if minut > 58 :
			circular = ind1colour
	else :
		circular = ind2colour
		
	if minut == 59 or minut == 29 :
		punt_horari = 1
	else :
		punt_horari = 0
		
    # Render the text
	bg.blit(digiclockhm, txtposhm)
	bg.blit(digiclocksec, txtpossec)
	bg.blit(digiany, txtposdata)
	bg.blit(digidia, txtposdia)
	bg.blit(ind1txt, txtposind1)
	bg.blit(ind2txt, txtposind2)
	bg.blit(ind3txt, txtposind3)
	bg.blit(ind4txt, txtposind4)
	
	time.sleep(0.04)
	pygame.time.Clock().tick(25)
	for event in pygame.event.get() :
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		# Pressing q+t to exit
		elif event.type == KEYDOWN:
			if event.key == K_q and K_t:
				pygame.quit()
				sys.exit()
