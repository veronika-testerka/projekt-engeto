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

def test_vouchery(page):
    page.goto("https://www.dm.cz/")

    print("cekani na susenky")
    
    # klik na odmitnout
    button = page.locator("#uc-show-more > div > a")
    button.click()

    # testujeme existenci sekce Nechte se okouzlit
    section = page.locator('#content-group-items-container-17')
    assert section.count() > 0, "No section found"

    # tlacitko Nechte se okouzlit nasim sortimentem - Zvirata, je 9. v poradi
    button = page.locator('#content-group-items-container-17 > li:nth-child(9) > div > div > a')

    # radeji otestujeme existenci selektoru, protoze uz jednou mi DM zmenilo strukturu
    assert button.count() > 0, "No section buttons found"
    button.click()

    search_results = page.locator('#tier-h1 > div > div > h1')
    text = search_results.text_content() 
    print(text) # zde nic netestujeme, jen vypiseme nazev stranky (je jedno, jestli to budou zvirata, nebo ne)

    # tady si ziskame vsechna tlacitka vsech produktu pro vlozeni do kosiku
    buttons = page.locator('ol li .pdd_14u321ic button')

    # otestujeme ze tam jsou vubec nejake produkty a hned pote, ze tam jsou alespon tri
    assert buttons.count() > 0, "No products found"
    assert buttons.count() > 2, "Less than two products found"

    # vime, ze jsou alespon tri, tak prvni a treti polozku vlozime do kosiku
    for i in [0,2]:
        buttons.nth(i).click()

    # zobrazime kosik
    page.locator('[data-dmid="cart-link"]').click()

    # pocitame polozky kosiku, ze tam zbozi bylo vlozeno
    polozky_kosiku_selector='[data-dmid="cart-entry-container"]'
    page.wait_for_selector(polozky_kosiku_selector, timeout=60000)

    assert page.locator(polozky_kosiku_selector).count() == 2, "Cart has different count of items than two"
    assert page.locator(polozky_kosiku_selector).count() > 0, "Cart is empty"

    # a ted uz se da odeslat objednavka
