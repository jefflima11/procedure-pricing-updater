cleanFromToSQL = """
    DELETE FROM DBAHUMS.DE_PARA_HUMS WHERE DT_VIGENCIA = TO_DATE(SYSDATE,'DD/MM/YY')
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