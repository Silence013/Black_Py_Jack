import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont, ImageShow
from adafruit_rgb_display import st7789
# Create the display
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT


# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

udlr_fill = "#00FF00"
udlr_outline = "#00FFFF"
button_fill = "#FF00FF"
button_outline = "#FFFFFF"
message = ""

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

option_a_selected = False
option_b_selected = False

class DisplayController:
    def __init__(self, width, height, cs_pin, dc_pin, reset_pin, backlight_pin):
        self.width = width
        self.height = height
        
        # Create the display
        self.cs_pin = DigitalInOut(cs_pin)
        self.dc_pin = DigitalInOut(dc_pin)
        self.reset_pin = DigitalInOut(reset_pin)
        self.backlight = DigitalInOut(backlight_pin)

        BAUDRATE = 24000000
        self.spi = board.SPI()
        self.disp = st7789.ST7789(
            self.spi,
            height=self.height,
            y_offset=80,
            rotation=180,
            cs=self.cs_pin,
            dc=self.dc_pin,
            rst=self.reset_pin,
            baudrate=BAUDRATE,
        )

        # Input pins:
        self.button_A = DigitalInOut(board.D5)
        self.button_A.direction = Direction.INPUT

        self.button_B = DigitalInOut(board.D6)
        self.button_B.direction = Direction.INPUT

        self.button_U = DigitalInOut(board.D17)
        self.button_U.direction = Direction.INPUT

        self.button_D = DigitalInOut(board.D22)
        self.button_D.direction = Direction.INPUT

        # Turn on the Backlight
        self.backlight.switch_to_output()
        self.backlight.value = True

        # Create blank image for drawing.
        self.image = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

        # Default font
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        png_path = "/home/kau-esw/ESW/png/" + png_path

    def draw_png(self, png_path, x=0, y=0):
        png_image = Image.open(png_path).resize((50,73))
        #.convert("RGB")
        self.image.paste(png_image, (x, y), png_image)

    def update_display(self):
        # Display the Image
        self.disp.image(self.image)

    def clear_display(self):
        # Clear the Image
        self.image = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def set_font(self, font_path, size):
        self.font = ImageFont.truetype(font_path, size)

    def draw_text(self, text, position, fill_color):
        self.draw.text(position, text, font=self.font, fill=fill_color)

# Example usage:
# display = DisplayController(width, height, cs_pin, dc_pin, reset_pin, backlight_pin)
# display.draw_png("example.png", x=50, y=50)
# display.draw_text("Hello!", (10, 10), fill_color=(255, 255, 255))
# display.update_display()
# time.sleep(5)  # Display for 5 seconds
# display.clear_display()

