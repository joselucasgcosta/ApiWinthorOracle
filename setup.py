#!/usr/bin/env python3
"""
Script de configuração inicial para API Winthor
===============================================

Este script ajuda na configuração inicial do projeto,
instalando dependências e verificando a configuração.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário")
        print(f"Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def check_java():
    """Verifica se o Java está instalado"""
    try:
        result = subprocess.run(['java', '-version'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            # Extrair versão da saída
            version_line = result.stderr.split('\n')[0]
            print(f"✅ Java instalado: {version_line}")
            return True
        else:
            print("❌ Java não encontrado")
            return False
    except FileNotFoundError:
        print("❌ Java não encontrado no PATH")
        return False

def check_jdbc_driver():
    """Verifica se o driver JDBC existe"""
    jdbc_path = Path("connection/ojdbc17.jar")
    if jdbc_path.exists():
        print(f"✅ Driver JDBC encontrado: {jdbc_path}")
        return True
    else:
        print(f"❌ Driver JDBC não encontrado: {jdbc_path}")
        print("   Baixe o driver Oracle JDBC e coloque em connection/ojdbc17.jar")
        return False

def check_env_file():
    """Verifica se o arquivo .env existe"""
    env_file = Path("environment/.env")
    example_file = Path("environment/.envexample")

    if env_file.exists():
        print("✅ Arquivo .env encontrado")
        return True
    elif example_file.exists():
        print("⚠️  Arquivo .env não encontrado")
        print("   Copie environment/.envexample para environment/.env")
        print("   E configure suas credenciais do Oracle")
        return False
    else:
        print("❌ Arquivo .envexample não encontrado")
        return False

def install_dependencies():
    """Instala as dependências do Python"""
    print("\n📦 Instalando dependências Python...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                      check=True)
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def test_connection():
    """Testa a conexão com o banco (se configurado)"""
    print("\n🔍 Testando conexão com o banco...")
    try:
        # Importar e testar conexão
        sys.path.append('.')
        from models.model import Model

        result = Model.try_connection()
        if result:
            print("✅ Conexão com o banco OK")
            return True
        else:
            print("❌ Erro na conexão com o banco")
            print("   Verifique suas configurações em environment/.env")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar conexão: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Configuração Inicial - API Winthor")
    print("=" * 40)

    checks = [
        ("Python 3.8+", check_python_version),
        ("Java Runtime", check_java),
        ("Driver JDBC", check_jdbc_driver),
        ("Arquivo .env", check_env_file),
    ]

    all_passed = True
    for name, check_func in checks:
        print(f"\n🔍 Verificando {name}...")
        if not check_func():
            all_passed = False

    if all_passed:
        print("\n✅ Todas as verificações passaram!")
        print("\n📦 Instalando dependências...")
        if install_dependencies():
            print("\n🔍 Testando configuração...")
            test_connection()

            print("\n🎉 Configuração concluída!")
            print("\nPara executar a API:")
            print("  uvicorn main:app --reload")
            print("\nPara ver a documentação:")
            print("  http://localhost:8000/docs")
    else:
        print("\n❌ Algumas verificações falharam.")
        print("   Corrija os problemas acima antes de continuar.")
        sys.exit(1)

if __name__ == "__main__":
    main()