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
    def query_info_client(codcli):
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
                logger.warning(
                    f"⚠️ Consulta sem resultados para codcli: {codcli}")

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
                CODUSUR,
                DATA,
                SUM(FATURADO) AS FATURADO,
                SUM(LIBERADO) AS LIBERADO,
                SUM(BLOQUEADO) AS BLOQUEADO,
                SUM("VENDA TOTAL") AS "VENDA TOTAL"
            FROM
                VW_FXIN_CB_VENDRCA
            WHERE
                CODUSUR = ?
                AND TRUNC(DATA) BETWEEN TO_DATE(?, 'DD/MM/YYYY') AND TO_DATE(?, 'DD/MM/YYYY')
            GROUP BY
                CODUSUR,
                DATA
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
                CODUSUR,
                DATA,
                SUM(FATURADO) AS FATURADO,
                SUM(LIBERADO) AS LIBERADO,
                SUM(BLOQUEADO) AS BLOQUEADO,
                SUM("VENDA TOTAL") AS "VENDA TOTAL"
            FROM
                VW_FXIN_CB_VENDRCA
            WHERE
                CODUSUR = ?
                AND TRUNC(DATA) = TO_DATE(?, 'DD/MM/YYYY')
            GROUP BY
                CODUSUR,
                DATA
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
            result = oracle_db.execute_query(
                query, [codsupervisor, data1, data2])
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

    @staticmethod
    def sales_by_rca_fornec(codfornec, codemitente, data1, data2,):
        """Executa uma consulta no banco e retorna informações de vendas por emitente/fornecedor."""

        query = f"""
            WITH
                VENDAS AS (
                    SELECT
                        A.DATA,
                        B.CODUSUR,
                        D.CODFORNEC,
                        D.FORNECEDOR,
                        CASE
                            WHEN B.CODEMITENTE IN (8888, 882, 883)
                            THEN B.CODUSUR
                            ELSE (SELECT PCEMPR.CODUSUR FROM PCEMPR WHERE PCEMPR.MATRICULA = B.CODEMITENTE)
                        END AS CODEMITENTEPED,
                        ROUND(SUM((A.PVENDA - A.VLREPASSE) * A.QT),2) AS VENDALIQ,
                        SUM(A.QT) AS UNIDS,
                        COUNT (DISTINCT A.CODPROD) AS MIX,
                        COUNT (DISTINCT B.CODCLI) AS POSITIV
                    FROM
                        PCPEDI A
                        JOIN PCPEDC B ON A.NUMPED = B.NUMPED
                        JOIN PCPRODUT C ON A.CODPROD = C.CODPROD
                        JOIN PCFORNEC D ON C.CODFORNEC = D.CODFORNEC
                    WHERE
                        A.POSICAO IN ('F','L')
                        AND A.QT > 0
                        AND B.TIPOVENDA NOT IN ('5')
                    GROUP BY
                        A.DATA,
                        B.CODUSUR,
                        B.CODEMITENTE,
                        D.CODFORNEC,
                        D.FORNECEDOR
                ),

                METAS AS (
                    SELECT
                        E.DATA,
                        E.CODIGO,
                        E.CODUSUR,
                        E.VLVENDAPREV AS META
                    FROM
                        PCMETA E
                    WHERE
                        E.TIPOMETA = 'FR'
                )

            SELECT
                H.CODSUPERVISOR,
                E.CODUSUR AS CODEMITENTEPED,
                E.CODIGO,
                E.META AS META,
                NVL(SUM(G.VENDALIQ),0) AS VENDALIQ,
                NVL(SUM(G.UNIDS),0) AS UNIDS,
                NVL(SUM(G.MIX),0) AS MIX,
                NVL(SUM(G.POSITIV),0) AS POSITIV
            FROM
                METAS E
                JOIN PCUSUARI H ON E.CODUSUR = H.CODUSUR
                LEFT JOIN VENDAS G
                    ON E.CODUSUR = G.CODEMITENTEPED
                    AND E.CODIGO = G.CODFORNEC
                    AND G.DATA BETWEEN ? AND ?
            WHERE
                E.CODIGO = ?
                AND E.CODUSUR = ?
            GROUP BY
                H.CODSUPERVISOR,
                E.CODUSUR,
                E.CODIGO,
                E.META
            ORDER BY
                E.CODIGO
        """

        try:
            result = oracle_db.execute_query(
                query, [data1, data2, codfornec, codemitente,])
            if not result:
                logger.warning(f"⚠️ Nenhum dado encontrado.")

            return result if result else None
            """ A consulta deve retornar os dados (colunas) de acordo com o model que será criado para fazer o tráfego de dados."""

        except Exception as e:
            logger.error(
                f"❌ Erro ao executar consulta de vendas por emitente/fornecedor {e}", exc_info=True)
            return None
