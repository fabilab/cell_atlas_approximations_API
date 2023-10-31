let atlasapprox = require('..');

atlasapprox.setAPIURI("http://127.0.0.1:5000/" + atlasapprox.api_version + "/");

let result;
(async () => {

    // test measurement_types
    result = await atlasapprox.measurement_types();

    // test organisms
    result = await atlasapprox.organisms({});
    console.log(result);

    result = await atlasapprox.organisms({ measurement_type: "chromatin_accessibility" });
    console.log(result);

    // test organs
    result = await atlasapprox.organs({ organism: "m_musculus" });
    console.log(result);

    // cell types
    result = await atlasapprox.celltypes({ organism: "m_musculus", organ: "lung" });
    console.log(result);

    // features
    result = await atlasapprox.features({ organism: "m_musculus", organ: "lung" });
    console.log(result);

    // average
    result = await atlasapprox.average({ organism: "m_musculus", organ: "lung", features: ["Col1a1", "Ptprc"] });
    console.log(result);

    // fraction expressing
    result = await atlasapprox.fraction_detected({ organism: "m_musculus", organ: "lung", features: ["Col1a1", "Ptprc"] });
    console.log(result);

    // neighborhood
    result = await atlasapprox.neighborhood({ organism: "i_pulchra", organ: "whole", features: ["TRINITY_DN18225_c0_g1", "TRINITY_DN18226_c0_g1"] });
    console.log(result);

    // markers
    result = await atlasapprox.markers({ organism: "m_musculus", organ: "lung", celltype: "fibroblast" });
    console.log(result);

    // highest measurement
    result = await atlasapprox.highest_measurement({ organism: "m_musculus", feature: "Ins1" });
    console.log(result);

    // similar features
    result = await atlasapprox.similar_features({ organism: "m_musculus", organ: "lung", feature: "Ins1" });
    console.log(result);

    // similar cell types
    result = await atlasapprox.similar_celltypes({ organism: "m_musculus", organ: "lung", celltype: "fibroblast", features: ["Col1a1", "Col1a2"] });
    console.log(result);
    
    // cell type x organ table
    result = await atlasapprox.celltypexorgan({ organism: "m_musculus" });
    console.log(result);

    // cell type location
    result = await atlasapprox.celltype_location({ organism: "m_musculus", celltype: "fibroblast" });
    console.log(result);
    
    // data sources
    result = await atlasapprox.data_sources();
    console.log(result);

})();
