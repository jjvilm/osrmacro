import remi.gui as gui
from remi import start, App
import xdot


class MyApp(App):
	def __init__(self, *args):
		super(MyApp, self).__init__(*args)
		
		
	
	def main(self):
		container = gui.VBox(width = 120, height = 100)
		
		self.drop_status = gui.Label('')
		self.drop_btn = gui.Button('DROP')
		self.drop_btn.style['background'] = 'teal'
		self.buttons = {'drop_btn': False}
	
		# setting the listener for the onclick event of the button
		self.drop_btn.set_on_click_listener(self, 'on_button_pressed')
	
		# appending a widget to another, the first argument is a string key
		container.append(self.drop_status)
		container.append(self.drop_btn)
	
		# returning the root widget
		return container
	
	# listener function
	def on_button_pressed(self):
		if not self.buttons['drop_btn']:
			self.buttons['drop_btn'] = True
			self.drop_btn.style['background'] = 'red'
			self.on_button_pressed()
		else:
			xdot.dropIt()
			self.drop_btn.style['background'] = 'teal'
        

# starts the webserver
if __name__ == "__main__":
    start(MyApp, address='127.0.0.1', start_browser=False)
