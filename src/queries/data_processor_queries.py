cleanFromToSQL = """
    DELETE FROM DBAHUMS.DE_PARA_HUMS
"""

checkExistsFromToSQL = """
    SELECT DISTINCT 0 FROM DBAHUMS.DE_PARA_HUMS            
"""

insertFromToSQL = """
    insert into dbahums.de_para_hums(
        cd_tiss, 
        dt_vigencia, 
        vl_honorario,
        vl_operacional,
        vl_total,
        sn_ativo,
        nm_usuario)
    values (
        :tiss,
        to_date(sysdate,'dd/mm/yy'),
        :vl_honorario,
        :vl_operacional,
        :valor,
        'S',
        user
    )
"""

insertFromToMatSQL = """
    insert into dbahums.de_para_hums(
        cd_tuss, 
        dt_vigencia, 
        vl_honorario,
        vl_operacional,
        vl_total,
        sn_ativo,
        nm_usuario)
    values (
        :tuss,
        to_date(sysdate,'dd/mm/yy'),
        :vl_honorario,
        :vl_operacional,
        :valor,
        'S',
        user
    )
"""

unregisteredProcedures = """
    SELECT DISTINCT
        DP.CD_TISS,
        IB.CD_PRO_FAT
    FROM
        DBAHUMS.DE_PARA_HUMS DP
        LEFT JOIN DBAMV.IMP_BRA IB ON DP.CD_TISS = IB.CD_TISS
    WHERE IB.CD_TISS IS NULL

"""