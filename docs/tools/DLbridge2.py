from rdflib import Graph, Namespace, RDF, RDFS, OWL

# === 路径 ===
SRC_QK_FILE  = "MechOn-fluid/external/qudt-public-repo-3.1.4/vocab/quantitykinds/VOCAB_QUDT-QUANTITY-KINDS-ALL.ttl"        # QUDT -QK 原文件
SRC_UNIT_FILE = "MechOn-fluid/external/qudt-public-repo-3.1.4/vocab/unit/VOCAB_QUDT-UNITS-ALL.ttl"               # QUDT -Unit 原文件（只用于补 label，可选）
BRIDGE_FILE  = "MechOn-fluid/external/qk-bridge2.ttl"           # 输出 DL-safe 桥接

# === 命名空间 ===
QUDT      = Namespace("http://qudt.org/schema/qudt/")
QK        = Namespace("http://qudt.org/vocab/quantitykind/")
UNIT      = Namespace("http://qudt.org/vocab/unit/")

# === 读源文件 ===
g_qk   = Graph().parse(SRC_QK_FILE, format="turtle")
g_unit = Graph().parse(SRC_UNIT_FILE, format="turtle")

# === 构建桥接图 ===
bridge = Graph()
bridge.bind("qudt",     QUDT)
bridge.bind("qudtqk",   QK)
bridge.bind("qudtunit", UNIT)

# 1) 壳类，保持 DL
bridge.add((QUDT.QuantityKind, RDF.type, OWL.Class))
bridge.add((QUDT.Unit,          RDF.type, OWL.Class))

# 2) 遍历 QuantityKind 并复制映射
for qk_indiv in g_qk.subjects(RDF.type, QUDT.QuantityKind):
    bridge.add((qk_indiv, RDF.type, QUDT.QuantityKind))

    # label/comment（可删）
    for p in (RDFS.label, RDFS.comment):
        for o in g_qk.objects(qk_indiv, p):
            bridge.add((qk_indiv, p, o))

    # 复制 applicableUnit
    for unit_indiv in g_qk.objects(qk_indiv, QUDT.applicableUnit):
        bridge.add((qk_indiv, QUDT.applicableUnit, unit_indiv))
        bridge.add((unit_indiv, RDF.type, QUDT.Unit))

        # 给单位加 label（从 unit 文件里抓）
        for lbl in g_unit.objects(unit_indiv, RDFS.label):
            bridge.add((unit_indiv, RDFS.label, lbl))

# 3) 保存
bridge.serialize(BRIDGE_FILE, format="turtle")
print(f"✅ Bridge written to {BRIDGE_FILE} ({len(bridge)} triples)")
