viewer_last_update = """
    SELECT
        TO_DATE(DT_VIGENCIA,'DD/MM/YY') DT_VIGENCIA,
        TO_CHAR(DT_VIGENCIA, 'DD/MM/YYYY') VIGENCIA,
        TB.DS_TAB_FAT TABELA,
        NM_USUARIO USUARIO
    FROM
        DBAMV.VAL_PRO VP
            INNER JOIN DBAMV.TAB_FAT TB ON VP.CD_TAB_FAT = TB.CD_TAB_fAT
    WHERE
        DT_VIGENCIA BETWEEN to_date(:date_from,'dd/mm/yy') and to_date(:date_to, 'dd/mm/yy')
    AND TB.{tab_fat_condition}
    GROUP BY TO_DATE(DT_VIGENCIA, 'DD/MM/YY'), TB.DS_TAB_FAT, NM_USUARIO, TO_CHAR(DT_VIGENCIA, 'DD/MM/YYYY') 
    ORDER BY 1
"""