def BPJ(deletecard):
    deck = []
    suits = ['diamonds','spades', 'hearts', 'clubs']
    ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
    deletecard = deletecard
    
    if deletecard == '1':
        suits = ['clubs', 'hearts']

    for suit in suits:
        for rank in ranks:
            deck.append(rank + '_' + 'of' + '_' + suit)


    #카드 셔플링 함수
    def shuffle_deck():
        random.shuffle(deck)

    #카드 한 장 뽑는 함수
    def deal_card():
        return deck.pop()

    #점수 계산 함수
    def calculate_hand(hand):
        score = 0
        num_aces = 0
        for card in hand:
            rank = card.split('_')[0]
            if rank == 'ace':
                num_aces += 1
                score += 11
            elif rank in ['jack', 'queen', 'king']:
                score += 10
            else:
                score += int(rank)
        while num_aces > 0 and score > 21:
            score -= 10
            num_aces -= 1
        return score

    def display_player_hand(player_hand):
        png = '.png'
        path = '/home/kau-esw/ESW/png/'
        x_position = 0
        player_score = calculate_hand(player_hand)
        
        message = 'Player score: \n' + str(player_score)
        draw.rectangle((10, 10, width-10, (height//2)-10), outline=0, fill=(255, 255, 255))
        draw.text((20, 30), message, font=fnt, fill=0)
        disp.image(image)
        for card in player_hand:
            img = Image.open(path + card + png).resize((75, 110))
            disp.image(img, x=x_position, y=10)
            x_position += 13
            time.sleep(0.01)
    
    #게임 실행 함수
    def play_game():
        
        shuffle_deck()
        player_hand = [deal_card(),deal_card()]
        dealer_hand = [deal_card(),deal_card()]
        #플레이어 턴
        while True:
            player_score = calculate_hand(player_hand)
            display_player_hand(player_hand)
            time.sleep(3)
            if player_score > 21:
                print('Bust! You lose!')
                message = 'Player score: \n' + str(player_score) + '\nBust! \nYou lose!'
                draw.rectangle((10, 10, width-10, (height)-20), outline=0, fill=(255, 255, 255))
                draw.text((20, 30), message, font=fnt, fill=0)
                disp.image(image)
                time.sleep(5)
                draw.rectangle((0, 0, width, height), outline=0, fill=(4,22,7))
                disp.image(image)
                return
            elif player_score == 21:
                print('Blackjack! You win!')
                message = 'Player score: \n' + str(player_score) + '\nBlackjack! \nYou Win!'
                draw.rectangle((10, 10, width-10, (height)-20), outline=0, fill=(255, 255, 255))
                draw.text((20, 30), message, font=fnt, fill=0)
                disp.image(image)
                time.sleep(5)
                draw.rectangle((0, 0, width, height), outline=0, fill=(4,22,7))
                disp.image(image)
                return
            else:
                if not button_A.value:
                    player_hand.append(deal_card())
                elif not button_B.value:
                    break
                
        #딜러 턴
        while True:
            print('Dealer hand:', dealer_hand)
            dealer_score = calculate_hand(dealer_hand)
            print('Dealer score:', dealer_score)
            if dealer_score > 21:
                print('Dealer bust! You win!')
                message = 'Player score: \n' + str(player_score) + '\nDealer hand: \n' + str(dealer_score) + '\nDealer bust!\nYou win!'
                draw.rectangle((10, 10, width-10, (height)-20), outline=0, fill=(255, 255, 255))
                draw.text((20, 30), message, font=fnt, fill=0)
                disp.image(image)
                time.sleep(5)
                draw.rectangle((0, 0, width, height), outline=0, fill=(4,22,7))
                disp.image(image)
                return
            elif dealer_score >= 17:
                break
            else:
                dealer_hand.append(deal_card())

        #결과 비교
        if player_score > dealer_score:
            message = 'Player score: \n' + str(player_score) + '\nDealer hand: \n' + str(dealer_score) + '\nYou win!'
            draw.rectangle((10, 10, width-10, (height)-20), outline=0, fill=(255, 255, 255))
            draw.text((20, 30), message, font=fnt, fill=0)
            disp.image(image)
            time.sleep(5)
            draw.rectangle((0, 0, width, height), outline=0, fill=(4,22,7))
            disp.image(image)
        elif player_score == dealer_score:
            message = 'Player score: \n' + str(player_score) + '\nDealer hand: \n' + str(dealer_score) + '\nPush!'
            draw.rectangle((10, 10, width-10, (height)-20), outline=0, fill=(255, 255, 255))
            draw.text((20, 30), message, font=fnt, fill=0)
            disp.image(image)
            time.sleep(5)
            draw.rectangle((0, 0, width, height), outline=0, fill=(4,22,7))
            disp.image(image)
        else:
            message = 'Player score: \n' + str(player_score) + '\nDealer hand: \n' + str(dealer_score) + '\nYou lose!'
            draw.rectangle((10, 10, width-10, (height)-20), outline=0, fill=(255, 255, 255))
            draw.text((20, 30), message, font=fnt, fill=0)
            disp.image(image)
            time.sleep(5)
            draw.rectangle((0, 0, width, height), outline=0, fill=(4,22,7))
            disp.image(image)
    play_game()

def card_choosing(mod1):
    option_a_selected = False
    option_b_selected = False
    confirm_pressed = False
    mod1 = mod1
    
    game_going = True
    while game_going:
        draw.rectangle((0, 0, width, height), outline=0, fill=(4,22,7))
        if not button_U.value:
            option_a_selected = True
            option_b_selected = False
        elif not button_D.value:
            option_a_selected = False
            option_b_selected = True
        
        if option_a_selected:
            draw.rectangle((0, 0, width, height//2), outline=0, fill=(255, 0, 0))
            draw.rectangle((10, 10, width-10, (height//2)-10), outline=0, fill=(255, 255, 255))
            mod = '3'
            draw.text((20, 10), 'Play with \n ♦, ♥, ♣, ♠', font=fnt, fill=0)
            
        elif option_b_selected:
            draw.rectangle((0, height, width, height//2), outline=0, fill=(0, 0, 255))
            draw.rectangle((10, height-10, width-10, (height//2)+10), outline=0, fill=(255, 255, 255))
            mod = '4'
            draw.text((20, 130), 'Play with \n ♣, ♥', font=fnt, fill=0)
        if option_a_selected or option_b_selected:
            if not button_A.value:
                if not confirm_pressed:
                    if mod == '4':
                        confirm_pressed = True
                        deletecard_value = '1'
                        draw.rectangle((0, 0, width, height), outline=0, fill=(4,22,7))
                        disp.image(image)
                        if mod1 == '1':
                            for _ in range(3):
                                BPJ(deletecard_value)
                                time.sleep(1)
                            game_going = False
                        elif mod1 == '2':
                            for _ in range(5):
                                BPJ(deletecard_value)
                                time.sleep(1)
                            game_going = False
                    elif mod == '3':
                        confirm_pressed = True
                        deletecard_value = '0'
                        draw.rectangle((0, 0, width, height), outline=0, fill=(4,22,7))
                        disp.image(image)
                        if mod1 == '1':
                            for _ in range(3):
                                BPJ(deletecard_value)
                                time.sleep(1)
                        elif mod1 == '2':
                            for _ in range(5):
                                BPJ(deletecard_value)
                                time.sleep(1)
        disp.image(image)
        time.sleep(0.01)

def mode_choosing():
    option_a_selected = False
    option_b_selected = False
    
    mod1 = '0'
    
    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=(4,22,7))
        
        confirm_pressed = False
        if not button_U.value:
            option_a_selected = True
            option_b_selected = False
        elif not button_D.value:
            option_a_selected = False
            option_b_selected = True

        if option_a_selected:
            draw.rectangle((0, 0, width, height//2), outline=0, fill=(255, 0, 0))
            draw.rectangle((10, 10, width-10, (height//2)-10), outline=0, fill=(255, 255, 255))
            mod1 = '1'
            draw.text((20, 30), '3 times \nto play game', font=fnt, fill=0)
        elif option_b_selected:
            draw.rectangle((0, height, width, height//2), outline=0, fill=(0, 0, 255))
            draw.rectangle((10, height-10, width-10, (height//2)+10), outline=0, fill=(255, 255, 255))
            mod1 = '2'
            draw.text((20, 150), '5 times \nto play game', font=fnt, fill=0)
        if option_a_selected or option_b_selected:
            if not button_A.value:
                if not confirm_pressed:
                    confirm_pressed = True
                    mod1 = mod1
                    card_choosing(mod1)
                    break

        disp.image(image)

        time.sleep(0.01)

mode_choosing()