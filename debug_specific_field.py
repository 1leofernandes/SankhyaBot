# debug_specific_field.py
from playwright.sync_api import sync_playwright
import time

def debug_field():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://peniel.sankhyacloud.com.br/mge/system.jsp")
        
        print("🔍 Faça login e navegue até a tela, depois pressione ENTER...")
        input()
        
        # Verificar o elemento específico
        selector = "#simple-item-content > sk-hbox > sk-pesquisa-input > sk-text-input > input"
        element = page.query_selector(selector)
        
        if element:
            print("✅ Elemento encontrado!")
            print(f"📝 Tag: {element.evaluate('el => el.tagName')}")
            print(f"👀 Visível: {element.is_visible()}")
            print(f"🔓 Habilitado: {element.is_enabled()}")
            print(f"🎯 Em foco: {element.evaluate('el => el === document.activeElement')}")
            print(f"📋 Classes: {element.get_attribute('class')}")
            print(f"📍 Placeholder: {element.get_attribute('placeholder')}")
            
            # Tentar focar
            element.focus()
            print("🎯 Elemento focado!")
            time.sleep(1)
            
            # Verificar se aceita input
            test_text = "TESTE"
            element.fill(test_text)
            actual_value = element.input_value()
            print(f"📝 Valor após preenchimento: '{actual_value}'")
            
            if actual_value == test_text:
                print("✅ Campo aceita input normalmente!")
            else:
                print("❌ Problema ao preencher campo")
        else:
            print("❌ Elemento não encontrado!")
            
            # Buscar elementos similares
            print("\n🔍 Procurando elementos similares...")
            similar = page.query_selector_all("sk-pesquisa-input sk-text-input input")
            print(f"Encontrados {len(similar)} elementos com estrutura similar")
            
            for i, el in enumerate(similar):
                print(f"  {i+1}. Classes: {el.get_attribute('class')}")
        
        input("Pressione ENTER para fechar...")
        browser.close()

if __name__ == "__main__":
    debug_field()
    