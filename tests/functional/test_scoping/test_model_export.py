from __future__ import unicode_literals

import io
from os.path import dirname, abspath, join

import textx.export as export
import textx.scoping as scoping
import textx.scoping.providers as scoping_providers
from textx import metamodel_from_file


def test_model_export():
    """
    This test checks that the export function (to graphdotviz)
    works with a model distributed across different files.
    It is checked that all filenames are included in the output
    and that some elements from every model file are incuded in the
    output.
    """
    #################################
    # META MODEL DEF
    #################################
    this_folder = dirname(abspath(__file__))

    def get_meta_model(provider, grammar_file_name):
        mm = metamodel_from_file(join(this_folder, grammar_file_name),
                                 debug=False)
        mm.register_scope_providers({
            "*.*": provider,
            "Call.method": scoping_providers.ExtRelativeName("obj.ref",
                                                             "methods",
                                                             "extends")
        })
        return mm

    import_lookup_provider = scoping_providers.FQNImportURI()

    a_mm = get_meta_model(
        import_lookup_provider, this_folder + "/metamodel_provider3/A.tx")
    b_mm = get_meta_model(
        import_lookup_provider, this_folder + "/metamodel_provider3/B.tx")
    c_mm = get_meta_model(
        import_lookup_provider, this_folder + "/metamodel_provider3/C.tx")

    scoping.MetaModelProvider.clear()
    scoping.MetaModelProvider.add_metamodel("*.a", a_mm)
    scoping.MetaModelProvider.add_metamodel("*.b", b_mm)
    scoping.MetaModelProvider.add_metamodel("*.c", c_mm)

    #################################
    # MODEL PARSING
    #################################

    m = a_mm.model_from_file(
        this_folder + "/metamodel_provider3/inheritance/model_a.a")

    out_file = io.StringIO()
    # export.model_export(
    #    None, "debug_test.dot", m._tx_model_repository.all_models )
    export.model_export_to_file(out_file, m)
    text = out_file.getvalue()

    print(text)
    assert "a2_very_long_name" in text
    assert "b2_very_long_name" in text
    assert "inheritance/model_a.a" in text
    assert "inheritance/model_b.b" in text
