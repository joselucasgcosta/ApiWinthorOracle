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
            SELECT
                CODCLI, CNPJ, CLIENTE, CLASSE,
                CASE
                    WHEN UF = 'MG' THEN 1 ELSE 2
                END AS CODFILIAL
            FROM
                FXIQVIACLI
            WHERE
                CODCLI = ?
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
        
    @staticmethod
    def answer_table(codfilial):
        """Executa uma consulta no banco e retorna informações"""
        
        # Query SQL para extrair informações do banco de dados
        query = """
            SELECT
                EAN, DESCRICAO, CODPROD, CODFILIAL, ESTOQUE, FAIXA_QTDE,
                PRECO_LIQ_SUGERIDO, PRECO_FIN_SUGERIDO, DOSAGEM, APRESENTACAO, PRINCIPATIVO
            FROM
                VW_FXIN_TAB_COT
            WHERE
                CODFILIAL = ?
        """
        
        try:
            result_cot = oracle_db.execute_query(query, [codfilial]) 
            if not result_cot:
                logger.warning(f"⚠️ Tabela de preços atualizada.")

            return result_cot if result_cot else None
            """ A consulta deve retornar os dados (colunas) de acordo com o model que será criado para fazer o tráfego de dados."""

        except Exception as e:
            logger.error(f"❌ Erro ao executar consulta {e}", exc_info=True)
            return None
    
    @staticmethod
    def sales_by_rca_between_dates(codusur, data1, data2):
        """Executa uma consulta no banco e retorna informações"""
        
        # Query SQL para extrair informações do banco de dados
        query = """
        SELECT
            *
        FROM
            VW_FXIN_CB_VENDRCA
        WHERE
            CODUSUR = ?
            AND TRUNC(DATA) BETWEEN TO_DATE(?, 'DD/MM/YYYY') AND TO_DATE(?, 'DD/MM/YYYY')
        """
        
        try:
            result = oracle_db.execute_query(query, [codusur, data1, data2]) 
            if not result:
                logger.warning(f"⚠️ Nenhum dado encontrado.")

            return result if result else None
            """ A consulta deve retornar os dados (colunas) de acordo com o model que será criado para fazer o tráfego de dados."""

        except Exception as e:
            logger.error(f"❌ Erro ao executar consulta {e}", exc_info=True)
            return None

    @staticmethod
    def sales_by_rca(codusur, data1):
        """Executa uma consulta no banco e retorna informações"""
        
        # Query SQL para extrair informações do banco de dados
        query = """
        SELECT
            *
        FROM
            VW_FXIN_CB_VENDRCA
        WHERE
            CODUSUR = ?
            AND TRUNC(DATA) = TO_DATE(?, 'DD/MM/YYYY')
        """
        
        try:
            result = oracle_db.execute_query(query, [codusur, data1]) 
            if not result:
                logger.warning(f"⚠️ Nenhum dado encontrado.")

            return result if result else None
            """ A consulta deve retornar os dados (colunas) de acordo com o model que será criado para fazer o tráfego de dados."""

        except Exception as e:
            logger.error(f"❌ Erro ao executar consulta {e}", exc_info=True)
            return None
    
    @staticmethod
    def sales_by_superv_between_dates(codsupervisor, data1, data2):
        """Executa uma consulta no banco e retorna informações"""
        
        # Query SQL para extrair informações do banco de dados
        query = """
        SELECT
            *
        FROM
            VW_FXIN_CB_VENDSUPERV
        WHERE
            CODSUPERVISOR = ?
            AND DATA BETWEEN TO_DATE(?, 'DD/MM/YYYY') AND TO_DATE(?, 'DD/MM/YYYY')
        """
        
        try:
            result = oracle_db.execute_query(query, [codsupervisor, data1, data2]) 
            if not result:
                logger.warning(f"⚠️ Nenhum dado encontrado.")

            return result if result else None
            """ A consulta deve retornar os dados (colunas) de acordo com o model que será criado para fazer o tráfego de dados."""

        except Exception as e:
            logger.error(f"❌ Erro ao executar consulta {e}", exc_info=True)
            return None
    
    @staticmethod
    def sales_by_superv(codsupervisor, data1):
        """Executa uma consulta no banco e retorna informações"""
        
        # Query SQL para extrair informações do banco de dados
        query = """
        SELECT
            *
        FROM
            VW_FXIN_CB_VENDSUPERV
        WHERE
            CODSUPERVISOR = ?
            AND DATA = TO_DATE(?, 'DD/MM/YYYY')
        """
        
        try:
            result = oracle_db.execute_query(query, [codsupervisor, data1]) 
            if not result:
                logger.warning(f"⚠️ Nenhum dado encontrado.")

            return result if result else None
            """ A consulta deve retornar os dados (colunas) de acordo com o model que será criado para fazer o tráfego de dados."""

        except Exception as e:
            logger.error(f"❌ Erro ao executar consulta {e}", exc_info=True)
            return None

    @staticmethod
    def promos(codfilial, condicoes):
        query = """
            SELECT *
            FROM VW_FXIN_CB_PROMOS
            WHERE CODFILIAL = ?
            AND LOWER(DESCRICAO) LIKE '%' || LOWER(?) || '%'
        """
        params = [codfilial, condicoes]

        try:
            result = oracle_db.execute_query(query, params)
            if not result:
                logger.warning("⚠️ Nenhum dado encontrado.")
            return result if result else None
        except Exception as e:
            logger.error(f"❌ Erro ao executar consulta {e}", exc_info=True)
            return None

    @staticmethod
    def nf_xml_data(numnota):
        """Executa uma consulta no banco e retorna informações"""
        
        # Query SQL para extrair informações do banco de dados
        query = f"""
            SELECT
                *
            FROM
                VW_FXIN_XML_01
            WHERE
                ROWNUM = 1 AND
                NUMNOTA = ?
        """
        
        try:
            result = oracle_db.execute_query(query, [numnota,]) 
            if not result:
                logger.warning(f"⚠️ Nenhum dado encontrado.")

            return result if result else None
            """ A consulta deve retornar os dados (colunas) de acordo com o model que será criado para fazer o tráfego de dados."""

        except Exception as e:
            logger.error(f"❌ Erro ao executar consulta {e}", exc_info=True)
            return None

    @staticmethod
    def boleto_data(numped):
        """Executa uma consulta no banco e retorna informações"""
        
        # Query SQL para extrair informações do banco de dados
        query = f"""
        SELECT
            NUMNOTA,
            NUMPED,
            CODCLI,
            CLIENTE,
            NUMDOC,
            VALOR,
            DTVENC,
            NOSSONUMBCO,
            LINHADIG
        FROM
            VW_FXIN_CB_DADOSBOLETO
        WHERE
        ROWNUM = 1 AND
        NUMNOTA = ?
        """
        
        try:
            result = oracle_db.execute_query(query, [numped,]) 
            if not result:
                logger.warning(f"⚠️ Nenhum dado encontrado.")

            return result if result else None
            """ A consulta deve retornar os dados (colunas) de acordo com o model que será criado para fazer o tráfego de dados."""

        except Exception as e:
            logger.error(f"❌ Erro ao executar consulta {e}", exc_info=True)
            return None