from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import asyncio
import nest_asyncio
import time

def date():
    # Mapping anglais → français
    mois_fr = {
        "January": "janvier",
        "February": "février",
        "March": "mars",
        "April": "avril",
        "May": "mai",
        "June": "juin",
        "July": "juillet",
        "August": "août",
        "September": "septembre",
        "October": "octobre",
        "November": "novembre",
        "December": "décembre"
    }

    # Date de départ
    date_depart = datetime.now()
    
    # Ajouter 45 jours
    date_updatee = date_depart + timedelta(days=45)
    
    # Récupérer le mois en anglais
    mois_anglais = date_updatee.strftime('%B')
    jour = date_updatee.strftime('%d')
    
    # Convertir en français et construire la chaîne
    date_str = f"{mois_fr[mois_anglais]} {jour},"
    
    return date_str


nest_asyncio.apply()

async def main():
    async with async_playwright() as p:
        # Lancer le navigateur Chromium en mode asynchrone car sur Jupyter il faut être asynchrone
        browser = await p.chromium.launch(headless=False)  # headless=False pour voir le navigateur
        page = await browser.new_page() # Ouvre une nouvelle page
    
        
        await page.goto("https://sport-dans-la-ville.doinsport.club/select-booking?guid=%221ce2c55d-6010-4f45-9b6f-1aafc04382fa%22&from=sport&activitySelectedId=%22cc4da804-1ef4-4f57-9fa4-4c203cdc06c8%22&categoryId=%22910503af-d67a-4f2b-a0df-838e0b4fb8ac%22") # Va sur l'URL demandé
        await page.locator("app-svg-container").get_by_role("img").click() # Click sur le logo calendrier pour ouvrir le calendrier
        for _ in range(2): # Si range est (2), c'est pour cliquer 2x afin d'avancer de 2 mois, etc...
            await page.locator("ion-calendar").get_by_role("button", name="chevron forward outline").click() # click sur fleche de droite x2 pour avancé de deux mois
        await page.get_by_label(date()).click() # Click sur le jour du mois
        
            
    
        # Naviguer jusqu'à la tranche horaire 16:00 - 20:00
        for direction in ['right', 'left']:
            for _ in range(5):
                await page.locator(f"button.btn-arrow-{direction}").click()
                creneau = await page.locator("div.value").text_content()  
                if "16:00 - 20:00" in creneau.lower():
                    await page.get_by_text("19:00").click()
                    numero_terrain = [4, 5, 7, 6, 3, 2, 1] # Prend les 7 terrains par ordre de préférence pour faire une boucle afin de trouver le 1er crénaux "Début19:0060 minA partir de100.00 €"
                    for i in numero_terrain: # Pour chaque numéro de terrain, trouver "Début19:0060 min"
                        text_playwriht = await page.get_by_text(f"Foot {i} Football 5vs5 - Exté").text_content() # Capturer  le text...
                        print(text_playwriht)
                        if "Début19:00" in text_playwriht and "60" in text_playwriht: # ... Si il y a le texte "Début19:0060 min", alors cliquer sur les pages suivantes
                            await page.locator("app-card-playground").filter(has_text=f"Foot {i} Football 5vs5 - Exté").locator("ion-label").filter(has_text="60 min").click()
                            await page.fill('input[placeholder="john.doe@example.com"]', 'jolie.mountain@gmail.com')
                            await page.get_by_text("Valider mon email").click()
                            await page.fill('input[placeholder="******"]', 'Toulouse31')
                            await page.get_by_text("Valider").click()
                            await page.get_by_text("Suivant").click()
                            await page.get_by_text("Payer et réserverPayer et ré").click()
                            await page.get_by_text("Ajouter une carte").click()
                            await page.locator("#ion-overlay-6 ion-radio").click()
                            await page.get_by_text("Sélectionner").click()
                            await page.get_by_text("Payer et réserver").nth(1).click()
                            await page.wait_for_timeout(1000)  # Attendre 500ms pour que la DOM se mette à jour
                            await page.pause()

asyncio.run(main())