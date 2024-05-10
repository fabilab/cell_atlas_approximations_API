let atlasapprox = require('..');

// Uncomment to test local API server
//atlasapprox.setAPIURI("http://127.0.0.1:5000/" + atlasapprox.api_version + "/");

let result;
(async () => {

    console.log("test measurement_types");
    result = await atlasapprox.measurement_types();

    console.log("test organisms");
    result = await atlasapprox.organisms({});
    console.log(result);

    result = await atlasapprox.organisms({ measurement_type: "chromatin_accessibility" });
    console.log(result);

    console.log("test organs");
    result = await atlasapprox.organs({ organism: "m_musculus" });
    console.log(result);

    console.log("cell types");
    result = await atlasapprox.celltypes({ organism: "m_musculus", organ: "lung" });
    console.log(result);

    console.log("cell types with abundances");
    result = await atlasapprox.celltypes({ organism: "m_musculus", organ: "lung", include_abundance: true });
    console.log(result);

    console.log("features");
    result = await atlasapprox.features({ organism: "m_musculus", organ: "lung" });
    console.log(result);

    console.log("average");
    result = await atlasapprox.average({ organism: "m_musculus", organ: "lung", features: ["Col1a1", "Ptprc"] });
    console.log(result);

    console.log("fraction expressing");
    result = await atlasapprox.fraction_detected({ organism: "m_musculus", organ: "lung", features: ["Col1a1", "Ptprc"] });
    console.log(result);

    console.log("markers");
    result = await atlasapprox.markers({ organism: "m_musculus", organ: "lung", celltype: "fibroblast" });
    console.log(result);

    console.log("markers (other organs)");
    result = await atlasapprox.markers({ organism: "m_musculus", organ: "lung", celltype: "fibroblast", versus: "other_organs" });
    console.log(result);

    console.log("interaction_partners");
    result = await atlasapprox.interaction_partners({ organism: "m_musculus", features: "Cd19,Notch1" });
    console.log(result);

    console.log("highest measurement");
    result = await atlasapprox.highest_measurement({ organism: "m_musculus", feature: "Ins1" });
    console.log(result);

    console.log("similar features");
    result = await atlasapprox.similar_features({ organism: "m_musculus", organ: "lung", feature: "Ins1" });
    console.log(result);

    console.log("similar cell types");
    result = await atlasapprox.similar_celltypes({ organism: "m_musculus", organ: "lung", celltype: "fibroblast", features: ["Col1a1", "Col1a2"] });
    console.log(result);
    
    console.log("cell type x organ table");
    result = await atlasapprox.celltypexorgan({ organism: "m_musculus" });
    console.log(result);

    console.log("cell type location");
    result = await atlasapprox.celltype_location({ organism: "m_musculus", celltype: "fibroblast" });
    console.log(result);
    
    console.log("data sources");
    result = await atlasapprox.data_sources();
    console.log(result);

    console.log("neighborhood");
    result = await atlasapprox.neighborhood({ organism: "i_pulchra", organ: "whole", features: ["TRINITY_DN18225_c0_g1", "TRINITY_DN18226_c0_g1"] });
    console.log(result);

    console.log("neighborhood with embeddings");
    result = await atlasapprox.neighborhood({ organism: "i_pulchra", organ: "whole", features: ["TRINITY_DN18225_c0_g1", "TRINITY_DN18226_c0_g1"], include_embedding: true });
    console.log(result);

    result = await atlasapprox.neighborhood({ organism: "m_leidyi", organ: "whole", features: "ML25764a,ML358828a,ML071151a,ML065728a" });
    console.log(result);

})();
