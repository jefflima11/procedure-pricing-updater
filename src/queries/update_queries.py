updateNewValuesSQL = """
    INSERT INTO DBAMV.VAL_PRO(
        CD_TAB_FAT,
        CD_PRO_FAT,
        DT_VIGENCIA,
        VL_HONORARIO,
        VL_OPERACIONAL,
        VL_TOTAL,
        SN_ATIVO,
        NM_USUARIO
    ) VALUES (
        1,
        :CD_PRO_FAT,
        TO_DATE(SYSDATE,'DD/MM/YY'),
        0,
        0,
        :NEW_VALUE,
        'S',
        USER
    )
"""

checkUpdateSQL = """
    SELECT DISTINCT 0 FROM DBAMV.VAL_PRO WHERE DT_VIGENCIA = TO_DATE(SYSDATE,'DD/MM/YY')
"""

cleanUpdateSQL = """
    DELETE FROM DBAMV.VAL_PRO WHERE DT_VIGENCIA = TO_DATE(SYSDATE,'DD/MM/YY')
"""