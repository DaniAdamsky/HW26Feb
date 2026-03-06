import pygame
import random
import sys

# ── initialise ────────────────────────────────────────────────────────────────
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Capital City Quiz")
clock = pygame.time.Clock()

# ── colours ───────────────────────────────────────────────────────────────────
BG          = (15,  20,  40)
CARD        = (25,  35,  65)
ACCENT      = (80, 140, 255)
WHITE       = (255, 255, 255)
LIGHT_GREY  = (180, 190, 210)
GREEN       = ( 60, 210, 120)
RED         = (220,  70,  70)
YELLOW      = (255, 210,  60)
DARK_CARD   = (18,  26,  50)
BTN_HOVER   = (50, 100, 200)

# ── fonts ─────────────────────────────────────────────────────────────────────
font_title   = pygame.font.SysFont("segoeui", 44, bold=True)
font_q       = pygame.font.SysFont("segoeui", 26, bold=True)
font_opt     = pygame.font.SysFont("segoeui", 22)
font_score   = pygame.font.SysFont("segoeui", 20)
font_big     = pygame.font.SysFont("segoeui", 60, bold=True)
font_sub     = pygame.font.SysFont("segoeui", 28)

# ── data ──────────────────────────────────────────────────────────────────────
ALL_QUESTIONS = [
    ("What is the capital of France?",      ["Paris",       "Lyon",        "Marseille",  "Nice"       ], 1),
    ("What is the capital of Italy?",       ["Milan",       "Venice",      "Rome",       "Naples"     ], 3),
    ("What is the capital of Spain?",       ["Barcelona",   "Seville",     "Madrid",     "Valencia"   ], 3),
    ("What is the capital of Portugal?",    ["Porto",       "Lisbon",      "Faro",       "Braga"      ], 2),
    ("What is the capital of Greece?",      ["Thessaloniki","Athens",      "Patras",     "Heraklion"  ], 2),
    ("What is the capital of Netherlands?", ["Rotterdam",   "Utrecht",     "Eindhoven",  "Amsterdam"  ], 4),
    ("What is the capital of Belgium?",     ["Antwerp",     "Bruges",      "Brussels",   "Ghent"      ], 3),
    ("What is the capital of Switzerland?", ["Zurich",      "Geneva",      "Basel",      "Bern"       ], 4),
    ("What is the capital of Austria?",     ["Salzburg",    "Vienna",      "Graz",       "Innsbruck"  ], 2),
    ("What is the capital of Canada?",      ["Toronto",     "Vancouver",   "Ottawa",     "Montreal"   ], 3),
    ("What is the capital of Brazil?",      ["Rio de Janeiro","São Paulo", "Brasília",   "Salvador"   ], 3),
    ("What is the capital of Japan?",       ["Osaka",       "Tokyo",       "Kyoto",      "Hiroshima"  ], 2),
    ("What is the capital of Australia?",   ["Sydney",      "Melbourne",   "Canberra",   "Perth"      ], 3),
    ("What is the capital of India?",       ["Mumbai",      "New Delhi",   "Bangalore",  "Chennai"    ], 2),
    ("What is the capital of Egypt?",       ["Alexandria",  "Giza",        "Cairo",      "Luxor"      ], 3),
    ("What is the capital of Mexico?",      ["Guadalajara", "Monterrey",   "Cancún",     "Mexico City"], 4),
    ("What is the capital of Argentina?",   ["Córdoba",     "Rosario",     "Mendoza",    "Buenos Aires"], 4),
    ("What is the capital of South Korea?", ["Busan",       "Incheon",     "Seoul",      "Daegu"      ], 3),
    ("What is the capital of Sweden?",      ["Gothenburg",  "Malmö",       "Uppsala",    "Stockholm"  ], 4),
    ("What is the capital of Norway?",      ["Bergen",      "Oslo",        "Trondheim",  "Stavanger"  ], 2),
]

WIN_SCORE  = 5
MAX_MISSES = 3

