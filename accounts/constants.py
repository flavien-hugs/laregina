M = "Monsieur"
MME = "Madame"
MLLE = "Mademoiselle"

CIVILITY_CHOICES = (
    (M, "Monsieur"),
    (MME, "Madame"),
    (MLLE, "Mademoiselle"),
)

DEFAULT_CIVILITY_CHOICES = M

MS_C = "Célibataire"
MS_M = "Marié(e)"
MS_V = "Veuf/ve"
MS_D = "Divorcé(e)"
MS_F = "Fiancé(e)"

MARITAL_STATUS_CHOICES = (
    (MS_C, "Célibataire"),
    (MS_M, "Marié(e)"),
    (MS_V, "Veuf/ve"),
    (MS_D, "Divorcé(e)"),
    (MS_F, "Fiancé(e)"),
)

DEFAULT_MARITAL_STATUS = MS_C

LE_CEPE = "CEPE - Certificat d'Etude Primaire et Elémentaire"
LE_BEPC = "BEPC - Brevet d’Étude du Premier Cycle"
LE_BAC = "BAC - Baccalauréat"
LE_BTS = "BTS - Brevet de Technicien Supérieur"
LE_DEUG = "DEUG - Diplôme d'Etudes Universitaires Générales"
LE_LICENCE = "Licence (1,2,3)"
LE_MASTER = "Master (1,2)"
LE_OTHERS = "Autres- Spécifier dans la note ci-dessous"

LEVEL_OF_EDUCATION_CHOICES = (
    (LE_CEPE, "CEPEC - Certificat d'Etude Primaire et Elémentaire"),
    (LE_BEPC, "BEPC - Brevet d’Étude du Premier Cycle"),
    (LE_BAC, "BAC - Baccalauréat"),
    (LE_BTS, "BTS - Brevet de Technicien Supérieur"),
    (LE_DEUG, "DEUG - Diplôme d'Etudes Universitaires Générales"),
    (LE_LICENCE, "Licence (1,2,3)"),
    (LE_MASTER, "Master (1,2)"),
    (LE_OTHERS, "Autres- Spécifier dans la note ci-dessous"),
)

DEFAULT_LEVEL_OF_EDUCATION_CHOICES = LE_CEPE
