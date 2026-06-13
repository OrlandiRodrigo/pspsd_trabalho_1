import requests
import time

BASE_URL = "http://localhost:8080/api/v1"

def povoar_sistema():
    print("="*50)
    print("INICIANDO POVOAMENTO DA BASE DE DADOS")
    print("="*50)

    # ---------------------------------------------------------
    # 1. CRIAR FUNCIONÁRIO (ADMIN)
    # ---------------------------------------------------------
    print("\n1. Criando conta de Administrador")
    admin_data = {
        "email": "admin@frotanext.com",
        "nome_completo": "Administrador Supremo",
        "senha": "admin"
    }
    
    try:
        res_admin = requests.post(f"{BASE_URL}/auth/registar-funcionario", json=admin_data)
        if res_admin.status_code == 201:
            print("   Admin criado com sucesso!")
        elif res_admin.status_code == 400 and "já existe" in res_admin.text.lower():
            print("   Admin já existia na base de dados.")
        else:
            print(f"   Resposta inesperada: {res_admin.text}")
    except Exception as e:
        print(f"   Erro ao conectar com o Gateway. Ele está rodando? Erro: {e}")
        return

    # ---------------------------------------------------------
    # 2. FAZER LOGIN E PEGAR O TOKEN JWT
    # ---------------------------------------------------------
    print("\n2. Fazendo login...")
    login_data = {
        "email": admin_data["email"], 
        "senha": admin_data["senha"]
    }
    
    res_login = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if res_login.status_code != 200:
        print(f"   Falha no login. Resposta: {res_login.text}")
        return
    
    token = res_login.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("   Login efetuado. Token JWT capturado.")

    # ---------------------------------------------------------
    # 3. CRIAR VEÍCULO DE PASSEIO (COM POLIMORFISMO)
    # ---------------------------------------------------------
    print("\n3. Cadastrando um Veículo (Passeio)...")
    carro_data = {
        "placa": "FRO-2026",
        "marca": "Honda",
        "modelo": "Civic Touring",
        "cor": 1, 
        "valor_diaria": 250.00,
        "ano_fabricacao": 2025,
        "ano_modelo": 2026,
        "chassi": "9BWZZZTESTE123456",
        "renavam": "12345678900",
        "capacidade_tanque": 45.0,
        "cambio_automatico": True,
        "ar_condicionado": True,
        
        "tipo_veiculo": "PASSEIO",
        "tipo_carroceria": "Sedan",
        "qtde_portas": 4,
        "qtde_passageiros": 5
    }
    
    res_carro = requests.post(f"{BASE_URL}/veiculos/passeio", json=carro_data, headers=headers)
    
    if res_carro.status_code == 201:
        veiculo_criado = res_carro.json()
        print(f"   Veículo cadastrado com sucesso!")
        print(f"      ID: {veiculo_criado.get('id_veiculo')} | Placa: {veiculo_criado.get('placa')}")
    else:
        print(f"   Falha ao cadastrar veículo. C++ ou Python devolveram erro:")
        print(f"      {res_carro.text}")

    print("\n" + "="*50)
    print("SEED CONCLUÍDO.")

if __name__ == "__main__":
    povoar_sistema()