cheksForUnconfiguredProceduresSQL = """"
    SELECT DISTINCT
        DP.CD_TISS,
        IB.CD_PRO_FAT
    FROM
        DBAHUMS.DE_PARA_HUMS DP
        LEFT JOIN DBAMV.IMP_BRA IB ON DP.CD_TISS = IB.CD_TISS
    WHERE IB.CD_TISS IS NULL
"""

proceduresUnconfiguredLogMedSQL = """
    SELECT DISTINCT
        TISS,
        CODIGO_BRASINDICE,
        VALOR,
        DESCRICAO
    FROM
        DBAHUMS.LOG_PROC_NAO_CONFIG_HUMS LP
        INNER JOIN (
                    SELECT DISTINCT
                        DP.CD_TISS
                    FROM
                        DBAHUMS.DE_PARA_HUMS DP
                        LEFT JOIN DBAMV.IMP_BRA IB ON DP.CD_TISS = IB.CD_TISS
                    WHERE IB.CD_TISS IS NULL
                    ) F ON LP.TISS = F.CD_TISS

"""                    

proceduresUnconfiguredLogMatSQL = """
    SELECT DISTINCT
        TUSS,
        VALOR,
        DESCRICAO
    FROM
        DBAHUMS.LOG_PROC_NAO_CONFIG_HUMS LP
        INNER JOIN (
                    SELECT DISTINCT
                        DP.CD_TUSS
                    FROM
                        DBAHUMS.DE_PARA_HUMS DP
                        LEFT JOIN DBAMV.IMP_SIMPRO I ON DP.CD_TUSS = I.CD_TUSS
                    WHERE I.CD_TUSS IS NULL
                    ) F ON LP.TUSS = F.CD_TUSS
"""

insertProceduresInLogMedSQL = """
    INSERT INTO DBAHUMS.LOG_PROC_NAO_CONFIG_HUMS(
        TISS,
        CODIGO_BRASINDICE,
        VALOR,
        DESCRICAO
    ) VALUES (
        :tiss,
        :codigo_brasindice,
        :valor,
        :descricao
    )
"""

insertProceduresInLogMatSQL = """
    INSERT INTO DBAHUMS.LOG_PROC_NAO_CONFIG_HUMS(
        TUSS,
        CODIGO_SIMPRO,
        VALOR,
        DESCRICAO
    ) VALUES (
        :tuss,
        :tuss,
        :valor,
        :descricao
    )
"""

deleteProceduresInLogSQL = """
    DELETE FROM DBAHUMS.LOG_PROC_NAO_CONFIG_HUMS
"""