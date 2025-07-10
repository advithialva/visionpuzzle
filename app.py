import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)
snapThreshold = 40
start_time = time.time()
total_time = 30  # seconds
game_state = "playing"

# Track mouse click
mouse_click_pos = None
def mouse_callback(event, x, y, flags, param):
    global mouse_click_pos
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_click_pos = (x, y)

cv2.namedWindow("Virtual Drag and Drop Puzzle Game")
cv2.setMouseCallback("Virtual Drag and Drop Puzzle Game", mouse_callback)

class PuzzleBox:
    def __init__(self, correct_pos, size=(150, 150)):
        self.correct_pos = correct_pos
        self.size = size

        while True:
            random_x = correct_pos[0] + np.random.randint(-300, 300)
            random_y = correct_pos[1] + np.random.randint(200, 400)
            dist = np.linalg.norm(np.array([random_x, random_y]) - np.array(correct_pos))
            if dist > 50:
                break

        self.current_pos = [random_x, random_y]
        self.snapped = False

    def update(self, cursor):
        if self.snapped:
            return
        cx, cy = self.current_pos
        w, h = self.size
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.current_pos = cursor

    def try_snap(self):
        dist = np.linalg.norm(np.array(self.current_pos) - np.array(self.correct_pos))
        if dist < snapThreshold:
            self.current_pos = self.correct_pos
            self.snapped = True

def reset_game():
    global pieces, start_time, game_state, mouse_click_pos
    pieces = [PuzzleBox(pos) for pos in positions]
    start_time = time.time()
    game_state = "playing"
    mouse_click_pos = None

# Grid positions
start_x, start_y = 500, 200
gap = 160
positions = [
    [start_x, start_y],
    [start_x + gap, start_y],
    [start_x, start_y + gap],
    [start_x + gap, start_y + gap]
]

reset_game()

# Button areas
button_try_again = ((500, 400), (780, 460))
button_exit = ((500, 480), (780, 540))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    cursor = None

    if hands:
        lmList = hands[0]["lmList"]
        if lmList and len(lmList) >= 9:
            cursor = lmList[8][:2]

    time_left = max(0, int(total_time - (time.time() - start_time)))

    # Handle mouse clicks
    if mouse_click_pos:
        mx, my = mouse_click_pos
        if game_state in ["complete", "gameover"]:
            if button_try_again[0][0] < mx < button_try_again[1][0] and \
               button_try_again[0][1] < my < button_try_again[1][1]:
                reset_game()
                continue
        if game_state == "gameover":
            if button_exit[0][0] < mx < button_exit[1][0] and \
               button_exit[0][1] < my < button_exit[1][1]:
                break
        mouse_click_pos = None  # Reset click

    # Game logic
    if game_state == "playing":
        if cursor:
            for piece in pieces:
                piece.update(cursor)
            for piece in pieces:
                piece.try_snap()
        if all(p.snapped for p in pieces):
            game_state = "complete"
        elif time_left <= 0:
            game_state = "gameover"

    overlay = img.copy()

    for pos in positions:
        gx, gy = pos
        cv2.rectangle(overlay, (gx - 75, gy - 75), (gx + 75, gy + 75), (0, 255, 0), 2)

    for piece in pieces:
        cx, cy = piece.current_pos
        w, h = piece.size
        color = (0, 255, 0) if piece.snapped else (255, 0, 255)
        cv2.rectangle(overlay, (cx - w // 2, cy - h // 2),
                      (cx + w // 2, cy + h // 2), color, cv2.FILLED)
        cvzone.cornerRect(overlay, (cx - w // 2, cy - h // 2, w, h), 20)

    img = cv2.addWeighted(overlay, 0.5, img, 0.5, 0)

    cv2.putText(img, f"Time Left: {time_left}s", (50, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    if game_state == "complete":
         # Background box with green fill and white border
        cv2.rectangle(img, (400, 300), (880, 500), (34, 139, 34), cv2.FILLED)  # Forest Green
        cv2.rectangle(img, (400, 300), (880, 500), (255, 255, 255), 4)

        # Puzzle Complete Text
        cv2.putText(img, "Puzzle Complete!", (430, 365),
                    cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 3)

        # Try Again Button
        cv2.rectangle(img, button_try_again[0], button_try_again[1], (0, 255, 255), cv2.FILLED)
        cv2.putText(img, "Try Again", (button_try_again[0][0] + 30, button_try_again[0][1] + 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

    elif game_state == "gameover":
         # Background Box
        cv2.rectangle(img, (400, 300), (880, 560), (20, 20, 20), cv2.FILLED)
        cv2.rectangle(img, (400, 300), (880, 560), (0, 0, 255), 4)

        # Game Over Text
        cv2.putText(img, "GAME OVER", (440, 360),
                    cv2.FONT_HERSHEY_DUPLEX, 1.8, (0, 0, 255), 4)

        # Try Again Button
        cv2.rectangle(img, button_try_again[0], button_try_again[1], (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Try Again", (button_try_again[0][0] + 20, button_try_again[0][1] + 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

        # Exit Button
        cv2.rectangle(img, button_exit[0], button_exit[1], (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "Exit", (button_exit[0][0] + 80, button_exit[0][1] + 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("Virtual Drag and Drop Puzzle Game", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()





        