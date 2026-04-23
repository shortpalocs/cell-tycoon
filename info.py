import pygame
import random
import math

SHOP_ITEMS = [
    {"name": "Mitochondria", "cost": 25, "desc": "+1 ATP/sec"},
    {"name": "Ribosome", "cost": 50, "desc": "+3 ATP/sec"},
    {"name": "Vacuole", "cost": 75, "desc": "+5 ATP/sec"},
    {"name": "Chloroplast", "cost": 500, "desc": "+10 ATP/sec"},
    {"name": "Golgi Apparatus", "cost": 10000, "desc": "Doubles all income."}
]

ORGANELLE_INFO = {
    "Mitochondria": "The powerhouse of the cell. Produces ATP for the cell via cellular respiration. He's why you're alive!",
    "Ribosome": "Tiny but mighty! Builds proteins from amino acids. Also helps with protein synthesis.",
    "Vacuole": "Storage unit of the cell. Holds water, nutrients, and waste.",
    "Chloroplast": "Converts sunlight energy, carbon dioxide, and water into glucose for the cell.",
    "Golgi Apparatus": "Modifies, sorts, and packages proteins and lipids received from the endoplasmic reticulum (ER) into vesicles."

}
# use for drawing later
ORGANELLE_VISUALS = {
    "Mitochondria": {"color": (220, 80, 80), "shape": "oval"},
    "Ribosome": {"color": (80, 80, 220), "shape": "circle"},
    "Vacuole": {"color": (11, 217, 224), "shape": "rect"},
    "Chloroplast": {"color": (12, 245, 74), "shape": "oval"},
    "Golgi Apparatus": {"color": (255, 0, 115), "shape": "pancakes"}

}


def showI(screen, font):
    screen_w, screen_h = screen.get_size()
    box_w, box_h = 800, 400
    box_x = (screen_w - box_w) // 2
    box_y = (screen_h - box_h) // 2
    pygame.draw.rect(screen, (255, 255, 255), [box_x, box_y, box_w, box_h])
    pygame.draw.rect(screen, (0, 0, 0), [box_x, box_y, box_w, box_h], 5)
    text_surface = font.render("Welcome to Cell Tycoon Enterprise!", True, (0, 0, 0))
    screen.blit(text_surface, (box_x + 100, box_y + 100))
    instruction_surface = font.render("Click the Nucleus to start building...", True, (10, 20, 20))
    screen.blit(instruction_surface, (box_x + 100, box_y + 200))


def draw_organelles(screen, organelles):
    # unique pulse depending on time
    time_ms = pygame.time.get_ticks()
    pulse_offset = math.sin(time_ms / 500) * 8  # Goes smoothly from -8 to +8

    for o in organelles:
        x, y = o["pos"]
        visual = ORGANELLE_VISUALS.get(o["name"])
        if not visual: continue  # Safety check

        color = visual["color"]
        shape = visual["shape"]

        if shape == "oval" and o["name"] == "Mitochondria":
            flicker = math.sin(time_ms / 100) * 40
            glow_color = (min(255, color[0] + flicker), color[1], color[2])

            pygame.draw.ellipse(screen, glow_color, [x, y, 40, 22])
            # zig zag line inside
            pygame.draw.lines(screen, (255, 255, 255), False,
                              [(x + 5, y + 11), (x + 15, y + 5), (x + 25, y + 17), (x + 35, y + 11)], 2)

        if shape == "oval" and o["name"] == "Chloroplast":
            # shimmer effect
            shimmer = math.sin(time_ms / 600) * 50
            leaf_color = (color[0], min(255, color[1] + int(shimmer)), color[2])
            pygame.draw.ellipse(screen, leaf_color, [x, y, 40, 22])
            for i in range(3):
                pygame.draw.rect(screen, (0, 100, 0), [x + 10 + (i * 10), y + 6, 4, 10])

        elif shape == "circle":

            # jitter
            jx = random.randint(-1,1)
            jy = random.randint(-1,1)
            pygame.draw.circle(screen, color, (x+ 7 + jx, y + 7 + jy), 5)
            if math.sin(time_ms / 200) > 0.8:
                pygame.draw.circle(screen, (255,255,255), (x + 15, y - 5), 3)


        elif shape == "rect":
            rect_coords = [x, y, 45, 35]
            pygame.draw.rect(screen, color, rect_coords, border_radius=5)
            # vacoule water highlight
            sway = math.sin(time_ms / 1000) * 3
            pygame.draw.rect(screen, (255, 255, 255, 100), [x + 5 + sway, y + 5, 15, 5], border_radius=2)

        elif shape == "pancakes":
            # ANIMATION
            for i in range(5):

                layer_offset_x = (i * 2)
                layer_offset_y = (i * 8)

                # apply the pulse_offset to the width and x-position of each layer
                width = 60 + pulse_offset
                current_x = (x + layer_offset_x) - (pulse_offset / 2)  # keep centered


                shade = max(0, min(255, int(150 + (i * 20))))  # simple shading
                layer_color = (shade, 0, 80)  # darker version of magenta for depth

                pygame.draw.ellipse(screen, layer_color, [current_x, y + layer_offset_y, width, 15])
                pygame.draw.ellipse(screen, color, [current_x, y + layer_offset_y, width, 15], 2)