# ── helpers ───────────────────────────────────────────────────────────────────
def draw_rounded_rect(surface, colour, rect, radius=16):
    pygame.draw.rect(surface, colour, rect, border_radius=radius)

def draw_text_centered(surface, text, font, colour, cx, cy):
    surf = font.render(text, True, colour)
    surface.blit(surf, surf.get_rect(center=(cx, cy)))

def wrap_text(text, font, max_width):
    """Split text into lines that fit within max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

# ── game state ────────────────────────────────────────────────────────────────
class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.questions    = list(ALL_QUESTIONS)
        random.shuffle(self.questions)
        self.score        = 0
        self.misses       = 0
        self.state        = "playing"   # "playing" | "feedback" | "win" | "lose"
        self.feedback_msg = ""
        self.feedback_col = WHITE
        self.selected     = None        # which button the player clicked
        self.correct_ans  = None
        self._load_next()

    def _load_next(self):
        if self.questions:
            q = self.questions.pop(0)
            self.question_text = q[0]
            self.options       = q[1]
            self.correct_ans   = q[2]   # 1-based
        self.selected = None

    def answer(self, choice):
        """Process a 1-based answer choice."""
        self.selected = choice
        if choice == self.correct_ans:
            self.score += 1
            self.feedback_msg = "✓  Correct!"
            self.feedback_col = GREEN
        else:
            self.misses += 1
            correct_city = self.options[self.correct_ans - 1]
            self.feedback_msg = f"✗  Wrong!  The answer was  {correct_city}"
            self.feedback_col = RED

        if self.score >= WIN_SCORE:
            self.state = "win"
        elif self.misses >= MAX_MISSES:
            self.state = "lose"
        else:
            self.state = "feedback"

    def next_question(self):
        self._load_next()
        self.state = "playing"

game = Game()

# ── button layout ─────────────────────────────────────────────────────────────
BTN_W, BTN_H = 340, 58
BTN_GAP       = 18
LEFT_X        = WIDTH // 2 - BTN_W - BTN_GAP // 2
RIGHT_X       = WIDTH // 2 + BTN_GAP // 2
TOP_Y         = 310

BUTTON_RECTS = [
    pygame.Rect(LEFT_X,  TOP_Y,               BTN_W, BTN_H),   # option 1
    pygame.Rect(RIGHT_X, TOP_Y,               BTN_W, BTN_H),   # option 2
    pygame.Rect(LEFT_X,  TOP_Y + BTN_H + 16,  BTN_W, BTN_H),   # option 3
    pygame.Rect(RIGHT_X, TOP_Y + BTN_H + 16,  BTN_W, BTN_H),   # option 4
]

NEXT_BTN  = pygame.Rect(WIDTH // 2 - 120, 490, 240, 52)
PLAY_BTN  = pygame.Rect(WIDTH // 2 - 130, 400, 260, 58)

# ── main loop ─────────────────────────────────────────────────────────────────
while True:
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if game.state == "playing":
                for i, rect in enumerate(BUTTON_RECTS):
                    if rect.collidepoint(mx, my):
                        game.answer(i + 1)   # convert 0-based index → 1-based answer

            elif game.state == "feedback":
                if NEXT_BTN.collidepoint(mx, my):
                    game.next_question()

            elif game.state in ("win", "lose"):
                if PLAY_BTN.collidepoint(mx, my):
                    game.reset()

    # ── draw ──────────────────────────────────────────────────────────────────
    screen.fill(BG)

    # top bar
    draw_rounded_rect(screen, DARK_CARD, pygame.Rect(0, 0, WIDTH, 80))
    draw_text_centered(screen, "🌍  Capital City Quiz", font_title, ACCENT, WIDTH // 2, 40)

    # score counters
    score_txt = font_score.render(f"✔  {game.score}  /  {WIN_SCORE}", True, GREEN)
    miss_txt  = font_score.render(f"✘  {game.misses}  /  {MAX_MISSES}", True, RED)
    screen.blit(score_txt, (30, 26))
    screen.blit(miss_txt,  (WIDTH - miss_txt.get_width() - 30, 26))

    # ── PLAYING / FEEDBACK screens ────────────────────────────────────────────
    if game.state in ("playing", "feedback"):

        # question card
        draw_rounded_rect(screen, CARD, pygame.Rect(60, 100, WIDTH - 120, 180))
        lines = wrap_text(game.question_text, font_q, WIDTH - 160)
        line_h = font_q.get_linesize()
        total_h = len(lines) * line_h
        start_y = 100 + (180 - total_h) // 2
        for li, line in enumerate(lines):
            draw_text_centered(screen, line, font_q, WHITE, WIDTH // 2, start_y + li * line_h + line_h // 2)

        # answer buttons
        labels = ["A", "B", "C", "D"]
        for i, (rect, opt) in enumerate(zip(BUTTON_RECTS, game.options)):
            # colour logic
            if game.state == "feedback":
                if i + 1 == game.correct_ans:
                    colour = GREEN
                elif i + 1 == game.selected:
                    colour = RED
                else:
                    colour = CARD
            else:
                colour = BTN_HOVER if rect.collidepoint(mx, my) else CARD

            draw_rounded_rect(screen, colour, rect)

            # label badge
            badge = pygame.Rect(rect.x + 10, rect.y + (BTN_H - 36) // 2, 36, 36)
            draw_rounded_rect(screen, ACCENT if colour == CARD or colour == BTN_HOVER else BG, badge, 8)
            draw_text_centered(screen, labels[i], font_opt, WHITE, badge.centerx, badge.centery)

            # option text
            opt_surf = font_opt.render(opt, True, WHITE)
            screen.blit(opt_surf, (rect.x + 58, rect.y + (BTN_H - opt_surf.get_height()) // 2))

        # feedback bar
        if game.state == "feedback":
            draw_rounded_rect(screen, DARK_CARD, pygame.Rect(60, 450, WIDTH - 120, 60))
            draw_text_centered(screen, game.feedback_msg, font_sub, game.feedback_col, WIDTH // 2, 480)

            nb_col = BTN_HOVER if NEXT_BTN.collidepoint(mx, my) else ACCENT
            draw_rounded_rect(screen, nb_col, NEXT_BTN)
            draw_text_centered(screen, "Next Question →", font_opt, WHITE, NEXT_BTN.centerx, NEXT_BTN.centery)

    # ── WIN screen ────────────────────────────────────────────────────────────
    elif game.state == "win":
        draw_rounded_rect(screen, CARD, pygame.Rect(100, 150, WIDTH - 200, 300))
        draw_text_centered(screen, "🎉  YOU WIN!", font_big, YELLOW, WIDTH // 2, 260)
        draw_text_centered(screen, f"You got {game.score} correct with only {game.misses} mistake(s).", font_sub, LIGHT_GREY, WIDTH // 2, 340)
        pb_col = BTN_HOVER if PLAY_BTN.collidepoint(mx, my) else ACCENT
        draw_rounded_rect(screen, pb_col, PLAY_BTN)
        draw_text_centered(screen, "Play Again", font_sub, WHITE, PLAY_BTN.centerx, PLAY_BTN.centery)

    # ── LOSE screen ───────────────────────────────────────────────────────────
    elif game.state == "lose":
        draw_rounded_rect(screen, CARD, pygame.Rect(100, 150, WIDTH - 200, 300))
        draw_text_centered(screen, "💀  GAME OVER", font_big, RED, WIDTH // 2, 260)
        draw_text_centered(screen, f"You scored {game.score} before getting {MAX_MISSES} wrong.", font_sub, LIGHT_GREY, WIDTH // 2, 340)
        pb_col = BTN_HOVER if PLAY_BTN.collidepoint(mx, my) else ACCENT
        draw_rounded_rect(screen, pb_col, PLAY_BTN)
        draw_text_centered(screen, "Try Again", font_sub, WHITE, PLAY_BTN.centerx, PLAY_BTN.centery)

    pygame.display.flip()
    clock.tick(60)