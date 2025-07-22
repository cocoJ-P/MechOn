from rdflib import Graph, Namespace, URIRef

# 定义QUDT命名空间
QUDT = Namespace("http://qudt.org/schema/qudt/")


class DLbridge:
    def __init__(self, ontology_file, ontology_prefix):
        self.ontology_file = ontology_file
        self.ontology = Graph()
        self.ontology.parse(ontology_file, format="turtle")
        self.ontology_prefix = ontology_prefix

    def get_ontology(self):

        # # 添加QUDT命名空间, 并添加QuantityKind顶级类
        # self.ontology.bind("qudt.quantitykind", Namespace(self.ontology_prefix))
        # self.ontology.add(
        #     (
        #         QUDT.QuantityKind,
        #         URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
        #         URIRef("http://www.w3.org/2002/07/owl#Class"),
        #     )
        # )
        # for s, _, _ in self.ontology.triples((None, None, None)):
        #     self.ontology.add(
        #         (
        #             s,
        #             URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
        #             QUDT.QuantityKind,
        #         )
        #     )
        # self.ontology.serialize("qk-bridge.ttl")

        # 获取本体中定义的所有命名空间
        namespaces = {}
        for prefix, namespace in self.ontology.namespaces():
            if prefix == self.ontology_prefix:
                namespaces[prefix] = namespace
        print(namespaces)
        # return self.ontology, namespaces


if __name__ == "__main__":
    ontology_file = "MechOn-fluid/MechOn-fluid/external/qudt-public-repo-3.1.4/vocab/quantitykinds/VOCAB_QUDT-QUANTITY-KINDS-ALL.ttl"
    dlbridge = DLbridge(ontology_file, "quantitykind")
    dlbridge.get_ontology()
    # ontology, namespaces = dlbridge.get_ontology()
    # print("本体图:", ontology)
    # print("命名空间:")
    # for prefix, namespace in namespaces.items():
    #     print(f"  {prefix}: {namespace}")
