import pygame
import random
SHOP_ITEMS = [
    {"name": "Mitochondria", "cost": 10, "desc": "+1 ATP/sec"},
    {"name": "Ribosome",     "cost": 25, "desc": "+3 ATP/sec"},
    {"name": "Vacuole",      "cost": 50, "desc": "+5 ATP/sec"},
]


ORGANELLE_INFO = {
    "Mitochondria": "The powerhouse of the cell. Produces ATP for the cell via cellular respiration. He's why you're alive!",
    "Ribosome":     "Tiny but mighty! Builds proteins from amino acids. Also helps with protein synthesis.",
    "Vacuole":      "Storage unit of the cell. Holds water, nutrients, and waste."
}
# use for drawing later
ORGANELLE_VISUALS = {
    "Mitochondria": {"color": (220, 80, 80), "shape": "oval"},
    "Ribosome": {"color": (80, 80, 220), "shape": "circle"},
    "Vacuole": {"color": (80, 200, 120), "shape": "rect"},

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
    for o in organelles:
        x, y = o["pos"]
        color = ORGANELLE_VISUALS[o["name"]]["color"]
        shape = ORGANELLE_VISUALS[o["name"]]["shape"]

        if shape == "oval":
            pygame.draw.ellipse(screen, color, [x, y, 40, 22])
            pygame.draw.ellipse(screen, (245,149,66), [x,y,40,22], 0)
        if shape == "circle":
            pygame.draw.circle(screen, (255, 255, 255), (x + 7, y + 7), 2)
        if shape == "rect":
            # vacoule
            rect_coords = [x,y,45,35]
            pygame.draw.rect(screen, color, rect_coords, border_radius=5)
            pygame.draw.rect(screen, (255, 255, 255), [x + 5, y + 5, 10, 5], border_radius=2)





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

        # Button background: grey out if can't afford
        color = (200, 230, 200) if can_afford else (200, 200, 200)
        btn_rect = pygame.Rect(shop_x + 10, item_y, 188, 75)
        pygame.draw.rect(screen, color, btn_rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), btn_rect, 2, border_radius=6)

        # Name
        name_surf = font.render(item["name"], True, (0, 0, 0))
        screen.blit(name_surf, (shop_x + 15, item_y + 5))

        # Cost + description
        cost_surf = small_font.render(f"Cost: {item['cost']} ATP  {item['desc']}", True, (60, 60, 60))
        screen.blit(cost_surf, (shop_x + 15, item_y + 35))

        # Owned count
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