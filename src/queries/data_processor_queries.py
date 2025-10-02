clean_from_toSQL = """
    DELETE FROM DBAHUMS.DE_PARA_HUMS
"""

checkExistsFromTo = """
    SELECT DISTINCT
        case
            when count(dt_vigencia) <> 0 and count(cd_tiss) <> 0 then 1
            when count(dt_vigencia) <> 0 and count(cd_tuss) <> 0 then 2
            else 3
        end t
    FROM DBAHUMS.DE_PARA_HUMS            
"""

insert_from_to_medSQL = """
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

insert_from_to_matSQL = """
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

unregistered_procedures = """
    SELECT DISTINCT
        DP.CD_TISS,
        IB.CD_PRO_FAT
    FROM
        DBAHUMS.DE_PARA_HUMS DP
        LEFT JOIN DBAMV.IMP_BRA IB ON DP.CD_TISS = IB.CD_TISS
    WHERE IB.CD_TISS IS NULL"""