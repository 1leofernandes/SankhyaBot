# auto_fill_sankhya.py
from playwright.sync_api import sync_playwright
import time
import pathlib

URL = "https://peniel.sankhyacloud.com.br/mge/system.jsp#app/YnIuY29tLnNhbmtoeWEuY29tLm1vdi5BdHVhbGl6YVByZWNWZW5kYVBlbGFDb21wcmE="
FILL_VALUE = "teste automático 123"
OUT_DIR = pathlib.Path("./debug_out")
OUT_DIR.mkdir(exist_ok=True)

def main():
    with sync_playwright() as p:
        # Configurar browser
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        # Criar contexto com viewport grande
        context = browser.new_context(viewport=None)
        page = context.new_page()
        
        try:
            # Acessar a URL
            print("🌐 Acessando o Sankhya...")
            page.goto(URL, wait_until="networkidle", timeout=60000)
            
            print("🕐 Faça login manualmente no Sankhya...")
            input("Quando estiver logado e na tela principal, pressione ENTER aqui para continuar...")
            
            # Aguardar um pouco após o login
            time.sleep(3)
            
            # Salvar debug info
            ts = int(time.time())
            page.screenshot(path=str(OUT_DIR / f"after_login_{ts}.png"), full_page=True)
            
            print("🔍 Procurando o campo de input...")
            
            # Tentar diferentes seletores em ordem de prioridade
            selectors = [
                # Seletor específico que você forneceu
                "#simple-item-content > sk-hbox > sk-pesquisa-input > sk-text-input > input",
                # Seletores alternativos baseados nas classes
                "input.form-control.ng-pristine.ng-untouched.ng-valid.ng-empty",
                "input.form-control[ng-model='value']",
                "input[ng-model='value']",
                "input.form-control",
                # XPath alternativo
                "xpath=//input[@ng-model='value']",
                "xpath=//input[contains(@class, 'form-control')]",
                # Último recurso: qualquer input visível
                "input"
            ]
            
            element = None
            used_selector = None
            
            for selector in selectors:
                try:
                    if selector.startswith("xpath="):
                        element = page.query_selector(selector)
                    else:
                        element = page.query_selector(selector)
                    
                    if element and element.is_visible():
                        used_selector = selector
                        print(f"✅ Campo encontrado com: {selector}")
                        break
                except Exception as e:
                    continue
            
            if not element:
                print("❌ Nenhum campo encontrado com os seletores padrão.")
                print("📋 Tentando busca mais ampla...")
                
                # Buscar todos os inputs e filtrar
                all_inputs = page.query_selector_all("input")
                visible_inputs = [inp for inp in all_inputs if inp.is_visible()]
                
                print(f"📝 Total de inputs encontrados: {len(all_inputs)}")
                print(f"👀 Inputs visíveis: {len(visible_inputs)}")
                
                for i, inp in enumerate(visible_inputs[:5]):  # Mostrar apenas os 5 primeiros
                    class_attr = inp.get_attribute("class") or ""
                    print(f"  {i+1}. Classes: {class_attr}")
                
                if visible_inputs:
                    element = visible_inputs[0]
                    used_selector = "primeiro input visível"
                else:
                    print("❌ Nenhum input visível encontrado.")
                    return
            
            # Preencher o campo
            print(f"⌨️  Preenchendo campo com: '{FILL_VALUE}'")
            
            # Foco no elemento
            element.focus()
            time.sleep(0.5)
            
            # Limpar e preencher
            element.fill("")
            element.type(FILL_VALUE, delay=100)  # Digitar com delay para parecer humano
            
            # Disparar eventos para garantir que AngularJS detecte a mudança
            page.evaluate("""
                (element) => {
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new Event('blur', { bubbles: true }));
                }
            """, element)
            
            print("✅ Campo preenchido com sucesso!")
            
            # Salvar screenshot do resultado
            time.sleep(1)
            page.screenshot(path=str(OUT_DIR / f"after_fill_{ts}.png"), full_page=True)
            
            # Verificar se o valor foi realmente preenchido
            actual_value = element.input_value()
            print(f"📋 Valor atual no campo: '{actual_value}'")
            
            if actual_value == FILL_VALUE:
                print("🎉 Sucesso! O valor foi preenchido corretamente.")
            else:
                print("⚠️  Aviso: O valor pode não ter sido preenchido corretamente.")
            
            # Manter o browser aberto para inspeção
            print("\n🔍 O browser permanecerá aberto para inspeção...")
            print("   - Pressione Ctrl+C no terminal para fechar")
            input("   - Ou pressione ENTER para fechar agora...")
            
        except Exception as e:
            print(f"❌ Erro durante a execução: {e}")
            # Salvar screenshot de erro
            page.screenshot(path=str(OUT_DIR / f"error_{int(time.time())}.png"))
        finally:
            browser.close()

if __name__ == "__main__":
    main()