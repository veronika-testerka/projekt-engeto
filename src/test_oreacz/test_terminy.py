import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(
            headless=False,
            slow_mo=3000
        )  # Set headless=False to see the browser actions
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def test_terminy(page):
    page.goto("https://www.orea.cz/resort-horal")

    # potvrzeni cookies
    page.wait_for_selector('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll', timeout=60000)
    page.locator('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll').click()

    # zobrazeni terminu
    button_terminy_selector = 'body > div.main-container-safe.navbar-fixed > div.main-container > div.main-container-content > section:nth-child(1) > div > div.uheader-content-wrapper > div > div > button'
    page.wait_for_selector(button_terminy_selector, timeout=60000)
    page.locator(button_terminy_selector).click()

    # okno s terminy je v iframu, tak musime pouzit frame_locator
    iframe = page.frame_locator("#reservation-modal-iframe") 

    # pockame si na tlacitko pro objednani, a to nam rekne, ze je okno nacteno
    button_objednani_selector = "#__next > main > div > div.-mx-6.flex.flex-col.bg-lightMedium.px-6.py-8.text-white.sm\:mx-0.md\:col-span-3.md\:px-4.pb-20.sm\:pb-6 > div.mt-auto.space-y-4.pt-12 > div > a"
    button_objednani = iframe.locator(button_objednani_selector)
    button_objednani.wait_for(state="visible", timeout=10000)
    print("tlacitko nacteno")

    # v kalendari budeme vybirat termin od-do
    kalendar_selector = '#__next > main > div > div.py-8.md\:col-span-7 > div > div.grid.gap-6 > div > div.grid.grid-cols-7.divide-x.divide-y.border-b.border-r'
    kalendar = iframe.locator(kalendar_selector).nth(0)
    kalendar.wait_for(state="visible", timeout=10000)
    print("kalendar nacten")

    # tabindex=0 jsou dostupne dny
    dny = kalendar.locator('button[tabindex="0"]')
    print(f"pocet volnych terminu: {dny.count()}")

    # vybereme tridenni pobyt
    dny.nth(0).click()
    dny.nth(2).click()

    # jakmile tlacitko pro objednani nebude disabled, vime, ze termin je vybrany
    aria_disabled = button_objednani.get_attribute("aria-disabled")
    assert aria_disabled == "false", f"Atribute aria-disabled has value of '{aria_disabled}', expected 'false'"

    # objednavka se muze potvrdit
