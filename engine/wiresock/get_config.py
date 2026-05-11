from playwright.sync_api import sync_playwright
import os

def generate_warp_config(country='def', dns='cf', sites=None, variant=1):
    if sites is None:
        sites = []
    
    download_dir = os.path.dirname(os.path.abspath(__file__))
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        
        page.goto("https://warp-generator.github.io/")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("#generateButton1", state="visible")
        
        page.click("#infoButton")
        page.wait_for_selector("#infoModal", state="visible")
        
        server_map = {
            'def': 'label:has(input#def)',
            'FL': 'label:has(input#FL)',
            'NL': 'label:has(input#NL)',
            'PL': 'label:has(input#PL)',
            'DE': 'label:has(input#DE)',
            'LV': 'label:has(input#LV)',
            'RU': 'label:has(input#RU)',
            'lteFL': 'label:has(input#lteFL)',
            'ltePL': 'label:has(input#ltePL)',
        }
        page.click(server_map.get(country, 'label:has(input#def)'))
        
        dns_map = {
            'cf': 'label:has(input#cf)',
            'google': 'label:has(input#google)',
            'malw': 'label:has(input#malw)',
            'xbox': 'label:has(input#xbox)',
            'geohide': 'label:has(input#geohide)',
            'comss': 'label:has(input#comss)',
        }
        page.click(dns_map.get(dns, 'label:has(input#cf)'))
        
        for site in sites:
            selector = f'label:has(input#{site})'
            if page.locator(selector).count() > 0:
                page.click(selector)
        
        page.click("#infoModal .close")
        page.wait_for_timeout(500)
        
        button_map = {1: "#generateButton1", 2: "#generateButton2", 3: "#generateButton3"}
        button = button_map.get(variant, "#generateButton1")
        
        page.click(button)
        
        warning = page.locator("#warning")
        if warning.count() > 0 and warning.is_visible():
            
            page.click("#warning .close")
            page.wait_for_timeout(300)
            
            page.click("#infoButton")
            page.wait_for_selector("#infoModal", state="visible")
            
            page.click('label:has(input#def)')
            
            page.click("#infoModal .close")
            page.wait_for_timeout(300)
            
            with page.expect_download() as download_info:
                page.click(button)
            
            download = download_info.value
        else:
            with page.expect_download() as download_info:
                pass
            
            download = download_info.value
        
        saved_path = os.path.join(download_dir, f"warp-{country}.conf")
        download.save_as(saved_path)
        
        with open(saved_path, 'r', encoding='utf-8') as f:
            config = f.read()
        
        browser.close()
        return saved_path, config


if __name__ == '__main__':
    try:
        path, config = generate_warp_config(
            country='NL',
            dns='cf', 
            sites=['youtube', 'discord'],
            variant=1
        )
        
    except Exception as e:
        print(f"Error: {e}")