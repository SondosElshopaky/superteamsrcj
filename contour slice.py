                # ===== Crop the biggest contour =====






# TIP >>>>> U MUST CHANGE FEW VARIEZ ###################









x, y, w, h = cv2.boundingRect(contour)
cropped = img[y:y + h, x:x + w]

# ===== Split into 9 equal parts =====
cell_h = h // 1
cell_w = w // 2

tiles = []

for row in range(1):
    for col in range(2):
        x_start = col * cell_w
        y_start = row * cell_h
        tile = cropped[y_start:y_start + cell_h, x_start:x_start + cell_w]
        tiles.append(tile)




for i, tile in enumerate(tiles):


    cv2.imwrite(f"c:/Users/CYBER-TECH/Desktop/saves/Tile {i+1}.png", tile)