def get_safe_pos():
    while True:
        rx = random.randint(200, 540)
        ry = random.randint(80, 450)


        dist = math.sqrt((rx - 350) ** 2 + (ry - 300) ** 2)
        if dist > 90:  # If it's at least 70px away from the center
            return (rx, ry)


def draw_popup(screen, font, organelle_name):
    small_font = pygame.font.Font(pygame.font.get_default_font(), 16)
    info = ORGANELLE_INFO.get(organelle_name, "No info available.")

    panel_w, panel_h = 340, 100
    panel_x = (screen.get_width() - panel_w) // 2
    panel_y = screen.get_height() - panel_h - 20

    pygame.draw.rect(screen, (255, 255, 220), [panel_x, panel_y, panel_w, panel_h], border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), [panel_x, panel_y, panel_w, panel_h], 2, border_radius=8)

    title = font.render(organelle_name, True, (0, 0, 100))
    screen.blit(title, (panel_x + 10, panel_y + 10))

    words = info.split()
    line, lines = "", []
    for word in words:
        if small_font.size(line + word)[0] < panel_w - 20:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    for j, l in enumerate(lines):
        text = small_font.render(l, True, (0, 0, 0))
        screen.blit(text, (panel_x + 10, panel_y + 45 + j * 20))


# scrap this idea tbh
def calc_new_price():
    pass



def draw_shop_button(screen, font):
    button_rect = pygame.Rect(700, 10, 90, 40)
    pygame.draw.rect(screen, (80, 180, 80), button_rect, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2, border_radius=8)
    label = font.render("Shop", True, (255, 255, 255))
    screen.blit(label, (button_rect.x + 18, button_rect.y + 5))
    return button_rect


def draw_shop_panel(screen, font, inventory, total_atp):
    screen_w, screen_h = screen.get_size()
    shop_w = 210
    shop_x = screen_w - shop_w

    pygame.draw.rect(screen, (240, 240, 240), [shop_x, 0, shop_w, screen_h])
    pygame.draw.rect(screen, (0, 0, 0), [shop_x, 0, shop_w, screen_h], 3)

    title = font.render("Shop", True, (0, 0, 0))
    screen.blit(title, (shop_x + 70, 15))

    small_font = pygame.font.Font(pygame.font.get_default_font(), 16)
    item_rects = []

    for i, item in enumerate(SHOP_ITEMS):
        item_y = 70 + i * 90
        count = inventory.get(item["name"], 0)
        can_afford = total_atp >= item["cost"]

        # gray out if cant afford
        color = (200, 230, 200) if can_afford else (200, 200, 200)
        btn_rect = pygame.Rect(shop_x + 10, item_y, 188, 75)
        pygame.draw.rect(screen, color, btn_rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), btn_rect, 2, border_radius=6)

        name_surf = font.render(item["name"], True, (0, 0, 0))
        screen.blit(name_surf, (shop_x + 15, item_y + 5))

        # cost + description
        cost_surf = small_font.render(f"Cost: {item['cost']} ATP  {item['desc']}", True, (60, 60, 60))
        screen.blit(cost_surf, (shop_x + 15, item_y + 35))

        # owned count
        owned_surf = small_font.render(f"Owned: {count}", True, (0, 100, 0))
        screen.blit(owned_surf, (shop_x + 15, item_y + 53))

        item_rects.append((item, btn_rect))

    return item_rects


def draw_inventory(screen, font, inventory):
    small_font = pygame.font.Font(pygame.font.get_default_font(), 16)
    panel_w = 180
    panel_h = 30 + len(inventory) * 25 + 10
    panel_x = 10
    panel_y = 80

    pygame.draw.rect(screen, (255, 255, 255), [panel_x, panel_y, panel_w, panel_h], border_radius=6)
    pygame.draw.rect(screen, (0, 0, 0), [panel_x, panel_y, panel_w, panel_h], 2, border_radius=6)

    title = small_font.render("Inventory", True, (0, 0, 0))
    screen.blit(title, (panel_x + 10, panel_y + 8))

    for i, (name, count) in enumerate(inventory.items()):
        color = (0, 130, 0) if count > 0 else (150, 150, 150)
        text = small_font.render(f"{name}: {count}", True, color)
        screen.blit(text, (panel_x + 10, panel_y + 30 + i * 25))