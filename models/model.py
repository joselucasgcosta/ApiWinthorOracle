from logger.setup_logger import setup_logger, get_logger
from connection.oracle_conn import OracleConnection

# Configura o logger
setup_logger()
logger = get_logger(__name__)

oracle_db = OracleConnection()

class Model:
    """Classe base para modelos que interagem com o banco de dados Oracle"""
    
    @staticmethod
    def try_connection():
        """Executa uma consulta teste. Use para testar a conexão."""

        query = """
            SELECT DUMMY FROM DUAL
        """
        try:
            dual = oracle_db.execute_query(query, params=None)
            return dual
        except Exception as e:
            logger.error(f"❌ Erro na conexão de teste: {e}", exc_info=True)
            return None

    @staticmethod
    def query_info_client(codcli): # pode ser alterado o nome da função para algo mais específico seguindo as boas práticas, mas lembre-se de alterar na rota também
        """Executa uma consulta no banco e retorna informações"""
        
        # Query SQL para extrair informações do banco de dados
        query = """
            SELECT * FROM VW_FXON_SQL_PORTALCLIENTE WHERE CODCLI = ?
        """
        
        try:
            result = oracle_db.execute_query(query, [codcli]) 
            if not result:
                logger.warning(f"⚠️ Consulta sem resultados para codcli: {codcli}")

            return result if result else None
            """ A consulta deve retornar os dados (colunas) de acordo com o model que será criado para fazer o tráfego de dados."""

        except Exception as e:
            logger.error(f"❌ Erro ao executar consulta {e}", exc_info=True)
            return None
        
        