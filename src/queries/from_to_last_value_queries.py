from_to_last_value_medSQL="""
    SELECT
        DP.CD_TISS,
        IB.CD_PRO_FAT,
        DP.VL_TOTAL NEW_VALUE,
        VP_ULT.DT_VIGENCIA OLD_DATE,
        VP_ULT.VL_TOTAL OLD_VALUE
    FROM
        DBAHUMS.DE_PARA_HUMS DP
        INNER JOIN DBAMV.IMP_BRA IB ON DP.CD_TISS = IB.CD_TISS
        INNER JOIN (
            SELECT
                DT_VIGENCIA,
                CD_PRO_FAT,
                VL_TOTAL
            FROM (
                SELECT
                dt_vigencia,
                CD_PRO_FAT,
                VL_TOTAL,
                ROW_NUMBER() OVER (PARTITION BY cd_pro_fat ORDER BY DT_VIGENCIA DESC) rn
                FROM
                DBAMV.VAL_PRO VP
                WHERE
                CD_TAB_FAT = 1)
            WHERE
                RN = 1) VP_ULT ON IB.CD_PRO_FAT = VP_ULT.CD_PRO_FAT
    WHERE
        IB.CD_TAB_FAT = 1
"""

from_to_last_value_matSQL="""
    SELECT
        DP.CD_TUSS,
        I.CD_PRO_FAT,
        DP.VL_TOTAL NEW_VALUE,
        VP_ULT.DT_VIGENCIA OLD_DATE,
        VP_ULT.VL_TOTAL OLD_VALUE
    FROM
        DBAHUMS.DE_PARA_HUMS DP
        INNER JOIN DBAMV.IMP_SIMPRO I ON DP.CD_TUSS = DP.CD_TUSS
        INNER JOIN (
            SELECT
                DT_VIGENCIA,
                CD_PRO_FAT,
                VL_TOTAL
            FROM (
                SELECT
                dt_vigencia,
                CD_PRO_FAT,
                VL_TOTAL,
                ROW_NUMBER() OVER (PARTITION BY cd_pro_fat ORDER BY DT_VIGENCIA DESC) rn
                FROM
                DBAMV.VAL_PRO VP
                WHERE
                CD_TAB_FAT = 50)
            WHERE
                RN = 1) VP_ULT ON I.CD_PRO_FAT = VP_ULT.CD_PRO_FAT
    WHERE
        I.CD_TAB_FAT = 50
"""