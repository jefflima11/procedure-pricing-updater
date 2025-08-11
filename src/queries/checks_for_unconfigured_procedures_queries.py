checks_for_unconfigured_proceduresSQL = """"
    SELECT DISTINCT
        DP.CD_TISS,
        IB.CD_PRO_FAT
    FROM
        DBAHUMS.DE_PARA_HUMS DP
        LEFT JOIN DBAMV.IMP_BRA IB ON DP.CD_TISS = IB.CD_TISS
    WHERE IB.CD_TISS IS NULL
"""

procedures_unconfigured_log_medSQL = """
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

procedures_unconfigured_log_matSQL = """
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

insert_procedures_in_log_medSQL = """
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

delete_procedures_in_logSQL = """
    DELETE FROM DBAHUMS.LOG_PROC_NAO_CONFIG_HUMS
"""