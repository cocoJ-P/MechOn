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

        # 获取本体中定义的所有命名空间
        namespaces = {}
        for prefix, namespace in self.ontology.namespaces():
            if prefix == self.ontology_prefix:
                namespaces[prefix] = namespace
                print(namespaces)
                QUDT_QK = Namespace(namespace)
        # return self.ontology, namespaces
        print(QUDT_QK)
        # 添加QUDT命名空间, 并添加QuantityKind顶级类
        self.ontology.bind("qudt.quantitykind", QUDT_QK)
        self.ontology.add(
            (
                QUDT.QuantityKind,
                URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                URIRef("http://www.w3.org/2002/07/owl#Class"),
            )
        )
        # 只处理数量类型相关的实体，避免为所有三元组的主语添加类型
        # 查找所有可能的数量类型实体（通常以特定URI模式开头）
        for s, p, o in self.ontology.triples((None, None, None)):
            # 只处理主语是URI且属于数量类型命名空间的实体
            if isinstance(s, URIRef) and str(s).startswith(str(QUDT_QK)):
                # 避免重复添加类型声明
                if not self.ontology.triples(
                    (
                        s,
                        URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                        QUDT.QuantityKind,
                    )
                ):
                    self.ontology.add(
                        (
                            s,
                            URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                            QUDT.QuantityKind,
                        )
                    )
        self.ontology.serialize("qk-bridge.ttl")


if __name__ == "__main__":
    ontology_file = "MechOn-fluid/MechOn-fluid/external/qudt-public-repo-3.1.4/vocab/quantitykinds/VOCAB_QUDT-QUANTITY-KINDS-ALL.ttl"
    dlbridge = DLbridge(ontology_file, "quantitykind")
    dlbridge.get_ontology()
    # ontology, namespaces = dlbridge.get_ontology()
    # print("本体图:", ontology)
    # print("命名空间:")
    # for prefix, namespace in namespaces.items():
    #     print(f"  {prefix}: {namespace}")
