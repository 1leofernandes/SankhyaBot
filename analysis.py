# deep_analysis.py
from playwright.sync_api import sync_playwright
import time
import json

def deep_analysis():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://peniel.sankhyacloud.com.br/mge/system.jsp")
        
        print("🔍 Faça login e navegue até a tela com o campo desejado...")
        input("Quando estiver na tela correta, pressione ENTER...")
        
        # Salvar HTML completo para análise
        with open("page_content.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        print("✅ HTML salvo como 'page_content.html'")
        
        # Análise completa da estrutura
        print("\n🔍 ANALISANDO ESTRUTURA DA PÁGINA:")
        
        # 1. Verificar se há Shadow DOM
        shadow_hosts = page.evaluate("""() => {
            const hosts = Array.from(document.querySelectorAll('*')).filter(el => 
                el.shadowRoot
            );
            return hosts.map(el => ({
                tag: el.tagName,
                id: el.id,
                classes: el.className
            }));
        }""")
        
        print(f"🌑 Hosts de Shadow DOM encontrados: {len(shadow_hosts)}")
        for host in shadow_hosts:
            print(f"   - {host['tag']} (id: {host['id']}, classes: {host['classes']})")
        
        # 2. Buscar todos os elementos customizados (sk-*)
        custom_elements = page.evaluate("""() => {
            const elements = Array.from(document.querySelectorAll('*')).filter(el => 
                el.tagName.toLowerCase().includes('-')
            );
            return elements.map(el => ({
                tag: el.tagName,
                id: el.id,
                classes: el.className,
                children: el.children.length,
                hasShadow: !!el.shadowRoot
            }));
        }""")
        
        print(f"\n🔧 Elementos customizados: {len(custom_elements)}")
        for elem in custom_elements[:20]:  # Mostrar apenas os primeiros 20
            print(f"   - {elem['tag']} (id: {elem['id']}, children: {elem['children']}, shadow: {elem['hasShadow']})")
        
        # 3. Buscar elementos por texto ou placeholder
        print("\n🔍 Procurando elementos por contexto...")
        
        # Tentar encontrar pelo contexto visual
        possible_containers = page.evaluate("""() => {
            // Buscar elementos que podem conter inputs
            const containers = Array.from(document.querySelectorAll('*')).filter(el => {
                const text = el.textContent || '';
                return text.includes('Pesquisa') || 
                       text.includes('Código') || 
                       text.includes('Descrição') ||
                       el.tagName.toLowerCase().includes('input') ||
                       el.tagName.toLowerCase().includes('search');
            });
            
            return containers.map(el => ({
                tag: el.tagName,
                id: el.id,
                classes: el.className,
                text: (el.textContent || '').substring(0, 100),
                children: el.children.length
            }));
        }""")
        
        print(f"🎯 Elementos contextuais encontrados: {len(possible_containers)}")
        for container in possible_containers[:10]:
            print(f"   - {container['tag']}: '{container['text']}'")
        
        # 4. Tentar acessar via JavaScript direto no contexto Angular
        print("\n🔍 Tentando acessar via Angular...")
        
        angular_info = page.evaluate("""() => {
            if (typeof angular !== 'undefined') {
                // Tentar encontrar elementos com ng-model
                const elements = Array.from(document.querySelectorAll('[ng-model]'));
                return elements.map(el => ({
                    tag: el.tagName,
                    ngModel: el.getAttribute('ng-model'),
                    id: el.id,
                    classes: el.className
                }));
            }
            return [];
        }""")
        
        print(f"🅰️  Elementos com ng-model: {len(angular_info)}")
        for elem in angular_info:
            print(f"   - {elem['tag']}: ng-model='{elem['ngModel']}'")
        
        # 5. Método alternativo: clicar na área e usar teclado
        print("\n🎯 Método alternativo: coordenadas...")
        
        # Encontrar área clicável
        clickable_areas = page.evaluate("""() => {
            const areas = Array.from(document.querySelectorAll('*')).filter(el => {
                const rect = el.getBoundingClientRect();
                return rect.width > 100 && rect.height > 20 && 
                       window.getComputedStyle(el).cursor === 'pointer';
            });
            return areas.map(el => ({
                tag: el.tagName,
                text: (el.textContent || '').substring(0, 50),
                rect: el.getBoundingClientRect()
            }));
        }""")
        
        print(f"🖱️  Áreas clicáveis: {len(clickable_areas)}")
        for area in clickable_areas[:5]:
            print(f"   - {area['tag']}: '{area['text']}'")
        
        print("\n📁 HTML completo salvo como 'page_content.html'")
        print("📋 Por favor, me envie o conteúdo desse arquivo!")
        
        input("Pressione ENTER para fechar...")
        browser.close()

if __name__ == "__main__":
    deep_analysis()