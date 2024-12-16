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
    page.goto("https://vouchery.kreativnicesko.cz/")

    # tlacitko Jak se registrovat
    button = page.locator('body > main > div.pg-hp > section.dark-theme > div > div > div.about__row.about__row--reverse > div.about__text > div > a > span')
    button.click()
    
    # tlacitko Vyberte si
    button = page.locator('#procedure > div > div.pg-instructions__buttons > div > a > span')
    button.click()
    
    fulltext_selector = '#reference_filter_fulltext'
    page.wait_for_selector(fulltext_selector, timeout=60000)

    query = "Lenka"
    page.fill(fulltext_selector, query)

    # toto si tu necham, kdybych s tim jeste nekdy bojovala
    #page.press(fulltext_selector, "Enter") # funguje, ale neodesle formular, takze se neobnovi vysledky
    #page.locator("#fulltext-search-btn").click() # funguje, ale neodesle formular, takze se neobnovi vysledky
    #page.locator("#sidebarFilter > div > form").evaluate("form => form.submit()") # funguje, obnovi vysledky, ale pouzivam javascript na odeslani formulare

    # funguje, obnovi vysledky, ale musim zmenit spatny type="button" na type="submit"
    page.locator("#fulltext-search-btn").evaluate("el => el.setAttribute('type', 'submit')")
    page.locator("#fulltext-search-btn").click()

    # tady nemuzeme pouzit wait_for_selector, protoze uz tam je, a tak pockame na obnovu
    page.wait_for_timeout(3000)

    # z vysledku bereme rovnou vsechny odkazy do detailu
    search_results = page.query_selector_all('#creativesList div.gallery-item__action > div.btn.btn--primary-link > a')
    assert len(search_results) > 0, "No search results found"
    print(f"Number of search results: {len(search_results)}")

    # zadala jsem si, ze budu klikat na druhy v poradi, tak musime otestovat, jestli tam alespon dva vysledky jsou
    assert len(search_results) >= 2, "Less than two search results found"
    search_results[1].click()

    # cekam na nacteni profilu
    nadpis_selector = 'body > main > div.pg-cr-detail h1'
    page.wait_for_selector(nadpis_selector, timeout=60000)
    assert page.locator(nadpis_selector).text_content() == "Detail kreativce", "Detail was not loaded"
