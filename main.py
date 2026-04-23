import sys, pygame
from info import showI, draw_shop_button, draw_shop_panel, draw_inventory, draw_popup, SHOP_ITEMS, draw_organelles
import asyncio
import random
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Cell Tycoon Enterprise")
font = pygame.font.Font(pygame.font.get_default_font(), 24)
small_font = pygame.font.Font(pygame.font.get_default_font(), 18)



CLICK_MULTIPLIERS = {
    "Mitochondria": 2,
    "Ribosome": 4,
    "Vacuole": 8,
    "Chloroplast": 5,
    "Golgi Apparatus": 1
}

ATP_RATES = {
    "Mitochondria": 1,
    "Ribosome": 15,
    "Vacuole": 5,
    "Chloroplast": 10,
    "Golgi Apparatus": 0
}


 # python3 -m pygbag --build . && cp build/web/index.html . && cp build/web/codespaces-blank.apk . && cp build/web/codespaces-blank.tar.gz . && git add . && git commit -m "update game" && git push origin main
def calc_atp_per_second(inventory):
    total = 0
    for name, count in inventory.items():
        total += ATP_RATES.get(name, 0) * count

    golgi_count = inventory.get("Golgi Apparatus", 0)
    multiplier = 2 ** golgi_count



    return total * multiplier

def get_click_value(inventory):
    multiplier = 1
    for name, count in inventory.items():
        if count > 0:
            multiplier += CLICK_MULTIPLIERS.get(name, 0) * count
    return multiplier
async def main():
    AQUA = (176, 255, 211)
    total_atp = 0
    clock = pygame.time.Clock()
    showinfo = True
    shop_open = False
    inventory = {item["name"]: 0 for item in SHOP_ITEMS}
    message = ""
    message_timer = 0
    popup_organelle = ""
    popup_timer = 0
    atp_per_second = 0
    atp_accumulator = 0.0


    organelles = []



    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(AQUA)

        if showinfo:
            showI(screen, font)

        item_rects = []
        if shop_open:
            item_rects = draw_shop_panel(screen, font, inventory, total_atp)

        shop_button_rect = draw_shop_button(screen, font)

        pygame.draw.circle(screen, (150, 0, 150), (350, 300), 50)

        draw_inventory(screen, font, inventory)

        # atp counter
        atp_per_second = calc_atp_per_second(inventory)
        atp_surf = font.render(f"ATP: {total_atp} (+{get_click_value(inventory)}/click)", True, (0, 0, 0))
        screen.blit(atp_surf, (10, 10))

        # passive atp from upgrades
        atp_accumulator += atp_per_second * dt
        if atp_accumulator >= 1:
            total_atp += int(atp_accumulator)
            atp_accumulator -= int(atp_accumulator)

        # purchase feedback message
        if message_timer > 0:
            msg_surf = small_font.render(message, True, (200, 0, 0))
            screen.blit(msg_surf, (10, 50))
            message_timer -= 1

        # Popup
        if popup_timer > 0:
            draw_popup(screen, font, popup_organelle)
            popup_timer -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if shop_button_rect.collidepoint(event.pos):
                    shop_open = not shop_open

                elif shop_open:
                    for item, rect in item_rects:
                        if rect.collidepoint(event.pos):
                            if total_atp >= item["cost"]:
                                total_atp -= (item["cost"])
                                inventory[item["name"]] += 1
                                message = f"Bought {item['name']}!"
                                popup_organelle = item["name"]
                                popup_timer = 300

                                # add to screen
                                rx = random.randint(50, 550) # avoid shop panel
                                ry = random.randint(80, 520)
                                organelles.append({"name": item["name"], "pos": (rx,ry)})

                            else:
                                message = f"Not enough ATP for {item['name']}!"
                            message_timer = 120
                            break

                else:
                    total_atp += get_click_value(inventory)
                    showinfo = False



        draw_organelles(screen, organelles)
        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())