from rdflib import Graph, Namespace, URIRef, RDF, OWL
from pathlib import Path

# 定义QUDT命名空间
QUDT        = Namespace("http://qudt.org/schema/qudt/")
QUDT_QK     = Namespace("http://qudt.org/vocab/quantitykind/")
QUDT_UNIT   = Namespace("http://qudt.org/vocab/unit/")

class DLBridgeBuilder:
    """
    Build a DL‑safe stub bridge file from QUDT full vocab.
    Keeps ONLY rdf:type triples:  QuantityKind & Unit individuals.
    """
    def __init__(self, qk_file: str, unit_file: str):
        self.qk_file   = Path(qk_file)
        self.unit_file = Path(unit_file)
        self.stub = Graph()
        # bind prefixes for pretty output
        self.stub.bind("qudt", QUDT)
        self.stub.bind("qudtqk", QUDT_QK)
        self.stub.bind("qudtunit", QUDT_UNIT)

        # declare the shell classes exactly once
        self.stub.add((QUDT.QuantityKind, RDF.type, OWL.Class))
        self.stub.add((QUDT.Unit,          RDF.type, OWL.Class))

    def build(self):
        # --- process quantity kinds ---
        g_qk = Graph().parse(self.qk_file, format="turtle")
        for subj in {s for s, _, _ in g_qk.triples((None, None, None))
                     if isinstance(s, URIRef) and str(s).startswith(str(QUDT_QK))}:
            self.stub.add((subj, RDF.type, QUDT.QuantityKind))

        # --- process units ---
        g_unit = Graph().parse(self.unit_file, format="turtle")
        for subj in {s for s, _, _ in g_unit.triples((None, None, None))
                     if isinstance(s, URIRef) and str(s).startswith(str(QUDT_UNIT))}:
            self.stub.add((subj, RDF.type, QUDT.Unit))

    def serialize(self, out_path: str):
        self.stub.serialize(out_path, format="turtle")

# ------------------ usage ------------------
if __name__ == "__main__":
    qk_file   = "MechOn-fluid/external/qudt-public-repo-3.1.4/vocab/quantitykinds/VOCAB_QUDT-QUANTITY-KINDS-ALL.ttl"
    unit_file = "MechOn-fluid/external/qudt-public-repo-3.1.4/vocab/unit/VOCAB_QUDT-UNITS-ALL.ttl"
    out_file  = "MechOn-fluid/external/qk-bridge.ttl"

    builder = DLBridgeBuilder(qk_file, unit_file)
    builder.build()
    builder.serialize(out_file)
    print(f"Stub written to {out_file}")

