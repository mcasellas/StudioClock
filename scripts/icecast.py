import webbrowser
import pygame 
pygame.init()
bg = pygame.display.set_mode()

pygame.mouse.set_visible(False)


webbrowser.open('http://demo.devabroadcast.com:9780')
 
for event in pygame.event.get() :
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		# Pressing q+t to exit
		elif event.type == KEYDOWN:
			if event.key == K_q and K_t:
				pygame.quit()
				sys.exit()
