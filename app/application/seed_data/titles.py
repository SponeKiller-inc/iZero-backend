# (name, priority) – titles with a lower priority are written closer to the beginning
# of the full name, e.g. "prof. Ing. Jan Novák, CSc., MBA"
PREFIX_TITLES: tuple[tuple[str, int], ...] = (
    ("prof.", 1),
    ("doc.", 2),
    ("MUDr.", 3),
    ("MDDr.", 3),
    ("MVDr.", 3),
    ("JUDr.", 3),
    ("PhDr.", 3),
    ("RNDr.", 3),
    ("PharmDr.", 3),
    ("PaedDr.", 3),
    ("ThDr.", 3),
    ("ThLic.", 3),
    ("Ing.", 4),
    ("Ing. arch.", 4),
    ("Mgr.", 4),
    ("MgA.", 4),
    ("Bc.", 5),
    ("BcA.", 5),
)

SUFFIX_TITLES: tuple[tuple[str, int], ...] = (
    ("DrSc.", 1),
    ("CSc.", 2),
    ("Ph.D.", 3),
    ("Th.D.", 3),
    ("MBA", 4),
    ("DBA", 4),
    ("MPA", 4),
    ("LL.M.", 4),
    ("MSc.", 4),
    ("DiS.", 5),
)
